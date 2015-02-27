# -*- coding:GBK -*-

import numpy as np
import matplotlib.pyplot as plt
import OpticsClusterArea as OP
from itertools import *
import AutomaticClustering as AutoC
from random import randint
import cPickle
from UserTrajectory import *
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


# opticsResult = cPickle.load(open('opticsResult.pkl', 'rb'))
# RD = opticsResult[0]
# CD = opticsResult[1]
# order = opticsResult[2]
# RPlot = []
# RPoints = []
#
#
#
#
# rootNode = cPickle.load(open('rootNode.pkl', 'rb'))
# # AutoC.graphTree(rootNode, RPlot)
#
# #get only the leaves of the tree
# leaves = AutoC.getLeaves(rootNode, [])
#
# #graph the points and the leaf clusters that have been found by OPTICS
# fig = plt.figure()
# ax = fig.add_subplot(111)
LocHistory = cPickle.load(open('LocHistory2.pkl', 'rb'))

numPoints = 0
for user in LocHistory:
    for traj in user.trajectory:
        numPoints += len(traj)

stayPointNumber = []
stayPointMatrix = np.zeros((numPoints, 2))

iterPoint = 0
for user in LocHistory:
    userStayPointNumber = []
    for traj in user.trajectory:
        userTrajectory = []
        for iter in traj:
            userTrajectory.append(iterPoint)
            stayPointMatrix[iterPoint] = [iter.latitude, iter.longitude]
            iterPoint += 1
        userStayPointNumber.append(userTrajectory)
    stayPointNumber.append(userStayPointNumber)

for item in order:
    RPlot.append(RD[item]) #Reachability Plot
    RPoints.append([stayPointMatrix[item][0],stayPointMatrix[item][1]]) #points in their order determined by OPTICS

ax.plot(stayPointMatrix[:,0], stayPointMatrix[:,1], 'y.')
colorString = 'bgrcmyk'
colors = cycle(colorString)
colorCounter = 0
for item, c in zip(leaves, colors):
    node = []
    for v in range(item.start,item.end):
        node.append(RPoints[v])
    node = np.array(node)
    if colorCounter / len(colorString) == 0:
        marker = 'o'
    elif colorCounter / len(colorString) == 1:
        marker = '+'
    else:
        marker = '*'
    ax.plot(node[:,0],node[:,1], c + marker, ms=5)

    colorCounter += 1

plt.savefig('Graph2.png', dpi=None, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format=None,
    transparent=False, bbox_inches=None, pad_inches=0.1)
plt.show()

# a = [1,2,3,4,5,6,7,8,9,9,4,4,4,4,4]
# # for i in range(1, len(a) + 1):
# #     print findKthNumber(a, i)
# print findKthNumber(a, 1)

b = 0