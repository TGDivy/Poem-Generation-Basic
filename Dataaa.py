import pandas as pd
import nltk

def PoetryFoundationRaw():
    data = pd.read_csv("G:\OneDrive - University of Edinburgh\Poem Generation\WebScrapping-PoetryFoundation\PoetryFoundationData.csv")
    data = data.drop(columns=["Unnamed: 0"])
    return(data)

def clean_texts(string):
    string  = str(string).upper()
    string  = string.replace("-", " ")
    string  = string.replace("—", " ")
    string  = string.replace(".", " . ")
    return str(string).replace("\r\r\n"," NEWLINE\n ")

def PoetryFoundationPoems():
    data = PoetryFoundationRaw()
    data = data.applymap(clean_texts)
    poems = data.Poem.map(lambda x: nltk.tokenize.word_tokenize(x,preserve_line =True))
    #For Faster Testing
    poem_sample = poems[:2000]
    return(poems)

def number_of_syllables(string):
    count = 0
    for ch in string:
        if(ch in "012"):
            count=count+1
    return(count)

def syllables_count(string, vowels):
    l = str(string).split(" ")
    count = 0
    for a in l:
        if(a in vowels):
            count+=1
    return count

def Syllable_database():
    syllables = pd.read_csv("Syllable dict.txt","  ", engine="python")
    syllables = syllables.rename(columns = {"A":"words","AH0":"syllable_count"})
    syllables.syllable_count = (syllables.syllable_count.map(number_of_syllables))
    syllable_dict = dict([(word, syllable)for word,syllable in zip(syllables.words,syllables.syllable_count)])
    syllable_dict["A"] = 1
    syllable_dict["NEWLINE"] = "NEWLINE"
    syllable_dict[","] = "punc"
    syllable_dict["."] = "punc"
    dict1 = pd.read_csv("dict1.txt","\t", engine="python")
    dict1 = dict1.rename(columns={"SCYTHING":"words","S IH DH AH NG":"syllable_count"})
    dict2 = pd.read_csv("dict2.txt","\t", engine="python")
    dict2 = dict2.rename(columns={"TREATERS/":"words","T R IY T ER Z":"syllable_count"})
    dict3 = pd.read_csv("dict3.txt","\t", engine="python")
    dict3 = dict3.rename(columns={"NOMMO":"words","N AA M OW":"syllable_count"})
    dict4 = pd.read_csv("dict4.txt","\t", engine="python")
    dict4 = dict4.rename(columns={"UNINFORMD":"words","Y UW N AH N F AO R M D":"syllable_count"})

    dictionary = ((dict1.append(dict2)).append(dict3)).append(dict4)

    phones = pd.read_csv("phones.txt","\t", engine="python")
    phones = phones.rename(columns={"AA":"symbol","vowel":"meaning"})
    phones = phones[phones["meaning"]=="vowel"]
    vowels = list(phones.symbol)
    vowels = vowels + ["AA"]

    dictionary.syllable_count = dictionary.syllable_count.map(lambda x: syllables_count(x,vowels))

    dict_database = syllables.append(dictionary)
    return dict_database

def SyllablesDict():
    dict_database = Syllable_database()
    syllable_dict = dict([(word, syllable)for word,syllable in zip(dict_database.words,dict_database.syllable_count)])
    #Some other basic additions to it manually
    syllable_dict["A"] = 1
    syllable_dict["NEWLINE"] = "NEWLINE"
    syllable_dict[","] = "punc"
    syllable_dict["."] = "punc"

    return(syllable_dict)

def syllables_poem(poem, untagged, syllable_dict):
    syllable_poem = []
    for token in poem:
        if(token in syllable_dict):
            tag = syllable_dict[token]
            syllable_poem = syllable_poem + [tag]
        else:
            untagged += [token]
    return(syllable_poem, untagged)

def PoemOfSyllables(poems):
    untagged = []
    syllable_poems = []
    syllable_dict = SyllablesDict()
    for i in poems:
        temp,untagged = syllables_poem(i,untagged, syllable_dict)
        syllable_poems = syllable_poems+[temp]
    return(syllable_poems)

def Poem_inDict(poem, untagged, syllable_dict):
    syllable_poem = []
    for token in poem:
        if(token in syllable_dict):
            syllable_poem = syllable_poem + [token]
        else:
            untagged += [token]
    return(syllable_poem, untagged)
def Poem_words_dict(poems):
    untagged = []
    syllable_poems = []
    syllable_dict = SyllablesDict()
    for i in poems:
        temp,untagged = Poem_inDict(i,untagged, syllable_dict)
        syllable_poems = syllable_poems+[temp]
    return(syllable_poems)

def words_by_syllables():
    dict_database = Syllable_database()
    dictSyllable = {}
    for i in dict_database.syllable_count.unique():
        dictSyllable[i] = list((dict_database[dict_database.syllable_count ==i]).words)
    return(dictSyllable)
