# 2.	实现哈夫曼编码和解码，并对一段英文文本进行编解码测试。
"""
实际上是现有一串英文文本，我们计算英文文本中的字频，通过对应关系生成哈夫曼树，得到对应的哈夫曼编码，再进行替换得到哈夫曼密码
得到密码，再通过哈夫曼树，进行解码
"""

import collections


class Node:
    def __init__(self, name, weight):
        self.name = name  # 节点名
        self.weight = weight  # 节点权重
        self.left = None  # 节点左孩子
        self.right = None  # 节点右孩子
        self.father = None  # 节点父节点

    def is_left_child(self):  # 判断当前节点是否是左孩子
        return self.father.left == self


def create_HF_tree(nodes):  # 建立哈夫曼树的过程
    tree_nodes = nodes.copy()  # 复制一下节点，都是叶子节点
    while len(tree_nodes) > 1:  # 只剩根节点时，退出循环，因为这个时候没有两个节点可以出了
        tree_nodes.sort(key=lambda node: node.weight)  # 升序排列
        new_left = tree_nodes.pop(0)  # 最小的节点，作为左节点
        new_right = tree_nodes.pop(0)  # 第二小的节点，作为右节点
        new_node = Node(None, (new_left.weight + new_right.weight))  # 这两个节点之和，作为父节点
        new_node.left = new_left
        new_node.right = new_right
        new_left.father = new_right.father = new_node
        tree_nodes.append(new_node)  # 重新把这个节点传入队列中
    tree_nodes[0].father = None  # 根节点父亲为None
    return tree_nodes[0]  # 返回根节点


# 获取huffman编码
def get_huffman_dict(str):
    a = collections.Counter(str)  # 统计str里的每个英文字母的频率
    nodes = []  # 创建节点的列表
    for i, j in a.items():  # 传入列表，键为字母，键值为字母的频率
        nodes.append(Node(i, j))
    create_HF_tree(nodes)  # 建立哈夫曼树
    huffman_dict = {}  # 最后的密码表
    for node in nodes:  # 从叶节点开始往上走,走到根节点停
        code = ''  # 每个节点的哈夫曼编码
        name = node.name  # 选择节点的名字
        while node.father != None:  # 没有父节点说明到了根节点就停止了
            if node.is_left_child():  # 如果是当前节点为左孩子
                code = '0' + code  # 加0，注意是在左边加0，因为是从下往上的过程
            else:
                code = '1' + code
            node = node.father
        huffman_dict[name] = code  # 传入字典
    return huffman_dict


def after_huffman_coding(str, huffman_dict):  # 哈夫曼编码的过程
    res = ""
    for i in str:
        res += huffman_dict[i]
    return res


def decode(code, huffman_reverse_dict):  # 哈夫曼解码的过程
    res = ""
    tmp = ""
    i = 0
    n = len(code)
    while i <= n - 1:
        if tmp not in huffman_reverse_dict.keys():
            tmp += code[i]
            i += 1
            if i == n:
                res += huffman_reverse_dict[tmp]
        else:
            res += huffman_reverse_dict[tmp]
            tmp = ""
    return res


if __name__ == '__main__':
    str = input("请输入你想编码的一段话(英语)")
    huffman_dict = get_huffman_dict(str)
    print(huffman_dict)  # 可以得到每个英文字母对应的哈夫曼编码值
    code = after_huffman_coding(str, huffman_dict)
    print("编码后的结果:", code)  # 得到经过哈夫曼编码后的一串密码
    huffman_reverse_dict = {j: i for i, j in huffman_dict.items()}
    print(huffman_reverse_dict)  # 可以得到每个哈夫曼编码值对应的英文字母
    decode1 = decode(code, huffman_reverse_dict)  # 解码，此处用的还是前面的密码，没有修改
    print("解码后的结果:", decode1)
