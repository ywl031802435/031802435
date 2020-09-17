from functools import reduce
from math import sqrt

import jieba.analyse

class Document:
    def __init__(self, f1_, f2_, K=1000):
        self.f1 = f1_
        self.f2 = f2_
        self.topK = K
        self.vector1 = {}
        self.vector2 = {}

    # 去除文本中的符号
    def delsim(self):
        str_ = ['，', '。', '《', '》', '：', '\n', '、', '“', '”', '？', '—', ' ']
        for i in str_:
            self.f1 = self.f1.replace(i, '')
            self.f2 = self.f2.replace(i, '')

    # 构建字典向量存储文本权重
    def vector(self):
        cut1 = jieba.analyse.extract_tags(self.f1, topK=self.topK, withWeight=True)
        cut2 = jieba.analyse.extract_tags(self.f2, topK=self.topK, withWeight=True)

        # 构建向量
        for i, j in cut1:
            self.vector1[i] = j
        for i, j in cut2:
            self.vector2[i] = j

        # 将两个文本中没有的关键词填充0
        for key in self.vector1:
            self.vector2[key] = self.vector2.get(key, 0)
        for key in self.vector2:
            self.vector1[key] = self.vector1.get(key, 0)

        # 计算相对词频
        def level(vdict_):
            _min = min(vdict_.values())
            _max = max(vdict_.values())
            _mid = _max - _min
            for key_ in vdict_:
                vdict_[key_] = (vdict_[key_] - _min) / _mid
            return vdict_

        self.vector1 = level(self.vector1)
        self.vector2 = level(self.vector2)

    # 计算向量余弦相似值
    def similar(self):
        self.vector()
        self.delsim()
        sum_ = 0
        for key in self.vector1:
            sum_ += self.vector1[key] * self.vector2[key]
        a = sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, self.vector1.values())))
        b = sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, self.vector2.values())))
        return sum_ / (a * b)
        # print("%.2f" % (sum/(a*b)))