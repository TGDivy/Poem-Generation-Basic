import pandas as pd
import nltk
import random
from Models import nGrams as n

def importData():
    data = pd.read_csv("G:\OneDrive - University of Edinburgh\Poem Generation\WebScrapping-PoetryFoundation\PoetryFoundationData.csv")
    data = data.drop(columns=["Unnamed: 0"])

    data = data.applymap(clean_text)
    data.Tags = data.Tags.map(split_tags)
    return(data)

def split_tags(string):
    return (str(string)).split(",")

def clean_text(string):
    string  = str(string).lower()
    return str(string).replace("\r\r\n","NEWLINE\n ")

def main():
    data = importData()

    Poems = data.Poem.map(lambda x: nltk.tokenize.word_tokenize(x,preserve_line =True))
    Poem_small = Poems[:2000]

    dicBi = {}
    for i in Poems:
        dicBi = n.BiGram(dicBi, i)

    dicTri = {}
    for i in Poems:
        dicTri = n.TriGram(dicTri, i)

    dic4 = {}
    for i in Poems:
        dic4 = n.NGram(dic4, i, 4)

    prev_word1 = "love"
    prev_word2 = n.next_word([prev_word1], dicBi, 2)
    prev_word3 = n.next_word([prev_word1,prev_word2], dicTri, 3)
    generate_str = prev_word1+" "+prev_word2 + " " +prev_word3

    for i in range(50):
        next_word = n.next_word([prev_word1, prev_word2,prev_word3], dic4, 4)
        prev_word1 = prev_word2
        prev_word2 = prev_word3
        prev_word3 = next_word
        generate_str = generate_str+" "+ next_word

    print(generate_str.replace("NEWLINE ","\n"))

if __name__ == '__main__':
    main()
