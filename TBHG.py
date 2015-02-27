# -*- coding:GBK -*-
__author__ = 'Administrator'
from UserTrajectory import *
# import numpy as np
from points import *
import matplotlib.pyplot as plt
import OpticsClusterArea as OP
import AutomaticClustering as AutoC

import cPickle


# 在AutoC的TreeNode类中添加neighbor属性，为列表
def linkClusters(levelNodes, stayPointNumber):
    dupStayPointNumber = list(stayPointNumber)
    # userVisitedTimes = [0] * len(stayPointNumber)
    nextLevelNodes = []
    for iterNode in levelNodes:
        if len(iterNode.children) > 0:
            nextLevelNodes += iterNode.children

    if len(levelNodes) != 1:
        for iterNode in range(len(levelNodes)):
            levelNodes[iterNode].userVisitedTimes = [0] * len(stayPointNumber)
            userID = 0
            for userTrajectory in dupStayPointNumber:
                for trajectory in userTrajectory:
                    flag = False
                    for iterStayPoint in range(len(trajectory)):
                        # 当前stay Point在这个cluster中
                        if levelNodes[iterNode].start <= trajectory[iterStayPoint] <= levelNodes[iterNode].end:
                            if flag is False:
                                # 增加当前用户访问次数
                                levelNodes[iterNode].userVisitedTimes[userID] += 1
                                flag = True
                        # 上一个节点在node这个cluster中
                        elif flag and (levelNodes[iterNode].start > trajectory[iterStayPoint]
                                       or trajectory[iterStayPoint] > levelNodes[iterNode].end):
                            flag = False
                            for neighborNode in levelNodes:
                                if neighborNode.start <= trajectory[iterStayPoint] <= neighborNode.end:
                                        # and levelNodes[iterNode].start <= trajectory[iterStayPoint] <= levelNodes[iterNode].end:

                                    levelNodes[iterNode].neighbor.append((neighborNode.start, neighborNode.end))
                                    # -1代表访问过
                                    # trajectory[iterStayPoint] = -1
                        elif flag:
                            flag = False
                userID += 1

    if len(nextLevelNodes) > 0:
        linkClusters(nextLevelNodes, stayPointNumber)

def getTBHG():
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

    ### plot the distribution
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(stayPointMatrix[:,0], stayPointMatrix[:,1], 'b.', ms=2)

    plt.savefig('Graph.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1)
    plt.show()

    #run the OPTICS algorithm on the points, using a smoothing value (0 = no smoothing)

    ### 从磁盘读取距离矩阵
    # OP.writePointwiseDistance(stayPointMatrix)

    RD, CD, order = OP.optics(stayPointMatrix, 9)

    cPickle.dump([RD, CD, order], open('opticsResult2.pkl', 'wb'))

    RPlot = []
    RPoints = []

    for item in order:
        RPlot.append(RD[item]) #Reachability Plot
        RPoints.append([stayPointMatrix[item][0], stayPointMatrix[item][1]]) #points in their order determined by OPTICS

    #hierarchically cluster the data
    rootNode = AutoC.automaticCluster(RPlot, RPoints)
    cPickle.dump(rootNode, open('rootNode2.pkl', 'wb'))
    AutoC.graphTree(rootNode, RPlot)

    linkClusters(rootNode, stayPointNumber)

# if __name__ == "__main__":
getTBHG()
# LocHistory = cPickle.load(open('LocHistory.pkl', 'rb'))
# sum = 0
# for i in a:
#     sum += len(i.trajectory)