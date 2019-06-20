#!/usr/bin/env python
# coding: utf-8

# In[511]:


import pandas as pd
import nltk
from collections import Counter


# ## Importing the dataset

# In[512]:


data = pd.read_csv("G:\OneDrive - University of Edinburgh\Poem Generation\WebScrapping-PoetryFoundation\PoetryFoundationData.csv")
data = data.drop(columns=["Unnamed: 0"])
data.head(5)


# ### Cleaning the Data Set

# Removing the unnecssary \r\r\n to just \n

# In[513]:


def clean_text(string):
    string  = str(string).lower()
    return str(string).replace("\r\r\n","NEWLINE\n ")

data = data.applymap(clean_text)


# Splitting the tags into lists as some poems have multiple tags!

# In[514]:


def split_tags(string):
    return (str(string)).split(",")

data.Tags = data.Tags.map(split_tags)
data[5:10]


# ## N-Gram model

# #### Tokenizing the poems

# In[515]:


Poems = data.Poem.map(lambda x: nltk.tokenize.word_tokenize(x,preserve_line =True))
#For Faster Testing
Poem_small = Poems[:2000]


# #### Getting word Bi-Grams

# The storage format for N-Grams is:
# Using a Dicitionary which contains all the unigrams as keys, whose values are all the words they have been before, making it the key-value as Bigram. 
# 
# For trigrams, It is Key containing another dictionary which contains Bigrams, making it a total of a trigram model!
# 
# This makes counting and finding values very easy!

# In[516]:


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


# Generating the Bigram's dictionary with counts

# In[539]:


dic = {}
for i in Poems:
    dic = BiGram(dic, i)


# The Next word method for Bigrams, i.e. given a previous word prediciting the next word

# In[518]:


def Next_word(word, dic):
    Max = 0
    next_word = ""
    for i,j in list(dic[word].items()):
        if(j>Max):
            Max = j
            next_word = i
    return(next_word)


# Generating a sentence from the Bigram Model!

# In[557]:


prev_word = "but"
generate_str = prev_word
for i in range(20):
    next_word = Next_word(prev_word, dic)
    prev_word = next_word
    generate_str = generate_str+" "+ next_word


# In[558]:


generate_str


# ### Generalizing to NGram Model

# In[ ]:





# In[559]:


def NGram(dictionary, poem, nGram):
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
    return(dictionary)


# In[560]:


dic4 = {}
for i in Poems:
    dic4 = NGram(dic4, i,4)


# In[561]:


def Next_word3(word1,word2,word3, dic):
    Max = 0
    next_word = ""
    for i,j in list(dic[word1][word2][word3].items()):
        if(j>Max):
            Max = j
            next_word = i
    return(next_word)
#Next_word3("NEWLINE","love","is",dic4)


# In[562]:


prev_word1 = "love"
prev_word2 = Next_word(prev_word1, dic)
prev_word3 = Next_word2(prev_word1,prev_word2, dic2)
generate_str = prev_word1+" "+prev_word2 + " " +prev_word3
for i in range(50):
    next_word = Next_word3(prev_word1, prev_word2,prev_word3, dic4)
    prev_word1 = prev_word2
    prev_word2 = prev_word3
    prev_word3 = next_word
    generate_str = generate_str+" "+ next_word
print(generate_str.replace("NEWLINE ","\n"))


# In[ ]:





# In[ ]:





# In[ ]:


dic3 = {}
sample = "this is why why why why i dont like is why".split(" ")
#for i in Poems[0][0:10]:
dic3 = NGram(dic3, sample,4)
dic3


# In[521]:


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


# In[522]:


dic2 = {}
for i in Poems:
    dic2 = TriGram(dic2, i)


# In[523]:


import random


# In[524]:


def Next_word2(word1,word2, dic):
    Max = 0
    next_word = ""
    for i,j in list(dic[word1][word2].items()):
        if(j>Max):
            Max = j
            next_word = i
    Max2 = 0 
    for i,j in list(dic[word1][word2].items()):
        if(j>Max2 and j<Max-random.randint(1,3)):
            Max2 = j
            next_word = i
    
    return(next_word)


# In[525]:


Next_word2("the","man",dic2)


# In[526]:


prev_word1 = "river"
prev_word2 = Next_word(prev_word1, dic)
generate_str = prev_word1+" "+prev_word2
for i in range(30):
    next_word = Next_word2(prev_word1, prev_word2, dic2)
    prev_word1 = prev_word2
    prev_word2 = next_word
    generate_str = generate_str+" "+ next_word
print(generate_str.replace("NEWLINE ","\n"))

