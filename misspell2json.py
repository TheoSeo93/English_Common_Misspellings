import re
import json
'''
    Commonly Misspelled English words stored into json.
    Corpora attained from Roger Milton's hompage
    https://www.dcs.bbk.ac.uk/~ROGER/corpora.html
'''
pattern = re.compile(r'\<ERR(.*?)\</ERR>')

# Birbeck misspellings
birkbeck_file = open('./data/missp.dat.txt', 'r')
birkbeck_data = birkbeck_file.readlines()

# Holbrook misspellings
holbrook_file = open('./data/holbrook-tagged.dat.txt')
holbrook_data = holbrook_file.readlines()


# Aspell misspellings
aspell_file = open('./data/aspell.dat.txt')
aspell_data = aspell_file.readlines()

# Wikipedia misspellings
wikipedia_file = open('./data/wikipedia.dat.txt')
wikipedia_data = wikipedia_file.readlines()

misspell_dic = {}

def store_misspellings(data, misspell_dic):
    word = ''
    for l in data:
        if '$' in l:
            word = l.replace('$', '').strip()
            misspell_dic[word] = list()
        else:
            mis_spell = l.strip()
            if mis_spell not in misspell_dic[word]:
                misspell_dic[word].append(mis_spell)


for l in holbrook_data:
    for match in pattern.finditer(l):
        split = match.groups()[0].split('> ')
        word = split[0].replace('targ=','').strip()
        misspell = split[1].strip()

        if word in misspell_dic:
            misspell_dic[word].append(misspell)
        else:
            misspell_dic[word] = list()
            if misspell not in misspell_dic[word]:
                misspell_dic[word].append(misspell)

store_misspellings(birkbeck_data, misspell_dic)
store_misspellings(aspell_data, misspell_dic)
store_misspellings(wikipedia_data, misspell_dic)


# Serializing json
json_object = json.dumps(misspell_dic)
with open("data/output_json/misspell.json", "w") as outfile:
    json.dump(json_object, outfile)