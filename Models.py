from math import inf
from math import log
class nGrams(object):

    def __init__(self):
        self.value = {}
        pass

    def NGram(self, dictionary, poem, nGram):
        Number_of_Ngrams = len(poem)-nGram+1

        for position in range(Number_of_Ngrams):
            words = []
            for nWord in range(nGram):
                words = words + [poem[nWord+position]]
            temp_dic = dictionary

            for nWord in range(nGram):
                current_word = words[nWord]
                last_word = nWord+1==nGram
                if(current_word in temp_dic):
                    if(last_word):
                        temp_dic[current_word] = temp_dic[current_word]+1 #Increase the Ngram Count by 1
                    else:
                        temp_dic = temp_dic[current_word]
                else:
                    create_dic = 0
                    if(last_word):
                        create_dic = 1
                    else:
                        create_dic = {words[-1]:1}

                    for k in range(nGram-2,nWord,-1):
                        create_dic = {words[k]:create_dic}
                    temp_dic[current_word] = create_dic
                    break
        self.value = dictionary
        return(dictionary)

    def BiGram(dic, poem):
        a = poem
        b = poem[1:]
        for i in range(len(b)):
            if(a[i] in dic):
                if(b[i] in dic[a[i]]):
                    dic[a[i]][b[i]] = dic[a[i]][b[i]]+1
                else:
                    dic[a[i]][b[i]] = 1
            else:
                dic[a[i]]={b[i]:1}

        return(dic)

    def TriGram(dic, poem):
        a = poem
        b = poem[1:]
        c = poem[2:]
        for i in range(len(c)):
            if(a[i] in dic):
                if(b[i] in dic[a[i]]):
                    #print(dic)
                    #print(c[i])
                    if(c[i] in (dic[a[i]])[b[i]]):

                        ((dic[a[i]])[b[i]])[c[i]] = dic[a[i]][b[i]][c[i]]+1
                    else:
                        dic[a[i]][b[i]][c[i]] = 1
                else:
                    dic[a[i]][b[i]] = {c[i]:1}
            else:
                dic[a[i]]={b[i]:{c[i]:1}}


        return(dic)

    def next_word(words, dic, nGram):
        Max = 0
        next_word = ""
        dictionary = dic
        for word in words:
            dictionary = dictionary[word]

        for i,j in list(dictionary.items()):
            if(j>Max):
                Max = j
                next_word = i
        return(next_word)

    def next_word_prob(words, dic, nGram, a=0.1):
        Max = -inf
        next_word = ""
        dictionary = dic
        for word in words:
            dictionary = dictionary[word]

        #print((list(dictionary.values())[0]))

        if(not (((list(dictionary.values())[0])<1)) ):
            total_counts = 0
            for i,j in list(dictionary.items()):
                total_counts = total_counts+j
            #print(total_counts)
            items = list(dictionary.items())
            alpha = a*total_counts
            for i,j in items:
                dictionary[i] = ((j+alpha)/(total_counts + alpha*len(items)))

        for i,j in list(dictionary.items()):
            if(j>Max):
                Max = j
                next_word = i
        return(next_word, Max)
