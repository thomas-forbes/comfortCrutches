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
subSetColours = ['blue', 'red']

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
    ohms = np.array([120, 108, 95, 83, 70.5, 58.1,
                     45.7, 33.3, 20.9, 8.5, -3.9])
    kg = np.array([1.5, 2.5, 3.5, 4.5, 5.5, 6.5,
                   7.5, 8.5, 9.5, 10.5, 11.5])

    a, b = np.polyfit(ohms, kg, 1)
    zNinOhms = -b/a  # Zero Newtons in ohms
    if USE_NEWTONS:
        return [(a*x+b)*9.8 for x in data if x > -1 and x < zNinOhms]
    else:
        return [x for x in data if x > -1 and x < zNinOhms]


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
        if USE_NEWTONS:
            out['percentDiff'] = (
                out['medians'][1]-out['medians'][0])/out['medians'][1]
        else:
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

    for s, c in zip(subSets, subSetColours):
        plt.plot(np.arange(0, len(data[s]) *
                           interval, interval), data[s], color=c)
    logger.info(data['medians'])
    logger.info(data['percentDiff'])

    subToNum = {'fran': 1, 'emily': 2}
    plt.xlabel('Seconds')
    plt.title(f'Subject {subToNum[stu]}')
    plt.legend(['Comfort Crutch',
                'Control'])

    if USE_NEWTONS:
        plt.ylabel('Newtons')
        plt.ylim(-1, convertToN([0])[0])
    else:
        plt.ylabel('Resistance')
        plt.ylim(-1, 120)


# Plots the medians of each student and a line of the
def plotDifferences(doPerc):
    sData = getStudentsData()

    if doPerc:
        sData.sort(key=lambda x: -float('inf')
                   if type(x['percentDiff']) is str else x['percentDiff'], reverse=True)
        inData = [{'data': x['percentDiff'], 'name': x['name']}
                  for x in sData if type(x['percentDiff']) is not str]
        plt.ylim(-1, 1)
    else:
        sData.sort(key=lambda x: abs(
            x['medians'][0] - x['medians'][1]), reverse=True)
        inData = [{'data': round(abs(x['medians'][0] - x['medians'][1]), 2),
                   'name': x['name']} for x in sData]

    outData = []
    for i, s in enumerate(inData):
        logger.debug(f"{s['data']}, {s['name']}")
        plt.plot(i, s['data'], 'ro')
        outData.append(s['data'])

    mean = sum(outData) / len(outData)
    median = outData[len(outData)//2]
    logger.info(f'mean:{mean}')
    logger.info(f'median:{median}')

    plt.plot(range(len(outData)), [mean] * len(outData), lw=3)
    plt.plot(range(len(outData)), [median] * len(outData), lw=3)


# Setup Arg options
parser = OptionParser()
parser.add_option('-n', dest='useN', default=False,
                  action='store_true', help='use newtons')
parser.add_option('-s', dest='stu', help='Name of student')
parser.add_option('-d', dest='doDiff', default=False,
                  action='store_true', help='Plot percentages including mean, median instead')
parser.add_option('-R', dest='doPerc', default=True,
                  action='store_false', help='Plot actual differences instead of percentages (must use -d)')
parser.add_option('-P', dest='doPlot', default=True,
                  action='store_false', help='Do not show plot')
parser.add_option('--download', dest='download', default=False,
                  action='store_true', help='Downloads student graph or all')
# Check options
(options, args) = parser.parse_args()
stu = options.stu
USE_NEWTONS = options.useN

# Run funcs
if options.doDiff:
    plotDifferences(options.doPerc)
elif stu in students:
    plotStu(stu)
    if options.download:
        plt.savefig(f'./images/final/{stu}.jpg')
        options.doPlot = False
else:
    parser.print_help()

# Bash command to download certain students
# for s in stu1 ... stuN; do python3 plotter.py -s $s --download; done

# fran emily

if options.doPlot:
    plt.show()
