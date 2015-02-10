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
import hcluster as H
import cPickle
import sys


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
    nrowsPerFile = 5000
    fileNumber = 0
    oneRow = [0.0] * m

    D = [list(oneRow) for row in range(nrowsPerFile)]
    for iterOut in range(0, m):
        print iterOut
        if iterOut % nrowsPerFile == 0 and iterOut != 0:
            cPickle.dump(D, open('pointDistance\\' + str(fileNumber), 'wb'))
            D = [list(oneRow) for row in range(fileNumber)]
            fileNumber += 1
        for iterIn in range(0, m):
            D[iterOut % nrowsPerFile][iterIn] = float(euclideanDist(x[iterOut][0], x[iterOut][1], x[iterIn][0], x[iterIn][1]))


    # cPickle.dump(D, open("pointwiseDistance.pkl", "wb"))


def getPointDistance(rowIndex):
    nrowsPerFile = 5000
    currentFileNo = rowIndex / nrowsPerFile
    return currentFileNo, cPickle.load(open('pointDistance\\' + str(currentFileNo), 'wb'))


def optics(x, k, distMethod='euclidean'):
    if len(x.shape) > 1:
        m, n = x.shape
    else:
        m = x.shape[0]
        n = 1

    try:
        # tmp = H.pdist(x, distMethod)
        # D = H.squareform(tmp)


        # D = H.squareform(H.pdist(x, distMethod))
        # ## the following 6 lines will take the place of the above line
        # D = []
        # D.append([0.0] * m)
        # D = D * m
        # for iterOut in range(0, m):
        #     print iterOut
        #     for iterIn in range(iterOut + 1, m):
        #         D[iterIn][iterOut] = D[iterOut][iterIn] = euclideanDist(x[iterOut][0], x[iterOut][1], x[iterIn][0],
        #                                                                 x[iterIn][1])
        sys.setrecursionlimit(100000000)  # 设置递归深度为100,000,000
        D = cPickle.load(open('pointwiseDistance.pkl', 'rb'))
        distOK = True
    except Exception, ex:
        print ex
        print "squareform or pdist error"
        distOK = False
        return


    currentFileNo = None
    nrowsPerFile = 5000

    CD = N.zeros(m)
    RD = N.ones(m) * 1E10

    for i in xrange(m):
        # again you can use the euclid function if you don't want hcluster
        #        d = euclid(x[i],x)
        #        d.sort()
        #        CD[i] = d[k]

        # tempInd = D[i].argsort()
        # tempD = D[i][tempInd]
        # #        tempD.sort() #we don't use this function as it changes the reference
        # CD[i] = tempD[k]  #**2
        # ## the following 2 line will take the place of the above 4 lines
        if currentFileNo is None or i / nrowsPerFile != currentFileNo:
            currentFileNo, D = getPointDistance(i)
        tempD = list(D[i % nrowsPerFile])
        tempD.sort()
        CD[i] = tempD[k]

    order = []
    seeds = N.arange(m, dtype=N.int)

    ind = 0
    while len(seeds) != 1:
        # for seed in seeds:
        ob = seeds[ind]
        seedInd = N.where(seeds != ob)
        seeds = seeds[seedInd]

        order.append(ob)
        tempX = N.ones(len(seeds)) * CD[ob]
        # 此处肯定访问过D，所以nrowsPerFile不可能为None
        if ob / nrowsPerFile != currentFileNo:
            currentFileNo, D = getPointDistance(ob)
        tempD = N.array(D[ob % nrowsPerFile])[seeds]  #[seeds]
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

