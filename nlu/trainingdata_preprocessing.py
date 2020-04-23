import nltk


def pre_process_for_entity_extraction(data):
    from pprint import pprint
    pprint(data)
    result = []
    for all_words in data:
        all_words = all_words.replace('?', '')
        got = []
        string = all_words
        string = string.replace('[', '!!**')
        string = string.replace(')', '!!')
        string = string.split('!!')
        print(string)
        # print(nltk.pos_tag(nltk.word_tokenize(string)))
        try:
            for i in string:
                print(i[0])
                if i[0] == '*' and i[1] == '*':
                    i = i[2:]
                    i = i.split('](')
                    got.append((i[0],i[1]))
                else:
                    for j in i.split():
                        print(j)
                        got.append((j,'O'))
        except IndexError:
            pass
        result.append(got)

    final_result = []
    for each_res in result:
      if each_res is not []:
        final_result.append(each_res)

    for each_sent in range(len(final_result)):
        temp = []
        for i in final_result[each_sent]:
            temp.append(i[0])
        print(temp)
        tag = nltk.pos_tag(temp)
        print(tag)
        if len(final_result[each_sent]) == 0:
            final_result[each_sent] = []
        elif len(tag) == len(final_result[each_sent]):
            print('yes')
            for i in range(len(tag)):
                temp_tuple = (final_result[each_sent][i][0], tag[i][1], final_result[each_sent][i][1])
                print(temp_tuple)
                final_result[each_sent][i] = temp_tuple
        print(final_result)

    return final_result
