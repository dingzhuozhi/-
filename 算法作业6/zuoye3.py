"""
3.	一位公司主席正向W教授咨询公司聚会计划。公司内部结构关系是层次化的，
即员工按主管-下属关系构成一棵树，根节点是公司主席。
人事部按“宴会交级能力”为每个员工打分，分值为实数。
为了使所有参加聚会的员工都感到愉快，主席不希望员工及其直接主管同时出席。
公司主席向W教授提供了公司结构树，树上每个节点除了保存指针外，还保存员工的名字和宴会交际评分。
设计算法，求宴会交际评分之和最大的宾客名单，并分析算法时间复杂度。

"""


class node():
    def __init__(self, score, name, parentNode):
        self.score = score  # 宴会得分
        self.name = name
        self.parent = parentNode
        self.child = []


def company_party_max(r):  # r是整个数的根结点root
    s0 = {}  # 不选当前节点的分数
    s1 = {}  # 选当前节点的分数
    attend = {}  # 参加列表
    company_party_score(r, s0, s1, attend)  # 得出两个各自得分，进行汇总
    if s0[r] > s1[r]:
        s = s0[r]
    else:
        s = s1[r]
    return s, attend  # 是返回的最大评分


def company_party_score(p, s0, s1, attend):  # P为子树的根结点 后序遍历
    if p is None:  # 递归终止条件
        return
    else:
        s0[p] = 0  # 不选为0
        s1[p] = p.score  # 选了为当前点得分
        for i in range(len(p.child)):  # 遍历孩子
            company_party_score(p.child[i], s0, s1, attend)  # 递归
            if s0[p.child[i]] > s1[p.child[i]]:  # 不选的比选的大
                s0[p] += s0[p.child[i]]  # 父亲不选，孩子也可以不选
            else:
                s0[p] += s1[p.child[i]]  # 孩子选，父亲不选
            s1[p] += s0[p.child[i]]  # 父亲选，孩子不选

    if s0[p] > s1[p]:  # 不选的总得分比选的大
        attend[p] = 0
    else:  # 不选的总得分比选的小
        attend[p] = 1


def party_list(p, attend, parent_attend=0):  # parent_attend初始值为0，根节点是公司主席，其没有上司 先序遍历
    if p is None:  # 递归终止条件
        return
    if parent_attend == 0:  # 必须保证父节点不选的情况下，才能去判断子节点该不该选
        cur_attend = attend[p]
        if attend[p] == 1:  # 父节点不选，子节点选，就打印
            print(p.name)
    else:
        cur_attend = 0  # 父节点选了，子节点不能选
    for i in range(len(p.child)):
        party_list(p.child[i], attend, cur_attend)  # 本质是一个先序遍历


if __name__ == "__main__":
    r = node(60, '公司主席', None)
    p1 = node(90, '主管1', r)
    p2 = node(80, '主管2', r)
    c1 = node(20, '员工1', p1)
    c2 = node(20, '员工2', p1)
    c3 = node(20, '员工3', p2)
    c4 = node(20, '员工4', p2)

    r.child = [p1, p2]
    p1.child = [c1, c2]
    p2.child = [c3, c4]

    s, attend = company_party_max(r)
    for i in attend:
        print(i.name)
    print('最大的宴会交际得分之和为：', s)
    print('参加宴会的名单如下：')
    party_list(r, attend, 0)
