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

ignoredStudents = ['august', 'connor', 'ruby']
students = [s for s in students if s not in ignoredStudents]


# Takes and array of values in Ohms and returns it in pascals
def convertToPascals(data):
    # This are the reading vedh gave me
    # They plot linearly for this range
    ohms = np.array([120, 108, 95, 83, 70.5])
    kg = np.array([1.5, 2.5, 3.5, 4.5, 5.5])

    # Code for creating graph of ohms -> kg relationship
    # plt.xlabel('Ohms')
    # plt.ylabel('KG')
    # plt.title('Sensor Calibration')
    # plt.plot(ohms, kg)
    # plt.show()

    # Creates coefficients for a linear func in form kg=a*ohms+b
    # its called line of best fit or fitting if you wanna search it up
    a, b = np.polyfit(ohms, kg, 1)
    # print(a, b)
    zNinOhms = -b/a  # Finds the value in ohms for 0 newtons.
    if USE_PASCALS:
        # a*x+b = kg then * 9.8 for newtons then /sensor_area for pascals

        # I changed decimal point on sensor area so we get KPa. It should be 10^-3 more
        # but if we take them off we get 10^3 on pascals which gives us kilopascals. kilo=1000
        # also checks making sure value is within -1 0 newtons
        return [((a*x+b)*9.8)/SENSOR_AREA for x in data if x > -1 and x < zNinOhms]
    else:
        return [x for x in data if x > -1 and x < zNinOhms]


# Returns dict with data for specified student with props: name, ours, notours, medians, and percentDiff
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
                # Doesn't convert if USE_PASCALS is false
                data = convertToPascals(data)
                out[s] = data

                sData = sorted(data)
                median = sData[len(sData)//2]
                out['medians'].append(median)

    try:
        if USE_PASCALS:
            out['percentDiff'] = (
                out['medians'][1]-out['medians'][0])/out['medians'][1]
        else:
            out['percentDiff'] = (
                out['medians'][0]-out['medians'][1])/out['medians'][0]
    except:
        pass
    return out


# Returns an array with data for all students
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
    try:
        plt.title(f'Subject {subToNum[stu]}')
    except:
        plt.title(f'Subject {stu}')
    plt.legend(['Comfort Crutch',
                'Standard Crutch'])

    if USE_PASCALS:
        plt.ylabel('Kilopascals')
        plt.ylim(-1, convertToPascals([0])[0])
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
        # plt.ylim(-1, 1)
    else:
        sData.sort(key=lambda x: abs(
            x['medians'][0] - x['medians'][1]), reverse=True)
        inData = [{'data': round(abs(x['medians'][0] - x['medians'][1]), 2),
                   'name': x['name']} for x in sData]
        a, b = np.array([]), np.array([])
        for i in sData:
            # print(i['medians'], i['name'])
            a = np.append(a, i['medians'][0])
            b = np.append(b, i['medians'][1])
        logger.info(
            f'{np.average(a)}, {np.std(a)}, {np.average(b)}, {np.std(b)}')

    outData = []
    for i, s in enumerate(inData):
        logger.debug(f"{s['data']}, {s['name']}")
        plt.plot(i, s['data'], 'ro')
        outData.append(s['data'])

    mean = sum(outData) / len(outData)
    median = outData[len(outData)//2]
    logger.info(f'mean:{mean}')
    logger.info(f'median:{median}')

    plt.plot(range(len(outData)), [mean] * len(outData), lw=2)
    # plt.plot(range(len(outData)), [median] * len(outData), lw=3)
    plt.title('Percentage Decreases')
    plt.xlabel('Test Subject')
    plt.ylabel('Percentage 0-1')


# Setup Arg options
parser = OptionParser()
parser.add_option('-p', dest='usePascals', default=False,
                  action='store_true', help='use pascals. Uses KPa')
parser.add_option('-s', dest='stu', help='Name of student')
parser.add_option('-d', dest='doDiff', default=False,
                  action='store_true', help='Plot percentages including mean, median instead')
parser.add_option('-R', dest='doPerc', default=True,
                  action='store_false', help='Plot actual differences instead of percentages (must use -d)')
parser.add_option('--noPlot', dest='doPlot', default=True,
                  action='store_false', help='Do not show plot')
parser.add_option('--download', dest='download', default=False,
                  action='store_true', help='Downloads the graph that would be shown')
# Check options
(options, args) = parser.parse_args()
stu = options.stu
USE_PASCALS = options.usePascals
SENSOR_AREA = 0.14  # n/mm^2 = MPa. We are getting KPa

# Run funcs
if options.doDiff:
    plotDifferences(options.doPerc)
elif stu in students:
    plotStu(stu)
else:
    parser.print_help()

if options.download:
    if stu != None:
        plt.savefig(f'./images/final/{stu}.jpg')
    else:
        plt.savefig(f'./images/final/differences.jpg')
    options.doPlot = False

# Bash command to download certain students
# for s in stu1 ... stuN; do python3 plotter.py -s $s --download; done

# fran emily

if options.doPlot:
    plt.show()
