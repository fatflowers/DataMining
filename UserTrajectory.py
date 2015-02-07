#-*- coding:GBK -*-
import os
import points
import cPickle

__author__ = 'Administrator'

class UserTrajectory:
    def __init__(self, uid, trajectory):
        self.uid = uid
        self.trajectory = trajectory

def getTrajectory_old(uid, userDir):
    Trajectory = []

    # global Trajectory
    userDir += "\\Trajectory\\"
    fileDirs = os.listdir(userDir)
    if fileDirs != [] and len(fileDirs) > 0:
        for dir in fileDirs:
            file = open(userDir + dir)
            try:
                allTheText = file.read().split('\n')[6:-1]
                # Trajectory = [points.Point()] * len(allTheText)
            finally:
                file.close()
            for iterText in range(0, len(allTheText)):
                Trajectory.append(points.getPointViaString(allTheText[iterText]))

    return UserTrajectory(uid, Trajectory)


def getAllTheText(fileDir):
    file = open(fileDir)
    try:
        allTheText = file.read().split('\n')[6:-1]
        # Trajectory = [points.Point()] * len(allTheText)
    finally:
        file.close()
    return allTheText


def parsePltFile(fileDir):
    file = open(fileDir)
    pointSet = []
    try:
        allTheText = file.read().split('\n')[6:-1]
        # Trajectory = [points.Point()] * len(allTheText)
    finally:
        file.close()
    for iterText in range(0, len(allTheText)):
        pointSet.append(points.getPointViaString(allTheText[iterText]))
    return pointSet

"""
Return a list of trajectory for a certain user.
"""
def getTrajectory(uid, userDir, DisThreh, TimeThreh):
    Trajectory = []
    pointSet = []
    # global Trajectory
    userDir += "\\Trajectory\\"
    fileDirs = os.listdir(userDir)

    lastFileLastLine = None
    dir = 0
    if fileDirs != [] and len(fileDirs) > 0:
        while dir < len(fileDirs):
            pointSet = parsePltFile(userDir + fileDirs[dir])
            addFile = 1
            while True: #and dir + addFile < len(fileDirs):# 加上时间条件
                if dir + addFile >= len(fileDirs):
                    dir = dir + addFile
                    break
                tmpFile = open(userDir + fileDirs[dir + addFile])
                tmpPoint = points.getPointViaString(tmpFile.read().split('\n')[6])
                tmpFile.close()
                if points.gpsDistance(pointSet[-1], tmpPoint) > DisThreh and tmpPoint.time - pointSet[-1].time > TimeThreh:
                    dir = dir + addFile
                    break
                pointSet += parsePltFile(userDir + fileDirs[dir + addFile])
                # pointSet.append(parsePltFile(userDir + fileDirs[dir + addFile]))
                addFile += 1

            Trajectory.append(UserTrajectory(uid, pointSet))
            # if addFile == 1:
            #     dir += 1
    return Trajectory


def getLocationHistory(DataDir, DisThreh, TimeThreh):
    fileDirs = os.listdir(DataDir)
    LocationHistory = []
    if fileDirs != [] and len(fileDirs) > 0:
        for uid in range(0, len(fileDirs)):
            print DataDir+fileDirs[uid]
            LocationHistory.append(UserTrajectory(uid, points.getStayPoints(getTrajectory(uid, DataDir+fileDirs[uid], DisThreh, TimeThreh), DisThreh, TimeThreh)))

    return LocationHistory

dir = 'D:\\Geolife Trajectories 1.3\\Data\\'
a = getLocationHistory(dir, 200, 20*60)
cPickle.dump(a, open("LocHistory.pkl", "wb"))

