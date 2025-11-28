#! /usr/bin/env python

shortcode = []

# query components(be queried)
def fname(arg):
    for x in range(len(etymon)):
        z = etymon[x][0]
        if z == arg:
            return etymon[x][1]

def scode(code, index):
    # 注意：scode 的逻辑是基于 fullcode 的顺序来生成不重复的简码
    # 当 fullcode 经过字频排序后，这个函数就能保证高频字的简码长度更短（index 较小）
    currentCode = code[0:index]
    if currentCode in shortcode and index <=6:
        return scode(code,index+1)
    else:
        shortcode.append(currentCode)
        return currentCode

def translatesCode(dic, etymon):
    fullcode = []
    for item in dic:
        # item[0] 是字符，item[1] 是拼写组件序列
        s = ''.join([fname(ch) for ch in item[1]])
        new_item = [item[0], s] # [字符, 完整编码]
        fullcode.append(new_item)
    return fullcode

def readTable(path):
    try:
        readContent = []
        for line in open(path, 'r', encoding='utf-8'):
            l = line.split('\t')
            # l -> components, keyboard key
            # l[1] = l[1][0:-1] # 这一行似乎是旧代码，如果您的文件末尾没有换行符不需要这一行
            l[1] = l[1].strip() # 使用 strip() 清理末尾的换行符和空格更通用
            readContent.append([l[0],l[1]])
        return readContent
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return []

# 新增函数：读取字频表
def readCharFreq(path):
    # 返回一个字典，key是字符，value是频率排名（索引），越小频率越高
    char_rank = {}
    try:
        rank = 0
        for line in open(path, 'r', encoding='utf-8'):
            l = line.split('\t') # 使用 \t 分隔
            if l:
                character = l[0].strip() # 获取字符
                if character:
                    char_rank[character] = rank # rank 越小，频率越高
                    rank += 1
        return char_rank
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return {}


def writeFullTable(path):
    table_file = open(path, "w", encoding='utf-8')
    for i in fullcode:
        character = i[0]
        code = i[1]
        table_file.write(character+"\t"+ code +"\n")

    table_file.close()


def writeShortTable(path):
    table_file = open(path, "w", encoding='utf-8')
    # 由于 fullcode 已经按字频排序，此处生成的简码将优先分配给高频字
    for i in fullcode:
        character = i[0]
        code = i[1]
        # 从两位开始检查简码
        code = scode(code,2)
        table_file.write(character+"\t"+ code +"\n")

    table_file.close()

if __name__ == '__main__':
    # 确保 etymon 是全局可用的，或者在函数中作为参数传递
    # etymon 是 readTable('yi_components_mapping.txt') 的结果
    # fullcode 是 translatesCode 的结果
    
    # read components mapping
    etymon = readTable('yi_components_mapping.txt')

    # read spelling
    dic = readTable('yi_spelling.txt')

    # ========== 新增部分：读取字频并排序 ==========
    char_freq_path = 'char_freq.txt'
    char_rank_map = readCharFreq(char_freq_path)
    
    # 根据字频对拼写列表进行排序
    # 排序键：使用 char_rank_map 查找字符的排名。
    # 如果字符不在字频表中（get不到），则视为最低频率（排在最后）。
    # 排序后，dic 中的元素顺序变为：高频字在前，低频字在后。
    dic.sort(key=lambda item: char_rank_map.get(item[0], len(char_rank_map)))
    print("Dictionary sorted by character frequency.")
    # ============================================

    # spelling translates code
    # fullcode 的顺序现在也是按字频排列的
    fullcode = translatesCode(dic,etymon)

    # write codeTable
    fullCodeTablePath = "yi_fullcode_table_demo.txt" 
    writeFullTable(fullCodeTablePath)
    print("write fullcode to " + fullCodeTablePath)

    # write ShortCodeTable
    # scode 函数的简码生成现在将基于排序后的 fullcode
    shortCodeTablePath = "yi_table_demo.txt"
    writeShortTable(shortCodeTablePath)
    print("write table to " + shortCodeTablePath)