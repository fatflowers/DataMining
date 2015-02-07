__author__ = 'Administrator'
from UserTrajectory import *
from points import *

import cPickle
a = cPickle.load(open('LocHistory.pkl','rb'))
sum = 0
for i in a:
    sum += len(i.trajectory)
b = 0