import pandas as pd
from LinkTable import LinkList, Node
#定义拉链表，8个段，每段16比特的从全0到全1
def initLinkTable():
    LinkTab = []
    for jj in range(0,8):
        Li = []
        for ii in range(0,pow(2,16)):
            L = LinkList()
            L.InsertNode(0,ii)  #链表的头是相应的段的值
            Li.insert(ii,L)
        LinkTab.insert(jj,Li)
    return LinkTab
#计算汉明重量
def HammingWeight(n):
    count = 0
    for j in range(0,128):
        if ((1<<j) & n) != 0:
            count+=1
    return count
#在数组0~65535位置存储每个数字的汉明重量
# def initHammingWeightTable():
#     HammingWeightTable = []
#     for ii in range(0,pow(2,16)):
#         HammingWeightTable.insert(ii,HammingWeight(ii))
#     return HammingWeightTable
#找出名字相同的文件
def findSameName(name,path):
    sameNameList = []
    for i in range(0,len(name)):
        for j in range(i,len(name)):
            if name[i] == name[j]:
                sameNameList.append([path[i],path[j]])
    if len(sameNameList) > 0:
        print("名字相同的文件：\n")
        for l in range(0,len(sameNameList)):
            print(sameNameList[l][1]+'  and  '+sameNameList[l][2])
    else:
        print("没有相同名字的文件.\n")



if __name__ == "__main__":
    df = pd.read_csv('fileInfo.csv', encoding='gbk')
    HashData = df['hash value']
    name = df['filename']
    path = df['location']
    HashTable = initLinkTable()
    # HammingWeightTable = initHammingWeightTable()
    #初始化hash散列表，把每个文件的路径和哈希值散列到每一段的对应拉链表
    for jj in range(0,len(HashData)):
        filepath = path[jj]
        HashValue = HashData[jj]
        for ii in range(7, -1, -1):
            H = int(HashValue, 16)
            temp = HashTable[ii][(H >> (16*ii)) & 0xFFFF]  #第ii段的拉链表，其实是引用
            temp.InsertNode(temp.GetLength(), [filepath, HashValue])#在链表末尾插入文件路径和哈希值的节点
    #找相同文件
    sameFileList = []
    for seg in range(7, -1, -1):
        for kk in range(0,pow(2,16)):
            aLinkList = HashTable[seg][kk]
            #链表第一个节点是数值，之后的节点是文件和哈希值，因此如果两个文件重复哈希值相同，拉链表有三个节点
            if aLinkList.GetLength() <= 2:
                continue
            #有文件重复，遍历链表的所有节点
            for k in range(1,aLinkList.GetLength()):
                Nodek = aLinkList.Get(k)
                Hashk = int(Nodek.GetData()[1],16)&~(0xFFFF<<(16*seg))  #取第k个节点哈希值除了这一段之外的其他比特，因为这一段相同无需重复比较
                for l in range(k+1,aLinkList.GetLength()):
                    Nodel = aLinkList.Get(l)
                    Hashl = int(Nodel.GetData()[1],16)&~(0xFFFF<<(16*seg)) #取第l个节点哈希值除了这一段之外其他比特
                    # 为了防止因为链表中先后顺序问题造成的文件重复，将已经找到的相同文件的路径对存入集合，消除顺序
                    fileNamePair = {Nodek.GetData()[0],Nodel.GetData()[0]}
                    if fileNamePair in sameFileList:
                        continue
                    #哈希值汉明距离小于等于7认为是同一文件，将路径对存入列表
                    if HammingWeight(Hashk^Hashl) <= 7:
                        sameFileList.append({Nodek.GetData()[0], Nodel.GetData()[0]})
    data = [list(PathPair) for PathPair in sameFileList]
    df = pd.DataFrame(data=data,index=range(1,len(data)+1),columns=['1','2'])
    df.to_csv('SameFile.csv',encoding='gbk',header=True)