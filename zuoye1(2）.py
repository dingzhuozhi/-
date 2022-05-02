import networkx as nx


# ————————————————————调包用Dijkstra算法求上图出从顶点1出发到其余各点的最短路径。————————————————————
class Find_shortest_path_diaobao:
    def __init__(self):
        self.G = nx.Graph()
        self.nodes = [1, 2, 3, 4, 5, 6, 7]
        self.G.add_nodes_from(self.nodes)
        self.ebunch = [(1, 2, 6), (1, 3, 7), (2, 3, 14), (2, 4, 23), (2, 5, 18),
                       (3, 4, 25), (3, 6, 20), (4, 5, 12), (4, 6, 15), (5, 6, 8), (5, 7, 5),
                       (6, 7, 10)]

        self.G.add_weighted_edges_from(self.ebunch)

    def get_shortest_path(self, node, target):
        print("节点{}到节点{}的最短路径是:".format(node, target), nx.dijkstra_path(self.G, node, target))
        print("节点{}到节点{}的最短路径长度:".format(node, target), nx.dijkstra_path_length(self.G, node, target))

    def get_shortest_path_from(self, start):
        for node in self.nodes:
            self.get_shortest_path(start, node)


if __name__ == '__main__':
    print("---------调包Dijkstra算法求上图出从顶点1出发到其余各点的最短路径----------。")
    f = Find_shortest_path_diaobao()
    f.get_shortest_path_from(1)

# ————————————————————非调包---------------------
# 求上图出从顶点1出发到其余各点的最短路径。————————————————————

import heapq  # 用小根堆（优先队列）实现
import math


class Find_shortest_path:
    def __init__(self):
        self.graph = {  # 邻接表,注意这里的表示需要双向表示，如1连到2,2也需要连到1
            1: {2: 6, 3: 7},
            2: {3: 14, 4: 23, 5: 18, 1: 6},
            3: {4: 25, 6: 20, 2: 14, 1: 7},
            4: {5: 12, 6: 15, 3: 25, 2: 23},
            5: {6: 8, 7: 5, 2: 18, 4: 12},
            6: {7: 10, 5: 8, 4: 15, 3: 20},
            7: {6: 10, 5: 5}}

    def init_distance(self, s):  # 初始化我们的距离字典，除了节点到本节点距离为0，其余初始化为正无穷
        distance = {s: 0}
        for vertex in self.graph:
            if vertex != s:
                distance[vertex] = math.inf
        return distance

    def dijkstra(self, s):
        pqueue = []  # 一个初始的小根堆
        heapq.heappush(pqueue, (0, s))  # 初始导入和自身点的距离和顶点
        seen = set()  # 已经使用的节点集合
        parent = {s: None}  # 节点的路径前端
        distance = self.init_distance(s)  # 初始化距离
        while len(pqueue) > 0:
            pair = heapq.heappop(pqueue)  # 弹出距离最短的距离和元素
            dist = pair[0]  # 距离
            vertex = pair[1]  # 顶点
            seen.add(vertex)  # 放入集合
            nodes = self.graph[vertex].keys()  # 邻接点
            for w in nodes:
                if w not in seen:
                    if dist + self.graph[vertex][w] < distance[w]:  # 更新最短距离
                        heapq.heappush(pqueue, (dist + self.graph[vertex][w], w))
                        parent[w] = vertex  # 更新
                        distance[w] = dist + self.graph[vertex][w]  # 更新
        path_list = []
        for path in parent:
            if path == s:
                path_list.append("{}".format(s))
            else:
                node = path
                final = ""
                p = path
                while p != s:
                    p = parent[path]
                    if p == s:
                        final = "{}".format(p) + final
                        break
                    final = "->{}".format(p) + final
                    path = p
                final = final + "->{}".format(node)
                path_list.append(final)
        return path_list, distance


if __name__ == '__main__':
    F = Find_shortest_path()
    start = 1
    path_list, distance = F.dijkstra(start)
    print("---------用领接表使用Dijkstra算法求上图出从顶点1出发到其余各点的最短路径----------。")
    print("从顶点1到各个顶点的最短路径:", path_list)
    print("从顶点1到各个顶点的最短路径长度:", distance)
