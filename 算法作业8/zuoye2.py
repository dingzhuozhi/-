"""
.在 n 个城市架设 n-1 条线路，建设通信网络。任意两个城市之间都可以建设通信线路，
且单位长度的建设成本相同。求建设通信网络的最低成本的线路方案。
（1）城市数\(n\geq10\)，由键盘输入；
（2）城市坐标 x, y 在（0～100）之间随机生成；
（3）输出线路方案的各段线路及长度。

"""

# 本程序使用Kruskal算法,因为感觉kruskal的思想更符合实际工程中的操作，是将一条条通信线路放回没有任何线路的网络中。而不是和prim一样要选择初始顶点，不符合常规思维
# 克鲁斯卡尔算法的时间复杂度为O(m log m)而普林算法的时间复杂度为O(m log n)

import random
import math
import networkx as nx
import matplotlib.pyplot as plt


class Kruskal:
    def __init__(self, ebunch, vertices):

        self.X = dict()  # 以全局变量X定义节点集合，即类似{'A':'A','B':'B','C':'C','D':'D'},如果A、B两点连通，则会更改为{'A':'B','B':'B",...},即任何两点连通之后，两点的值value将相同。
        self.R = dict()  # 各点的初始等级均为0,如果被做为连接的的末端，则增加1
        self.ebunch = ebunch
        self.edges = [(w, u, v) for u, v, w in self.ebunch]
        self.vertices = vertices

    def make_set(self, point):  # 初始的定义
        self.X[point] = point
        self.R[point] = 0

    def find(self, point):  # 查询并查集,找到祖先即根节点，并进行更新
        if self.X[point] != point:
            self.X[point] = self.find(self.X[point])
        return self.X[point]

    def merge(self, point1, point2):  # 合并两个集合，只需要合并两个集合的根节点
        r1 = self.find(point1)
        r2 = self.find(point2)
        if r1 != r2:
            if self.R[r1] > self.R[r2]:  # 如果祖先等级大
                self.X[r2] = r1  # r1变成r2的祖先
            else:
                self.X[r1] = r2  # 相反一样
                if self.R[r1] == self.R[r2]:  # 如果是相等情况，
                    self.R[r2] += 1

    def kruskal(self):
        for vertice in self.vertices:  # 所有点的初始化
            self.make_set(vertice)
        minu_tree = []  # 最小生成树
        self.edges.sort()  # 按照权重从小到大排序
        for edge in self.edges:  # 逐个选择
            weight, vertice1, vertice2 = edge
            if self.find(vertice1) != self.find(vertice2):  # 如果连不成环
                self.merge(vertice1, vertice2)  # 进行归并
                minu_tree.append(edge)  # 添加当前边作为最小生成树的边
                if len(minu_tree) == len(self.vertices) - 1:
                    break
        return minu_tree

    def total_cost(self):
        minu_tree = self.kruskal()
        cost = 0
        for i in minu_tree:
            cost += i[0]
        return cost


if __name__ == '__main__':
    n = int(input("输入城市数量"))
    city_list = []
    for i in range(1, n + 1):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        city_list.append((i, x, y))
    ebunch = []
    for i in range(0, n):
        for j in range(i + 1, n):
            distance = round( # 欧氏距离
                math.sqrt((city_list[i][1] - city_list[j][1]) ** 2 + (city_list[i][2] - city_list[j][2]) ** 2), 0)
            ebunch.append((i + 1, j + 1, distance))
    vertices = [i for i in range(1, n + 1)]
    K = Kruskal(ebunch, vertices)
    minu_tree = K.kruskal()
    cost = K.total_cost()
    print("kruskal算法生成的最小生成树(w,u,v)--(权重，边，边）:", minu_tree)
    print("最小生成树的代价:", cost)
    # 可视化
    G = nx.Graph()
    nodes = vertices
    G.add_nodes_from(nodes)
    ebunch = []
    for w, u, v in minu_tree:
        ebunch.append((u, v, w))
    G.add_weighted_edges_from(ebunch)
    nx.draw(G, node_size=300, with_labels=True,
            edge_color='r')
    pos = nx.spring_layout
    plt.show()
