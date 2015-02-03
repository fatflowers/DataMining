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

def gpsDistance(pi, pj):
    lonRes = 102900
    latRes = 110000
    return math.sqrt(abs(pi.latitude - pj.latitude) * latRes * abs(pi.latitude - pj.latitude) * latRes
                     + abs(pi.longitude - pj.longitude) * lonRes * abs(pi.longitude - pj.longitude) * lonRes)


def getPointViaString(line):
    point = Point()

    line_element = line.split(',')
    point.latitude = string.atof(line_element[0])
    point.longitude = string.atof(line_element[1])
    point.time = time.mktime(time.strptime(line_element[5] + line_element[6], '%Y-%m-%d%H:%M:%S'))

    return point

def getStayPoints(points, DisThreh, TimeThreh):
    listStayPoints = []
    stayPoint = StayPoint()
    iteOuter = 0
    while iteOuter < len(points):
        iteInner = iteOuter + 1
        while iteInner < len(points):
            if gpsDistance(points[iteOuter], points[iteInner]) > DisThreh:
                if points[iteInner].time - points[iteOuter].time > TimeThreh:
                    stayPoint.latitude, stayPoint.longitude = meanCoord(points[iteOuter:iteInner+1])
                    stayPoint.arrivalTime = points[iteOuter].time
                    stayPoint.leaveTime = points[iteInner].time
                    listStayPoints.append(stayPoint)
                iteOuter = iteInner
                break

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
