# 用python定义图类，提供邻接矩阵、字典形式邻接表、边三元组存储结构。
# 选择一种结构实现Prim算法、 Kruskal算法
import matplotlib.pyplot as plt

import networkx as nx
from collections import defaultdict
import heapq


# ————————————————————使用Prim算法构造出如下图所示的网的最小生成树，并给出最小生成树的代价。用红色线表示最小生成树。————————————————————

class Prim:
    def __init__(self, ebunch, start):  # 需要传入边和初始顶点
        self.ebunch = ebunch
        self.edges = [(w, u, v) for u, v, w in ebunch]  # 转换成权重在前，因为要小根堆操作
        self.start = start

    def prim(self):
        adjacent_dict = defaultdict(list)  # 构建邻接表
        for weight, v1, v2 in self.edges:
            adjacent_dict[v1].append((weight, v1, v2))
            adjacent_dict[v2].append((weight, v2, v1))
        minu_tree = []  # 最小生成树
        visited = [self.start]  # 存储访问过的顶点，注意指定起始点
        adjacent_vertexs_edges = adjacent_dict[self.start]  # 初始的点的邻接边
        heapq.heapify(adjacent_vertexs_edges)  # 变成小根堆，便于找到权重最小的边，这步实际上可以不要，只是体现出建堆的过程
        while adjacent_vertexs_edges:
            weight, v1, v2 = heapq.heappop(adjacent_vertexs_edges)  # 小根堆弹出权重最小的边
            if v2 not in visited:
                visited.append(v2)  # 已访问
                minu_tree.append((weight, v1, v2))  # 放入结果
                for next_edge in adjacent_dict[v2]:  # 继续进行寻找，找到v2相邻的边，把这些边压入小根堆，以实现集合的完整性。
                    if next_edge[2] not in visited:  # 如果v2还未被访问过，就加入堆中
                        heapq.heappush(adjacent_vertexs_edges, next_edge)

        return minu_tree

    def get_total_weight(self):
        minu_tree = self.prim()
        total_weight = 0
        for w, u, v in minu_tree:
            total_weight += w
        return total_weight


if __name__ == "__main__":
    ebunch = [(1, 2, 6), (1, 3, 7), (2, 3, 14), (2, 4, 23), (2, 5, 18),
              (3, 4, 25), (3, 6, 20), (4, 5, 12), (4, 6, 15), (5, 6, 8), (5, 7, 5),
              (6, 7, 10)]

    P = Prim(ebunch, 1)
    print("prim算法生成的最小生成树(w,u,v)--(权重，边，边）:")
    print(P.prim())
    print("从顶点1出发构建的最小生成树的代价为:",P.get_total_weight())



# ————————————————————使用Kruskal算法构造出如下图所示的网的最小生成树，并给出最小生成树的代价。用红色线表示最小生成树。————————————————————
# 并查集的思想
"""
【并查集】

1.对于每一次连接，找需要连接的两个点的祖先，直到找到他们的最先的祖先，比较，如果一样，说明已经连通，不能连接，否则说明可以连接

2.对于每一次成功的连接，后加入“已连接”集合的，都认他所连接的那个已经在集合内的点叫做“爸爸”，如果两个点都是第一次进集合，那么随便认一个点做“爸爸”

3.对于每一次成功的连接，如果是两个家族连接在一起，那么其中一个家族的最先祖先，认另外一个家族的最先祖先做爸爸

可见，只要最先祖先相同，连接起来一定成环


"""

class Kruskal:
    def __init__(self,ebunch,vertices):

        self.X = dict()  # 以全局变量X定义节点集合，即类似{'A':'A','B':'B','C':'C','D':'D'},如果A、B两点连通，则会更改为{'A':'B','B':'B",...},
        # 即任何两点连通之后，两点的值value将相同。
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
                if len(minu_tree) == len(self.vertices) - 1: #添加了提前终止条件，节约时间复杂度
                    break
        return minu_tree

    def total_cost(self):
        minu_tree = self.kruskal()
        cost = 0
        for i in minu_tree:
            cost += i[0]
        return cost


if __name__ == '__main__':
    ebunch = [(1, 2, 6), (1, 3, 7), (2, 3, 14), (2, 4, 23), (2, 5, 18),
                   (3, 4, 25), (3, 6, 20), (4, 5, 12), (4, 6, 15), (5, 6, 8), (5, 7, 5),
                   (6, 7, 10)]
    vertices = [1, 2, 3, 4, 5, 6, 7]
    K = Kruskal(ebunch,vertices)
    minu_tree = K.kruskal()
    cost = K.total_cost()
    print("kruskal算法生成的最小生成树(w,u,v)--(权重，边，边）:")
    print(minu_tree)
    print("最小生成树的代价:", cost)
    G = nx.Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7]
    G.add_nodes_from(nodes)
    ebunch = [(u, v, w) for w, u, v in minu_tree]

    G.add_weighted_edges_from(ebunch)
    nx.draw(G, node_size=300, with_labels=True,
            edge_color='r')
    pos = nx.spring_layout
    plt.show()
