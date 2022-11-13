#! /usr/bin/env python

etymon = []
dic = []
codeset = []

# query components(be queried)
def fname(arg):
    for x in range(len(etymon)):
        z = etymon[x][0]
        if z == arg:
            return etymon[x][1]

def code(arg):
        for index in range(len(arg)):
            x = arg[0:index + 2]
            if (index == 5):
                shortcode = x 
                break
            elif (x in codeset):
                pass
            else:
                codeset.append(x)
                shortcode = x 
                break
        return shortcode

# read components mapping
for line in open('yi_components_mapping.txt',"r",encoding='utf-8'):
    l = line.split('\t')
    # l -> components, keyboard key
    l[1] = l[1][0:-1]
    etymon.append([l[0],l[1]])

# read spelling
for line in open('yi_spelling.txt',"r",encoding='utf-8'):
    l = line.split('\t')
    # l -> character，spelling
    l[1] = l[1][0:-1]
    dic.append([l[0],l[1]])

# deal
for i in range(len(dic)):
    s = ''
    for j in range(len(dic[i][1])):
        ch = dic[i][1][j]
        s=s+fname(ch);
    dic[i][1] = s

# write code file
fullcode_file = open("yi_fullcode_table.txt","w",encoding='utf-8')
table_file = open("yi_table.txt","w",encoding='utf-8')
for i in dic:
    character=i[0]
    fullcode=i[1]
    shortcode = code(fullcode);
    fullcode_file.write(character+"\t"+ fullcode +"\n")
    table_file.write(character+"\t"+ shortcode +"\n")

print("write fullcode to 'yi_fullcode_table.txt'")
print("write table to 'yi_table.txt'")