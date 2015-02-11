# -*- coding:GBK -*-

# __author__ = 'Administrator'
# from OpticsClusterArea import *
# import numpy as np
# # from points import *
# # def a():
# #     global iii
# #     print iii
# # pi = Point()
# # pj = Point()
# #
# # pi.latitude = 39.984702
# # pi.longitude = 116.318417
# # pj.latitude = 39.983675
# # pj.longitude = 116.299031
# #
# # print gpsDistance(pi, pj)
# # print gpsDistance2(pi, pj)
# # a()
# x = np.array([[1, 0], [2, 0], [3, 0]])
#
# writePointwiseDistance(x)
#

# 在AutoC的TreeNode类中添加neighbor属性，为列表
def linkClusters(levelNodes, stayPointNumber):
    dupStayPointNumber = list(stayPointNumber)
    nextLevelNodes = []
    for iterNode in levelNodes:
        if len(iterNode.children) > 0:
            nextLevelNodes += iterNode.children

    if len(levelNodes) != 1:
        for iterNode in range(len(levelNodes)):
            for userTrajectory in dupStayPointNumber:
                for trajectory in userTrajectory:
                    flag = False
                    for iterStayPoint in range(len(trajectory)):
                        if trajectory[iterStayPoint] == -1:
                            continue
                        if levelNodes[iterNode].start <= trajectory[iterStayPoint] <= levelNodes[iterNode].end:
                            flag = True
                        # 上一个节点在node这个cluster中
                        elif flag and (levelNodes[iterNode].start > trajectory[iterStayPoint] or trajectory[iterStayPoint] > levelNodes[iterNode].end):
                            for neighborNode in levelNodes:
                                if neighborNode.start != levelNodes[iterNode].start and neighborNode.end != levelNodes[iterNode].end and levelNodes[iterNode].start <= trajectory[iterStayPoint] <= levelNodes[iterNode].end:
                                    levelNodes[iterNode].neighbor.append((neighborNode.start, neighborNode.end))
                                    # -1代表访问过
                                    trajectory[iterStayPoint] = -1

    if len(nextLevelNodes) > 0:
        linkClusters(nextLevelNodes, stayPointNumber)


def test(a):
    for aa in a:
        for aaa in aa:
            for aaaa in range(len(aaa)):
                aaa[aaaa] = 3

a = [[[1, 2]]]
test(a)
print a
