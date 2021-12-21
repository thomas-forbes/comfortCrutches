from click.decorators import option
import matplotlib.pyplot as plt
import numpy as np
import logging
import os
from optparse import OptionParser
from txtToCsv import listify


groups = ['tuesday']
subSets = ['ours', 'notours']

interval = 0.5

students = []
for g in groups:
    students += [x.split('.')[0]
                 for x in os.listdir(f'./{g}/{subSets[0]}')]
students.sort()


def getStudentData(stu):
    out = {'name': stu, 'ours': [], 'notours': [], 'medians': [],
           'median': 'Not enough data for median'}
    for s in subSets:
        for g in groups:
            fileN = f'./{g}/{s}/{stu}.txt'
            if os.path.exists(fileN):
                data = listify(fileN)
                data = [float(x[1]) for x in data]

                logging.debug(data)
                out[s] = data

                sData = sorted(data)
                median = sData[len(sData)//2]
                out['medians'].append(median)

    try:
        out['median'] = (out['medians'][0]-out['medians'][1])/out['medians'][0]
    except:
        pass
    return out


def getStudentsData():
    sData = []
    for stu in students:
        stuD = getStudentData(stu)
        sData.append(stuD)
    return sData


# Plotting funcs
def plotStu(stu):
    data = getStudentData(stu)

    for s in subSets:
        plt.plot(np.arange(0, len(data[s])*interval, interval), data[s])
    logging.info(data['medians'])
    logging.info(data['median'])

    plt.xlabel('Seconds')
    plt.ylabel('Resistance')
    plt.title(f'Subject {stu}')
    plt.legend(['Comfort Crutch',
               'Control'])
    plt.ylim(-1, 120)


# Plots the medians of each student and a line of the
def plotMedians():
    sData = getStudentsData()
    sData.sort(key=lambda x: -float('inf')
               if type(x['median']) is str else x['median'], reverse=True)

    meds = []
    for i, s in enumerate(sData):
        logging.debug(s['median'], s['name'])
        if type(s['median']) is not str:
            plt.plot(i, s['median'], 'ro')
            meds.append(s['median'])
    plt.plot(range(len(meds)), [sum(meds) / len(meds)] * len(meds), lw=3)

    plt.ylim(-1, 1)


# Setup logging
logging.basicConfig(level=logging.INFO)

# Setup Arg options
parser = OptionParser()
parser.add_option('-n', dest='useN', default=False,
                  action='store_true', help='use newtons')
parser.add_option('-s', dest='stu', help='Name of student')
parser.add_option('-m', dest='doMedians', default=False,
                  action='store_true', help='Plot medians instead')
parser.add_option('-P', dest='doPlot', default=True,
                  action='store_false', help='Do not show plot')

# Check options
(options, args) = parser.parse_args()
stu = options.stu
USE_NEWTONS = options.useN

# Run funcs
if options.doMedians:
    plotMedians()
elif stu in students:
    plotStu(stu)
else:
    parser.print_help()


if options.doPlot:
    plt.show()
