from sklearn import svm
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from pickle import dump, load


def intent_classify(dataset):
    vectorizer = CountVectorizer(ngram_range=(1, 1))
    vectorizer.fit(dataset['text'])
    X = vectorizer.transform(dataset['text'])
    le = LabelEncoder()
    le.fit(dataset['intent'])
    labels = le.transform(dataset['intent'])

    x_train, x_test, y_train, y_test = train_test_split(X, labels)
    svc = svm.SVC(kernel='linear', C=1,gamma=0.1, probability=True).fit(x_train, y_train)

    ypred = svc.predict(x_test)
    from sklearn.metrics import accuracy_score
    print(accuracy_score(y_test, ypred))

    dump(le, open('label_encoding.pkl', 'wb'))
    dump(vectorizer, open('featurizer.pkl', 'wb'))
    dump(svc, open('model.pkl', 'wb'))


def test_input(user_input):
    svc = load(open('nlu/model.pkl', 'rb'))
    vectorizer = load(open('nlu/featurizer.pkl', 'rb'))
    le = load(open('nlu/label_encoding.pkl', 'rb'))
    x_ = vectorizer.transform([user_input])
    results = svc.predict_proba(x_)[0]
    intent = le.inverse_transform(svc.predict(x_))[0]
    # gets a list of ['most_probable_class', 'second_most_probable_class', ..., 'least_class']
    results_ordered_by_probability = list(
        map(lambda x: x[0], sorted(zip(svc.classes_, results), key=lambda x: x[1], reverse=True)))
    temp = dict(zip(results_ordered_by_probability, results))
    confidence = {}
    for k, v in list(temp.items()):
        each_val = {le.inverse_transform([k])[0]: v * 100}
        confidence.update(each_val)
    return intent, confidence

