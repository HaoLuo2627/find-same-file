#定义节点类
class Node:
    def __init__(self, data=None, next=None):
        self._data=data
        self._next=next

    def GetData(self):
        return self._data

    def GetNext(self):
        return self._next

    def SetData(self, data):
        self._data = data

    def SetNext(self, next):
        self._next = next

#定义链表类
class LinkList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0
#判断链表是否为空
    def isEmpty(self):
        return (self._head is None)
#输出链表节点数
    def GetLength(self):
        return self._length
#查找链表索引为i的节点指针
    def Get(self, i):
        j=0
        if (i<0 or i>=self._length):
            raise ValueError('%s is not a legal index'%i)
        probe = self._head
        while probe.GetNext() is not None and j != i:
            probe = probe.GetNext()
            j+=1
        return probe
#析构函数
    def ClearList(self):
        probe = self._head
        while probe is not None:
            self._head = probe.GetNext()
            probe = self._head
            self._length-=1
        self._tail=None
#打印所有元素
    def PrintList(self):
        probe = self._head
        while probe is not None:
            print(str(probe.GetData())+' ')
            probe = probe.GetNext()
#在索引i的位置处插入节点
    def InsertNode(self, i, data):
        s = Node(data=data,next=None)
        if i == 0:
            s.SetNext(self._head)
            self._head = s
        elif 1<=i<=self._length:
            p = self.Get(i-1)
            s.SetNext(p.GetNext())
            p.SetNext(s)
        if i == self._length:  #在链表末尾插入节点，更改尾指针
            self._tail = s
        self._length+=1

#查找值为value的节点编号
    def Search(self,value):
        probe = self._head
        j = 0
        while probe is not None:
            if probe.GetData() == value:
                return j
            probe = probe.GetNext()
            j = j + 1
        return None  #找不到
#删除索引i的节点
    def DeleteNode(self, i):
        if i is None:
            raise ValueError('None is illegal index of LinkList.')
        self._length-=1
        #不是头节点
        if i != 0:
            #拿到前一个结点
            p = self.Get(i-1)
            s = p.GetNext()
            p.SetNext(s.GetNext())
            #如果删除的是尾节点，更改尾指针为原来的前一个结点
            if i == self._length:
                self._tail = p
            return s.GetData()
        else:  #删除头节点
            p = self._head
            self._head = p.GetNext()
            #如果链表中原来只有一个节点，删除后链表为空链表
            if 0 == self._length:
                self._tail = None
            return p.GetData()

if __name__=='__main__':
    ll=LinkList()
    ll.InsertNode(0,-2)
    ll.InsertNode(1, 1)
    ll.InsertNode(2, 0)
    ll.InsertNode(3, -1)
    ll.InsertNode(4, 2)
    ll.DeleteNode(3)
    print(ll.Search(2))     #3
    ll.InsertNode(1,5)
    print(ll.Get(1).GetData())        #5
    ll.PrintList()          #-2 5 1 0 2
    ll.DeleteNode(ll.Search(0))
    print('\n')
    ll.PrintList()          #-2 5 1 2
    ll.ClearList()
    print(ll.isEmpty())