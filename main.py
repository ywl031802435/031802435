from functools import reduce
import jieba.analyse
from math import sqrt
import sys
#定义文件类
class Document():
    def __init__(self,f1,f2,topK):
        self.f1 = f1
        self.f2 = f2
        self.topK = topK
        self.vector1 = {}
        self.vector2 = {}
    #去除文本中的符号
    def delsim(self):
        str = ['，','。','《','》','：','\n','、','“','”','？','—',' ']
        for i in str:
            self.f1 = self.f1.replace(i, '')
            self.f2 = self.f2.replace(i, '')

    #构建字典向量存储文本权重
    def vector(self):
        cut1 = jieba.analyse.extract_tags(f1,topK = K, withWeight = True)
        cut2 = jieba.analyse.extract_tags(f2,topK = K, withWeight = True)

        #构建向量
        for i,j in cut1:
            self.vector1[i] = j
        for i,j in cut2:
            self.vector2[i] = j

        #将两个文本中没有的关键词填充0
        for key in self.vector1:
            self.vector2[key] = self.vector2.get(key, 0)
        for key in self.vector2:
            self.vector1[key] = self.vector1.get(key, 0)

    # 计算相对词频
        def maplevel(vdict):
            _min = min(vdict.values())
            _max = max(vdict.values())
            _mid = _max - _min
            for key in vdict:
                vdict[key] = (vdict[key] - _min) / _mid
            return vdict
        self.vector1 = maplevel(self.vector1)
        self.vector2 = maplevel(self.vector2)
    #计算向量余弦相似值
    def similar(self):
        self.vector()
        self.delsim()
        sum = 0
        for key in self.vector1:
            sum += self.vector1[key]*self.vector2[key]
        a = sqrt(reduce(lambda x,y: x+y, map(lambda x: x*x, self.vector1.values())))
        b = sqrt(reduce(lambda x,y: x+y, map(lambda x: x*x, self.vector2.values())))
        return sum/(a*b)
        #print("%.2f" % (sum/(a*b)))

if __name__ == '__main__':
    orifile = sys.argv[1]
    copyfile = sys.argv[2]
    ansfile = sys.argv[3]
    #读入文件
    try:
        with open(orifile,encoding = 'utf-8') as file1:
            f1 = file1.read()
        with open(copyfile,encoding ='utf-8') as file2:
            f2 = file2.read()
    except:
        print('路径有错')
    K = int(len(f1)*0.8)
    s = Document(f1,f2,K)
    sim = round(s.similar(),2)
    #输出文件
    try:
        with open(ansfile,'w+',encoding = 'utf-8') as file3:
            file3.write(str(sim))
    except:
        print('路径有错')
    import sys
    s.similar()
