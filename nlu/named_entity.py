from nlu.trainingdata_preprocessing import pre_process_for_entity_extraction
import sklearn_crfsuite
import pandas as pd
from pickle import load, dump
import nltk
nltk.download('punkt')
dff = pd.read_csv("emp_details.csv")
m_df = pd.read_csv("sales db.csv")
cdf = pd.DataFrame({'column' : m_df.columns})


def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]


def train_entity(data):
    data = data['text_entity']
    final_result = pre_process_for_entity_extraction(data)
    X_train = [sent2features(s) for s in final_result]
    y_train = [sent2labels(s) for s in final_result]
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)

    from sklearn_crfsuite import metrics
    labels = list(crf.classes_)
    labels.remove('O')
    labels
    y_pred = crf.predict(X_train)
    metrics.flat_f1_score(y_train, y_pred,
                          average='weighted', labels=labels)

    print(metrics.flat_classification_report(y_pred, y_train))
    dump(crf, open('entity_extraction.pkl', 'wb'))


def test(user_input):
    entity_list = []; entity_tok = []
    crf = load(open('nlu/entity_extraction.pkl', 'rb'))
    tokens = nltk.word_tokenize(user_input)
    tag = nltk.pos_tag(tokens)
    # print(tag)
    featured_input = sent2features(tag)
    # print(featured_input)
    y_pred = crf.predict([featured_input])
    # print(y_pred[0])
    for i in range(len(y_pred[0])):
        if y_pred[0][i] is not 'O':
            # print(y_pred[0][i])
            entity_list.append(y_pred[0][i])
            entity_tok.append(tokens[i])
            # entity.append({y_pred[0][i]: []})
    ent = seperate(entity_list, entity_tok)
    # print(ent, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    return ent


def seperate(entity,entity_val):
    new_dict = {}
    for dictionary in set(entity):
        new_dict[dictionary] = []
    for num,entities in enumerate(entity):
        new_dict[entities].append(entity_val[num])
    return [new_dict]


def simple_uv(df):
    obj = [column for column in df.columns if df[column].dtype == 'O']
    index_ranges = {}
    initial = 0
    for cols in obj:
        end = df[cols].dropna().nunique()+initial
        index_ranges[cols] = [i for i in range(initial,end)]
        initial = end
    collect = []
    la = lambda x:collect.extend(list(df[x].dropna().unique()))
    mapping = map(la,obj)
    [map_vals for map_vals in mapping]
    udfs = pd.DataFrame({'Unique_Values' :collect})
    return index_ranges,udfs


def get_startswith(splitted_query, index_ranges, unique_dataframe):
    df = unique_dataframe.copy()
    iv = []
    col = []
    position = []
    for index_, string in enumerate(splitted_query):
        try:
            if type(eval(string)) == int or type(eval(string)):
                position.append(len(col))
        #                print(len(col),">>>>>>POSITION<<<<<<<",string)
        except Exception as e:
            pass
        df['Unique_Values'] = df['Unique_Values'].str.lower()
        for i, j in enumerate(df[df['Unique_Values'].str.startswith(string)].values):
            indexes = df[df['Unique_Values'].str.startswith(string)].index
            splitting = j[0].split()
            length = len(splitting)

            if length == 1 and splitting[0] == string:
                #                print(i,j,">>>>>Here is I<<<<<<<")
                column = [val for val in index_ranges if indexes[i] in index_ranges[val]]
                #                print("Exact Match : {} , column : {}, column index : {} ".format(df["Unique_Values"][indexes[i]],column,indexes[i]))
                iv.append(indexes[i])
                col.append(column[0])
                break
            elif splitting[0] == string:
                take = splitted_query[index_:index_ + length]
                #                splitted_query =[change for change in range]
                if splitting == take:
                    #                    for change in range(index_,index_+length):
                    #                        splitted_query[change] = ''
                    #                    print(take,splitted_query[index_:index_+length],">>>>>Here is I<<<<<<<",[index_,index_+length])
                    column = [val for val in index_ranges if indexes[i] in index_ranges[val]]

                    #                    print("Exact Match : {} ,column : {}, column index : {}".format(df["Unique_Values"][indexes[i]],column,indexes[i]))
                    iv.append(indexes[i])
                    col.append(column[0])
                    break

    return iv, col, position


def find_actual_values(df, index_values, columns):
    values = [df['Unique_Values'][iv] for iv in index_values]
    return values, columns


def connect_startswith_unique_df(query, unique_df):
    query = query.lower()
    query = query.split()
    get_vals = get_startswith(query, unique_df[0], unique_df[1])
    return find_actual_values(unique_df[1], get_vals[0], get_vals[1])


