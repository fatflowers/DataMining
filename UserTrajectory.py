import os
import points
__author__ = 'Administrator'

class UserTrajectory:
    def __init__(self, uid, trajectory):
        self.uid = uid
        self.trajectory = trajectory

def getTrajectory(uid, userDir):
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

def getLocationHistory(DataDir, DisThreh, TimeThreh):
    fileDirs = os.listdir(DataDir)
    LocationHistory = []
    if fileDirs != [] and len(fileDirs) > 0:
        for uid in range(0, len(fileDirs)):
            print DataDir+fileDirs[uid]
            LocationHistory.append(UserTrajectory(uid, points.getStayPoints(getTrajectory(uid, DataDir+fileDirs[uid]), DisThreh, TimeThreh)))

    return LocationHistory

dir = 'D:\\Geolife Trajectories 1.3\\Data\\'
a = getLocationHistory(dir, 200, 20*60*60*1000)
