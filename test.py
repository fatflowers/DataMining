# -*- coding:GBK -*-
from random import randint
import cPickle
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
# D = []
# for row in range(3):
#     D.append([0.0]*3)
#
# D[0][0] = 3
# print D
# f = open('LocHistory.pkl', 'rb')
# # LocHistory = cPickle.load(open('LocHistory.pkl', 'rb'))
# a = [[[1, 2]]]
# test(a)
# print a

def findKthNumber(oneRow, k):
    if k == len(oneRow):
        return max(oneRow)
    randIndex = randint(0, len(oneRow) - 1)
    # print k, randIndex, oneRow
    Sa = [0.0] * len(oneRow)
    Sb = [0.0] * len(oneRow)

    lenSa = 0
    lenSb = 0

    allTheSame = True

    for elementIndex in range(len(oneRow)):
        if allTheSame and elementIndex > 0 and oneRow[elementIndex - 1] != oneRow[elementIndex]:
            allTheSame = False
        if oneRow[elementIndex] < oneRow[randIndex]:
            Sa[lenSa] = oneRow[elementIndex]
            lenSa += 1
        else:
            Sb[lenSb] = oneRow[elementIndex]
            lenSb += 1

    if allTheSame:
        return oneRow[0]

    if lenSa > k:
        return findKthNumber(Sa[:lenSa], k)
    elif lenSa == k:
        return max(Sa[:lenSa])
    else:
        return findKthNumber(Sb[:lenSb], k - lenSa)


a = cPickle.load(open('opticsResult.pkl', 'rb'))

rootNode = cPickle.load(open('rootNode.pkl', 'rb'))

D1 = cPickle.load(open('pointDistance\\pD1.pkl', 'rb'))[:4]

# a = [1,2,3,4,5,6,7,8,9,9,4,4,4,4,4]
# # for i in range(1, len(a) + 1):
# #     print findKthNumber(a, i)
# print findKthNumber(a, 1)

b = 0