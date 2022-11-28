#! /usr/bin/env python

etymon = []
dic = []
shortcode = []

# query components(be queried)
def fname(arg):
    for x in range(len(etymon)):
        z = etymon[x][0]
        if z == arg:
            return etymon[x][1]

def scode(code, index):
    currentCode = code[0:index]
    if currentCode in shortcode and index <=6:
        return scode(code,index+1)
    else:
        shortcode.append(currentCode)
        return currentCode

def translatesCode():
    dicCount = len(dic)
    for i in range(dicCount):
        s = ''
        for j in range(len(dic[i][1])):
            ch = dic[i][1][j]
            s=s+fname(ch)
        dic[i][1] = s

def readTable(path):
    try:
        readContent = []
        for line in open(path, 'r', encoding='utf-8'):
            l = line.split('\t')
            # l -> components, keyboard key
            l[1] = l[1][0:-1]
            readContent.append([l[0],l[1]])
        return readContent
    except Exception:
        print(Exception)

def writeFullTable(path):
    table_file = open(path, "w", encoding='utf-8')
    for i in dic:
        character = i[0]
        code = i[1]
        table_file.write(character+"\t"+ code +"\n")

    table_file.close()


def writeShortTable(path):
    table_file = open(path, "w", encoding='utf-8')
    for i in dic:
        character = i[0]
        code = i[1]
        code = scode(code,2)
        table_file.write(character+"\t"+ code +"\n")

    table_file.close()


if __name__ == '__main__':
    # read components mapping
    etymon = readTable('yi_components_mapping.txt')

    # read spelling
    dic = readTable('yi_spelling.txt')

    # spelling translates code
    translatesCode()

    # write codeTable
    fullCodeTablePath = "yi_fullcode_table.txt" 
    writeFullTable(fullCodeTablePath)
    print("write fullcode to " + fullCodeTablePath)

    # write ShortCodeTable
    shortCodeTablePath = "yi_table.txt"
    writeShortTable(shortCodeTablePath)
    print("write table to " + shortCodeTablePath)