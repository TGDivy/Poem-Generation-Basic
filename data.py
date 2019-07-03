import pandas as pd
import nltk

class Poems():
    def __init__(self, poems_data_location, syllable_dict_location = "syllable_dict.txt", updated_syllable_dict = "new_words_syllables.csv"):
        self.data_location = poems_data_location
        self.poems = self.__PoetryFoundationPoems()
        print("self.poems is ready!")
        self.word_syllablecount_dict = self.__SyllablesDict(syllable_dict_location, updated_syllable_dict)
        print("self.word_syllablecount_dict is ready!")
        self.poems_of_syllables = self.__PoemOfSyllables()
        print("self.poems_of_syllables is ready!")
        self.poems = self.__Poem_words_dict()
        print("self.poems is updated!")
        self.poems_of_POStags, self.word_POStag_dict = self.__poem_of_tags()
        print("self.poems_of_POStags and self.word_POStag_dict are ready!")

    def __PoetryFoundationRaw(self):
        data = pd.read_csv(self.data_location)
        data = data.drop(columns=["Unnamed: 0"])
        return(data)

    def __clean_texts(self, string):
        string  = str(string).upper()
        string  = string.replace("-", " ")
        string  = string.replace("—", " ")
        string  = string.replace(".", " . ")
        return str(string).replace("\r\r\n"," NEWLINE\n ")

    def __PoetryFoundationPoems(self):
        data = self.__PoetryFoundationRaw()
        data = data.applymap(self.__clean_texts)
        poems = data.Poem.map(lambda x: nltk.tokenize.word_tokenize(x,preserve_line =True))
        #For Faster Testing
        poem_sample = poems[:2000]
        return(poems)

    def __number_of_syllables(self, string):
        count = 0
        for ch in string:
            if(ch in "012"):
                count=count+1
        return(count)

    def __syllables_count(self, string, vowels):
        l = str(string).split(" ")
        count = 0
        for a in l:
            if(a in vowels):
                count+=1
        return count

    def __Syllable_database(self, syllable_dict_location, updated_syllable_dict):
        syllables = pd.read_csv(syllable_dict_location,"  ", engine="python")
        syllables = syllables.rename(columns = {"A":"words","AH0":"syllable_count"})
        syllables.syllable_count = (syllables.syllable_count.map(self.__number_of_syllables))

        dictionary = pd.read_csv(updated_syllable_dict, engine="python")

        phones = pd.read_csv("phones.txt","\t", engine="python")
        phones = phones.rename(columns={"AA":"symbol","vowel":"meaning"})
        phones = phones[phones["meaning"]=="vowel"]
        vowels = list(phones.symbol)
        vowels = vowels + ["AA"]

        dictionary.syllable_count = dictionary.syllable_count.map(lambda x: self.__syllables_count(x,vowels))

        dict_database = syllables.append(dictionary)
        return dict_database

    def __SyllablesDict(self, syllable_dict_location, updated_syllable_dict):
        dict_database = self.__Syllable_database(syllable_dict_location, updated_syllable_dict)
        syllable_dict = dict([(word, syllable)for word,syllable in zip(dict_database.words,dict_database.syllable_count)])
        #Some other basic additions to it manually
        syllable_dict["A"] = 1
        syllable_dict["NEWLINE"] = "NEWLINE"
        syllable_dict[","] = "punc"
        syllable_dict["."] = "punc"
        syllable_dict["?"] = "punc"
        syllable_dict[":"] = "punc"

        return(syllable_dict)

    def __syllables_poem(self, poem, untagged, syllable_dict):
        syllable_poem = []
        for token in poem:
            if(token in syllable_dict):
                tag = syllable_dict[token]
                syllable_poem = syllable_poem + [tag]
            else:
                untagged += [token]
        return(syllable_poem, untagged)

    def __PoemOfSyllables(self):
        untagged = []
        syllable_poems = []
        syllable_dict = self.word_syllablecount_dict
        poems = self.poems
        for i in poems:
            temp,untagged = self.__syllables_poem(i,untagged, syllable_dict)
            syllable_poems = syllable_poems+[temp]
        return(syllable_poems)

    def __Poem_inDict(self, poem, untagged, syllable_dict):
        syllable_poem = []
        for token in poem:
            if(token in syllable_dict):
                syllable_poem = syllable_poem + [token]
            else:
                untagged += [token]
        return(syllable_poem, untagged)
    def __Poem_words_dict(self):
        poems = self.poems
        untagged = []
        syllable_poems = []
        syllable_dict = self.word_syllablecount_dict
        for i in poems:
            temp,untagged = self.__Poem_inDict(i,untagged, syllable_dict)
            syllable_poems = syllable_poems+[temp]
        return(syllable_poems)

    def __word_pos_tags(self, dic, poems_tagged):
        for word, tag in poems_tagged:
            if(word in dic):
                if(tag in dic[word]):
                    dic[word][tag] = dic[word][tag]+1
                else:
                    dic[word][tag] = 1
            else:
                dic[word] = {tag:1}
        return dic

    def __tag_pos(self, poem, dic):
        poem = [w.lower() for w in poem]
        nltk_tags = nltk.pos_tag(poem)
        modify_tags = []
        only_tags = []
        for word,tag in nltk_tags:
            if(word == "newline"):
                modify_tags = modify_tags + [(word,"NEWLINE")]
                only_tags = only_tags + ["NEWLINE"]
            else:
                modify_tags = modify_tags + [(word,tag)]
                only_tags = only_tags + [tag]

        dic = self.__word_pos_tags(dic, modify_tags)
        #print(modify_tags)
        #print()
        return(only_tags, dic)

    def __poem_of_tags(self):
        poems_of_tags = []
        pos_dicts = {}
        for p in self.poems:
            poem_tagged, pos_dicts = self.__tag_pos(p, pos_dicts)
            poems_of_tags = poems_of_tags + [poem_tagged]
            #print(pos_dicts)
        return(poems_of_tags, pos_dicts)
