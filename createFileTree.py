import os, cv2, sys
import numpy as np
import hashlib
import pandas as pd
from LinkTable import LinkList
#计算图片的dHash值
def dHashFunc(picpath):
    stream = open(picpath.encode(sys.getfilesystemencoding()),'rb')  #文件路径中含中文的处理方法，但是对有的图片不成功
    bytes = bytearray(stream.read())
    picarray = np.asarray(bytes, dtype=np.uint8)
    img_src=cv2.imdecode(picarray, cv2.IMREAD_UNCHANGED)                 # 原图
    width = 9
    height = 8
    img_resized = cv2.resize(img_src, (width, height))    #调整到9x8，宽x高
    convertGray = np.array([0.11,0.59,0.3],dtype='float32')
    img_gray = np.inner(img_resized,convertGray) # 转灰度图
    img_diff = np.zeros((8,8),dtype=np.float32)
    # 计算差异值，左边的像素值减右边
    for idx in range(width-1):
        img_diff[:,idx] = img_gray[:,idx]-img_gray[:,idx+1]
    finger=np.zeros((8,8), dtype=np.int32)
    # 左边的像素比右边亮，记1
    finger[img_diff>0] = 1
    finger=finger.reshape(1,64)
    #得到信息指纹
    fingerHex=''
    for idx in range(0,64,4):
        temp = finger[0,idx:idx+4]
        shijinzhi = temp[0]*8+temp[1]*4+temp[2]*2+temp[3]*1
        shiliujinzhi = '{:x}'.format(shijinzhi)
        fingerHex = fingerHex+shiliujinzhi
    return fingerHex
#求文件的MD5值
def MD5HashFunc(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hashHex = md5obj.hexdigest()
        # 改良的哈希值，为了和dHash的长度一致，采用128bit高64位和低64位按位模二和，得到64比特的哈希值字符串
        # hash64 = int(hashHex,16)              #python的int型数据做了优化，可以支持任意范围而不会溢出
        # a = hash64 >> 64
        # b = hash64 & 0xFFFFFFFFFFFFFFFF
        # hashHex = hex(a^b)[2:]
        return hashHex

def isPicture(filepath):
    status = os.path.splitext(filepath)[-1]     #取文件名中的扩展名
    if status.lower() in ['.jpg','.png','.tiff','.bmp','.jpeg','.gif']:
        return True
    else:
        return False


if __name__ == '__main__':
    infolist = []
    rootpath = "E:\\资料\\大二下资料"   #要扫描的文件夹路径
    if os.path.exists('fileInfo.csv'):
        os.remove('fileInfo.csv')
    for root, dirs, files in os.walk(rootpath,topdown=True):
        print('当前搜索目录：{0}'.format(root))
        for filename in files:          #对当前目录下的文件求MD5，结果放入列表infolist
            filepath = os.path.join(root, filename)
            HashValue = MD5HashFunc(filepath)
            infolist.append([filename, filepath, HashValue])
        if root == rootpath:    #如果当前在根目录，代表搜索一开始
            # list转dataframe
            df = pd.DataFrame(infolist,columns=['filename','location','hash value'])
            # 保存到本地excel，存储时加上表头。由于后续分文件夹存储结果，索引值不好算且无意义，不加索引
            df.to_csv("fileInfo.csv", mode='a',index=False,encoding='gbk',header=True) #mode='a'代表在文件末尾追加
            infolist = []
        else:
            # list转dataframe
            df = pd.DataFrame(infolist)
            # 保存到本地excel
            df.to_csv("fileInfo.csv", mode='a', index=False, encoding='gbk', header=False)
            infolist = []
    # if len(infolist) > 0 :
    #     # list转dataframe
    #     df = pd.DataFrame(infolist)#, columns=['filename', 'location', 'hash value'])
    #     # 保存到本地excel
    #     df.to_csv("fileInfo.csv", mode='a', index=False, encoding='gbk',header=False)
    #     infolist = []