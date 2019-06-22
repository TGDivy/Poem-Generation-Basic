import Models


ngram = Models.nGrams()

dic = {}
sentence = "What is all that about?".split(" ")

print(ngram.NGram(dic,sentence,2))
print()
#print(ngram.value)
