from math import inf
from math import log
class nGrams(object):
    def __init__(self, data_set, nGram, alpha = 0.15):
        self.n = nGram
        self.model = {}
        for poem in data_set:
            self.model = self.__NGram(self.model, poem, self.n)
        self.alpha = alpha

    def __NGram(self, dictionary, poem, nGram):
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

    def next_word2(self, words):
        Max = 0
        next_word = ""
        dictionary = self.model
        for word in words:
            dictionary = dictionary[word]

        for i,j in list(dictionary.items()):
            if(j>Max):
                Max = j
                next_word = i
        return(next_word)

    def next_word(self, words, return_prob = False):
        a = self.alpha
        Max = -inf
        next_word = ""
        dictionary = self.model
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
        if(return_prob==True):
            return(next_word, Max)
        else:
            return(next_word)


def nextSyllableWord(words, words_nGram, syllable_nGram, syllable_dic, n):
    syllables = [syllable_dic[word] for word in words]

    wordsDic = words_nGram.model
    syllaDic = syllable_nGram.model

    words_nGram.next_word(words)
    syllable_nGram.next_word(syllables)

    for word in words:
        wordsDic = wordsDic[word]
    for syllable in syllables:
        syllaDic = syllaDic[syllable]

    Max = 0
    next_word = "Error"
    #print(words)

    for word,probablity_word in list(wordsDic.items()):

        final_prob = 0
        if(word in syllable_dic):
            word_syllable_count = syllable_dic[word]
            final_prob = probablity_word * syllaDic[word_syllable_count]

        #print(word,probablity_word,syllaDic[word_syllable_count], final_prob)
        if(final_prob>Max):
            Max = final_prob
            next_word = word
    return(next_word)

def nextPOSWord(words, POS_tags_of_words, words_nGram, POS_nGram, POS_dic_words, alpha = 0):
    wordsDic    = words_nGram.model
    POS_Ngram   = POS_nGram.model

    words_nGram.next_word(words)
    POS_nGram.next_word(POS_tags_of_words)

    for word in words:
        wordsDic = wordsDic[word]

    for POS_tag in POS_tags_of_words:
        POS_Ngram = POS_Ngram[POS_tag]

    Max = 0
    next_word = "Error"
    next_tag  = "Error2"
    for word,probablity_word in list(wordsDic.items()):
        POS_prob(word.lower(), POS_dic_words, alpha)
        word_POS_p = list(POS_dic_words[word.lower()].items())
        for tag, prob_tag_given_word in word_POS_p:
            final_prob = 0
            if(tag in POS_Ngram):
                prob_tag_for_tag_sequence = POS_Ngram[tag]
                final_prob = probablity_word * prob_tag_given_word*prob_tag_for_tag_sequence

            if(final_prob>Max):
                Max = final_prob
                next_word = word
                next_tag  = tag
    #print(next_word, Max)
    return(next_word, next_tag)

def POS_prob(word, dic, a = 0.2):
    counts_dic = dic[word]

    if(not (((list(counts_dic.values())[0])<1)) ):
        total_counts = 0
        for POS_tag,Count in list(counts_dic.items()):
            total_counts = total_counts+Count

        items = list(counts_dic.items())
        alpha = a*total_counts
        for POS_tag,Count in items:
            counts_dic[POS_tag] = ((Count+alpha)/(total_counts + alpha*len(items)))


def nextPOSWordSyllable(words, POS_tags_of_words, words_nGram, POS_nGram, syllable_nGram, POS_dic_words,syllable_dic, alpha = 0):
    syllables = [syllable_dic[word] for word in words]

    wordsDic    = words_nGram.model
    POS_Ngram   = POS_nGram.model
    syllaDic    = syllable_nGram.model

    words_nGram.next_word(words)
    POS_nGram.next_word(POS_tags_of_words)
    syllable_nGram.next_word(syllables)

    for word in words:
        wordsDic = wordsDic[word]
    for POS_tag in POS_tags_of_words:
        POS_Ngram = POS_Ngram[POS_tag]
    for syllable in syllables:
        syllaDic = syllaDic[syllable]

    Max = 0
    next_word = "Error"
    next_tag  = "Error2"
    for word,probablity_word in list(wordsDic.items()):
        POS_prob(word.lower(), POS_dic_words, alpha)
        word_POS_p = list(POS_dic_words[word.lower()].items())
        for tag, prob_tag_given_word in word_POS_p:
            final_prob = 0
            if(tag in POS_Ngram):
                prob_tag_for_tag_sequence = POS_Ngram[tag]
                final_prob = probablity_word * prob_tag_given_word*prob_tag_for_tag_sequence
            if(word in syllable_dic):
                word_syllable_count = syllable_dic[word]
                final_prob = final_prob * syllaDic[word_syllable_count]

            if(final_prob>Max):
                Max = final_prob
                next_word = word
                next_tag  = tag
    #print(next_word, Max)
    return(next_word, next_tag)