def final_json(query,unique_df,main_df,param):
    got = connect_startswith_unique_df(query,unique_df)
    values = got[0]
    cnames = got[1]
    if param == 'mail':
        ids = []
        for i,j in enumerate(values):
            ids.extend(list(main_df[main_df[cnames[i]] == j]['Mail_ID'].values))
    #    auto_report(','.join(ids))
        if ids != []:
            return [{"recepients" : ids}]
        else:
            return []

    elif param == 'deepinsights':
        return values
    #final_format = formatizer(got)


def entity_extraction_rules(intent, user_input):
    udf = simple_uv(dff)
    udf_column = simple_uv(cdf)
    entities = []
    if intent == 'deepinsights':
        print('yes')
        gott = final_json(user_input, udf_column, cdf, intent)
        print(gott)
        entities.extend(gott)
    elif intent == 'mail':
        entities.extend(final_json(user_input, udf, dff, intent))
    entities.extend(test(user_input=user_input))
    return entities

# udf = simple_uv(dff)
# st = "share it with dmx and dsci team"
# print(final_json(st,udf,dff))
#
# data = ["what is the weather at [chennai](location) [today](day_time)?",
# "will it rain at [poland](location)",
# "Is there a possibility to rain at [madras](location) in [Tuesday](day_time)?",
# "what is the weather at [india](location)?",
# "Tell me the weather in [chennai](location) for [next 5 days](day_time)",
# "weather in [chennai](location) on [Wednesday](day_time)",
# "weather at [mumbai](location)?",
# "tell me the weather at [bangalore](location) [this wednesday](day_time).",
# "how is the weather at [trichy](location)?",
# "weather at [pune](location) on [Monday](day_time)?",
# "what is the weather at [hydrebad](location)?",
# "what is the weather in [mumbai](location)?",
# "will it rain at [germany](location)",
# "Is there a possibility to rain at [delhi](location)",
# "what is the weather at [west bengal](location)?",
# "weather at [kolkata](location)?",
# "tell me the weather at [chennai](location) in [monday](day_time).",
# "how is the weather at [trichy](location)?",
# "weather at [goa](location)?",
# "Will it rain [tomorrow](day_time) morning at [alabama](location)?",
# "weather at [Kannur](location) for [next 3 days](day_time)?",
# "tell me about the weather in [boston](location) [tomorrow](day_time)",
# "weather in [kannur](location)?",
# "what is the weather at [Pakistan](location)?",
# "what is the temperature at [kolathur](location)",
# "humidity at [nungambakkam](location) for [next 2 days](day_time)",
# "what is weather [kolathur](location)",
# "weather at [delhi](location)?",
# "weather at [chennai](location) for [next Thrusday](day_time)",
# "weather at [chennai](location) in [coming Friday](day_time)?",
# "weather at [kerala](location)?",
# "What is the weather in Kannur?",
# "tell me about the weather at [boston](location)",
# "what's the weather in [pollachi](location)?",
# "weather at [chennai](location)?",
# "what’s the weather in [Chennai](location) [tomorrow](day_time)??",
# "what’s the weather now in [perambur](location)??",
# "what will be the weather in [Chennai](location) on [Thursday](day_time)??",
# "What's the weather in [pondicherry](location) [this day_time](day_time)?",
# "Is it snowing in [Kashmir](location) [today](day_time)??",
# "Is it going to rain in [kerala](location) [tonight](day_time)?",
# "Is there any history of snowfall in [chennai](location)?",
# "Do I need an umbrella [today](day_time)??",
# "Do I need a Jacket for my [Bangalore](location) trip [day after tomorrow](day_time)?",
# "Tell me about the weather for [my pin location](location)??",
# "[Cities](location) with high temperature [today](day_time)??",
# "[Delhi](location) temperature [this Friday](day_time)??",
# "Temperature [here](location) now?",
# "Current weather??",
# "What is the season called in [chennai](location) now?",
# "Is there any chance of tornadoes at [america](location) [this sunday](day_time)?",
# "Which day of [this week](day_time) will be the warmest in [chennai](location)?",
# "Will [chennai](location) receives rain with thunderstorm [day after tomorrow](day_time)?",
# "Do any precipitation expected in [kerala](location) [this month](day_time)?",
# "[Chennai](location) forecast?",
# "what is weather at [chennai](location)",
# "[Delhi](location) temperature [this Friday](day_time)",
# "Delhi temperature [this Friday](day_time)",
# "will it rain in [trichy](location) [today](day_time)?",
# "do i need an umbrella [today](day_time)?",
# "do i need umbrella [tomorrow](day_time)?",
# "weather at [egmore](location) in [monday](day_time)",
# "tell me about the weather at [mumbai](location) on [sunday](day_time)",
# "what will be the weather",
# "weather at [chennai](location) for [next 3 days](day_time)",
# "weather at [chennai](location) [tomorrow](day_time)",
# "weather at [chennai](location) [today](day_time)",
# "weather at [chennai](location) [today](day_time)",
# "what's the weather at [chennai](location) for [next 2 days](day_time)"]
#
# print(train_entity(data))
# print(test(user_input='weather at chennai today and tomorrow'))