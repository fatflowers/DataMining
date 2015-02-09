import string
import time
import math
import numpy as np

__author__ = 'Administrator'

class Point:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.time = 0.0

class StayPoint:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.arrivalTime = 0.0
        self.leaveTime = 0.0





def gpsDistance2(pi, pj):
    # lonRes = 102900
    lonRes = 102834.74258026089786013677476285
    # latRes = 110000
    latRes = 111712.69150641055729984301412873
    return math.sqrt(abs(pi.latitude - pj.latitude) * latRes * abs(pi.latitude - pj.latitude) * latRes
                     + abs(pi.longitude - pj.longitude) * lonRes * abs(pi.longitude - pj.longitude) * lonRes)

def gpsDistance(pi, pj):
    radLat1 = math.radians(pi.latitude)
    radLat2 = math.radians(pj.latitude)
    a = radLat1 - radLat2;
    b = math.radians(pi.longitude) - math.radians(pj.longitude)

    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) +
                                math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
    EARTH_RADIUS = 6378137
    s *= EARTH_RADIUS
    # s = (s * 10000) / 10000
    return s


def getPointViaString(line):
    point = Point()

    line_element = line.split(',')
    point.latitude = string.atof(line_element[0])
    point.longitude = string.atof(line_element[1])
    point.time = time.mktime(time.strptime(line_element[5] + line_element[6], '%Y-%m-%d%H:%M:%S'))

    return point

def getStayPoints(userTrajectories, DisThreh, TimeThreh):
    listStayPoints = []


    for traj in userTrajectories:
        iteOuter = 0
        aPointList = []
        while iteOuter < len(traj.trajectory):
            # print iteOuter
            iteInner = iteOuter + 1
            while iteInner < len(traj.trajectory):
                if gpsDistance(traj.trajectory[iteOuter], traj.trajectory[iteInner]) > DisThreh:
                    if traj.trajectory[iteInner].time - traj.trajectory[iteOuter].time > TimeThreh:
                        stayPoint = StayPoint()
                        stayPoint.latitude, stayPoint.longitude = meanCoord(traj.trajectory[iteOuter:iteInner+1])
                        stayPoint.arrivalTime = traj.trajectory[iteOuter].time
                        stayPoint.leaveTime = traj.trajectory[iteInner].time
                        aPointList.append(stayPoint)
                    iteOuter = iteInner
                    break
                iteInner += 1
            iteOuter = iteInner
        listStayPoints.append(aPointList)
        # listStayPoints = [listStayPoints, aPointList]

    return listStayPoints



def meanCoord(points):
    latitudes = [0] * len(points)
    longitudes = [0] * len(points)
    for i in range(0, len(points)):
        latitudes[i] = points[i].latitude
        longitudes[i] = points[i].longitude

    return np.mean(np.array(latitudes)), np.mean(np.array(longitudes))

class Point:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.time = 0.0

class StayPoint:
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.arrivalTime = 0.0
        self.leaveTime = 0.0
