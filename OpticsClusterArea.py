# -*- coding:GBK -*-
'''
 -------------------------------------------------------------------------
 Function:
 [RD,CD,order]=optics(x,k)
 -------------------------------------------------------------------------
 Aim:
 Ordering objects of a data set to obtain the clustering structure
 -------------------------------------------------------------------------
 Input:
 x - data set (m,n); m-objects, n-variables
 k - number of objects in a neighborhood of the selected object
 (minimal number of objects considered as a cluster)
 -------------------------------------------------------------------------
 Output:
 RD - vector with reachability distances (m,1)
 CD - vector with core distances (m,1)
 order - vector specifying the order of objects (1,m)
 -------------------------------------------------------------------------
 Example of use:
 x=[randn(30,2)*.4;randn(40,2)*.5+ones(40,1)*[4 4]];
 [RD,CD,order]=optics(x,4)
 -------------------------------------------------------------------------
 References:
 [1] M. Ankrest, M. Breunig, H. Kriegel, J. Sander,
 OPTICS: Ordering Points To Identify the Clustering Structure,
 available from www.dbs.informatik.uni-muenchen.de/cgi-bin/papers?query=--CO
 [2] M. Daszykowski, B. Walczak, D.L. Massart, Looking for natural
 patterns in analytical data. Part 2. Tracing local density
 with OPTICS, J. Chem. Inf. Comput. Sci. 42 (2002) 500-507
 -------------------------------------------------------------------------
 Written by Michal Daszykowski
 Department of Chemometrics, Institute of Chemistry,
 The University of Silesia
 December 2004
 http://www.chemometria.us.edu.pl


ported to python Jan, 2009 by Brian H. Clowers, Pacific Northwest National Laboratory.
Dependencies include scipy, numpy, and hcluster.
bhclowers at gmail.com
'''

import numpy as N
# import hcluster as H
import cPickle
import sys
from random import randint


def euclideanDist(x1, y1, x2, y2):
    return N.sqrt((x1 - x2)**2 + (y1 - y2)**2)



def writePointwiseDistance(x):

    sys.setrecursionlimit(100000000)  # 设置递归深度为10,000,000
    m, n = x.shape
    # D = []
    # D.append([0.0] * m)
    # D = D * m

    # D = [[0.0 for col in range(m)] for row in range(m)]
###wrong code...
    # D = []
    # row = N.array([0.0] *m)
    # for i in range(m):
    #     D.append(N.array(row))
    #
    # for iterOut in range(0, m):
    #     print iterOut
    #     for iterIn in range(iterOut + 1, m):
    #         D[iterIn][iterOut] = D[iterOut][iterIn] = float(euclideanDist(x[iterOut][0], x[iterOut][1], x[iterIn][0],
    #                                                                       x[iterIn][1]))
###
    nrowsPerFile = 1000
    fileNumber = 0
    oneRow = [0.0] * m

    D = [list(oneRow) for row in range(nrowsPerFile)]
    for iterOut in range(0, m):
        print iterOut
        if iterOut % nrowsPerFile == 0 and iterOut != 0:
            cPickle.dump(D, open('pointDistance\\' + str(fileNumber), 'wb'))
            D = [list(oneRow) for row in range(nrowsPerFile)]
            fileNumber += 1
        for iterIn in range(0, m):
            D[iterOut % nrowsPerFile][iterIn] = float(euclideanDist(x[iterOut][0], x[iterOut][1], x[iterIn][0], x[iterIn][1]))

    cPickle.dump(D, open('pointDistance\\' + str(fileNumber), 'wb'))


    # cPickle.dump(D, open("pointwiseDistance.pkl", "wb"))


def getPointDistance(rowIndex):
    nrowsPerFile = 1000
    currentFileNo = rowIndex / nrowsPerFile
    return currentFileNo, cPickle.load(open('pointDistance\\' + str(currentFileNo), 'rb'))


def optics(x, k, distMethod='euclidean'):
    def getDistanceRow(rowNumber):
        row = [0.0] * m
        for iterRow in range(m):
            row[iterRow] = euclideanDist(x[rowNumber][0], x[rowNumber][1], x[iterRow][0], x[iterRow][1])
        return row

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



    if len(x.shape) > 1:
        m, n = x.shape
    else:
        m = x.shape[0]
        n = 1

    try:
        pass
    except Exception, ex:
        print ex
        print "squareform or pdist error"
        distOK = False
        return


    currentFileNo = None
    nrowsPerFile = 1000

    CD = N.zeros(m)
    RD = N.ones(m) * 1E10

    for i in xrange(m):
        print i, m
        # again you can use the euclid function if you don't want hcluster
        #        d = euclid(x[i],x)
        #        d.sort()
        #        CD[i] = d[k]

        # tempInd = D[i].argsort()
        # tempD = D[i][tempInd]
        # #        tempD.sort() #we don't use this function as it changes the reference
        # CD[i] = tempD[k]  #**2
        # ## the following 2 line will take the place of the above 4 lines
        # if currentFileNo is None or i / nrowsPerFile != currentFileNo:
        #     currentFileNo, D = getDistanceRow(i)
        # tempD = list(D[i % nrowsPerFile])
        tempD = list(getDistanceRow(i))
        # print tempD
        tempD.sort()
        CD[i] = tempD[k]

        # # alternative function faster
        # CD[i] = findKthNumber(getPointDistance(i), k)

    order = []
    seeds = N.arange(m, dtype=N.int)

    ind = 0
    count = 0
    while len(seeds) != 1:
        # for seed in seeds:
        ob = seeds[ind]

        print "main loop" + str(count)
        count += 1

        seedInd = N.where(seeds != ob)
        seeds = seeds[seedInd]

        order.append(ob)
        tempX = N.ones(len(seeds)) * CD[ob]
        # 此处肯定访问过D，所以nrowsPerFile不可能为None
        # if ob / nrowsPerFile != currentFileNo:
        #     currentFileNo, D = getDistanceRow(ob)
        tempD = N.array(getDistanceRow(ob))[seeds]  #[seeds]
        #you can use this function if you don't want to use hcluster
        #tempD = euclid(x[ob],x[seeds])

        temp = N.column_stack((tempX, tempD))
        mm = N.max(temp, axis=1)
        ii = N.where(RD[seeds] > mm)[0]
        RD[seeds[ii]] = mm[ii]
        ind = N.argmin(RD[seeds])

    order.append(seeds[0])
    RD[0] = 0  # we set this point to 0 as it does not get overwritten
    return RD, CD, order


def euclid(i, x):
    """euclidean(i, x) -> euclidean distance between x and y"""
    y = N.zeros_like(x)
    y += 1
    y *= i
    if len(x) != len(y):
        raise ValueError, "vectors must be same length"

    d = (x - y) ** 2
    return N.sqrt(N.sum(d, axis=1))

