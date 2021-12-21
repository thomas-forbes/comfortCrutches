from click.decorators import option
import matplotlib.pyplot as plt
import numpy as np
import logging
import os
from optparse import OptionParser
from txtToCsv import listify

# Setup logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

groups = ['tuesday']
subSets = ['ours', 'notours']

interval = 0.5

students = []
for g in groups:
    students += [x.split('.')[0]
                 for x in os.listdir(f'./{g}/{subSets[0]}')]
students.sort()

# Ignored Reasons
"""
Connor: we did him again and different results after making the positioning better.
August + Ruby: We did them before we noticed the positioning better and improved our instructions.
"""
ignoredStudents = ['august', 'connor', 'ruby']  # , 'maisieT', 'liamH', 'zoe']
students = [s for s in students if s not in ignoredStudents]


def convertToN(data):
    if USE_NEWTONS:
        ohms = np.array([120, 108, 95, 83, 70.5, 58.1,
                         45.7, 33.3, 20.9, 8.5, -3.9])
        kg = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5,
                       7.5, 8.5, 9.5, 10.5, 11.5])

        a, b = np.polyfit(ohms, kg, 1)
        return [a*x+b for x in data]
    else:
        return data


def getStudentData(stu):
    out = {'name': stu, 'ours': [], 'notours': [], 'medians': [],
           'percentDiff': 'Not enough data for median'}
    for s in subSets:
        for g in groups:
            fileN = f'./{g}/{s}/{stu}.txt'
            if os.path.exists(fileN):
                data = listify(fileN)
                data = [float(x[1]) for x in data]

                # logger.debug(data)
                # Doesn't convert if USE_NEWTONS is false
                data = convertToN(data)
                out[s] = data

                sData = sorted(data)
                median = sData[len(sData)//2]
                out['medians'].append(median)

    try:
        out['percentDiff'] = (
            out['medians'][0]-out['medians'][1])/out['medians'][0]
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
    logger.info(data['medians'])
    logger.info(data['percentDiff'])

    plt.xlabel('Seconds')
    plt.title(f'Subject {stu}')
    plt.legend(['Comfort Crutch',
                'Control'])

    if USE_NEWTONS:
        plt.ylabel('Newtons')
        # plt.ylim(-1, convertToN([120])[0])
    else:
        plt.ylabel('Resistance')
        plt.ylim(-1, 120)


# Plots the medians of each student and a line of the
def plotPercentages():
    sData = getStudentsData()
    sData.sort(key=lambda x: -float('inf')
               if type(x['percentDiff']) is str else x['percentDiff'], reverse=True)

    percents = []
    for i, s in enumerate(sData):
        logger.debug(f"{s['percentDiff']}, {s['name']}")
        if type(s['percentDiff']) is not str:
            plt.plot(i, s['percentDiff'], 'ro')
            percents.append(s['percentDiff'])

    meanPerc = sum(percents) / len(percents)
    medianPerc = percents[len(percents)//2]
    logger.info(f'mean:{meanPerc}')
    logger.info(f'median:{medianPerc}')

    plt.plot(range(len(percents)), [meanPerc] * len(percents), lw=3)
    plt.plot(range(len(percents)), [medianPerc] * len(percents), lw=3)
    plt.ylim(-1, 1)


# Setup Arg options
parser = OptionParser()
parser.add_option('-n', dest='useN', default=False,
                  action='store_true', help='use newtons')
parser.add_option('-s', dest='stu', help='Name of student')
parser.add_option('-m', dest='doPerc', default=False,
                  action='store_true', help='Plot percentages including mean, median instead')
parser.add_option('-P', dest='doPlot', default=True,
                  action='store_false', help='Do not show plot')

# Check options
(options, args) = parser.parse_args()
stu = options.stu
USE_NEWTONS = options.useN

# Run funcs
if options.doPerc:
    plotPercentages()
elif stu in students:
    plotStu(stu)
else:
    parser.print_help()


if options.doPlot:
    plt.show()
