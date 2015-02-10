# -*- coding:GBK -*-
__author__ = 'Administrator'
from UserTrajectory import *
import numpy as np
from points import *
import matplotlib.pyplot as plt
import OpticsClusterArea as OP
import AutomaticClustering as AutoC

import cPickle

def getTBHG():
    LocHistory = cPickle.load(open('LocHistory.pkl', 'rb'))

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
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    #
    # ax.plot(stayPointMatrix[:,0], stayPointMatrix[:,1], 'b.', ms=2)
    #
    # plt.savefig('Graph.png', dpi=None, facecolor='w', edgecolor='w',
    #     orientation='portrait', papertype=None, format=None,
    #     transparent=False, bbox_inches=None, pad_inches=0.1)
    # plt.show()

    #run the OPTICS algorithm on the points, using a smoothing value (0 = no smoothing)

    ### 从磁盘读取距离矩阵
    OP.writePointwiseDistance(stayPointMatrix)

    RD, CD, order = OP.optics(stayPointMatrix, 9)

    # cPickle.dump([RD, CD, order], open('opticsResult.pkl', 'wb'))

    RPlot = []
    RPoints = []

    for item in order:
        RPlot.append(RD[item]) #Reachability Plot
        RPoints.append([stayPointMatrix[item][0], stayPointMatrix[item][1]]) #points in their order determined by OPTICS

    #hierarchically cluster the data
    rootNode = AutoC.automaticCluster(RPlot, RPoints)
    AutoC.graphTree(rootNode, RPlot)
    o = 0



getTBHG()
# LocHistory = cPickle.load(open('LocHistory.pkl', 'rb'))
# sum = 0
# for i in a:
#     sum += len(i.trajectory)