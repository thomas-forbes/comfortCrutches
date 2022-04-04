import json
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

# important variables
groups = ['tuesday']
subSets = ['ours', 'notours']
subSetColours = ['blue', 'red']

# Time interveral between readings
interval = 0.5

# Creates an array
students = []
for g in groups:
    students += [x.split('.')[0]
                 for x in os.listdir(f'./{os.path.dirname(__file__)}/{g}/{subSets[0]}')]
students.sort()

# Removes certain students from students array. August and ruby were before proper testing methods and connor we redid.
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
        # also checks making sure value is greater than -1 resistance and less than 0 newtons
        return [((a*x+b)*9.8)/SENSOR_AREA for x in data if x > -1 and x < zNinOhms]
    else:
        # This func runs every time but only converst when use_pascals flag is set
        return [x for x in data if x > -1 and x < zNinOhms]


# Returns dict with data for specified student with props: name, ours, notours, medians, and percentDiff
def getStudentData(stu):
    out = {'name': stu, 'ours': [], 'notours': [], 'medians': [],
           'percentDiff': 'Not enough data for median'}
    # Finds student
    for s in subSets:
        for g in groups:
            # Finds student if file path exists
            fileN = f'./{os.path.dirname(__file__)}/{g}/{s}/{stu}.txt'
            if os.path.exists(fileN):
                # Gets data from txtToCsv.py
                data = listify(fileN)
                # Changes from str to float
                data = [float(x[1]) for x in data]

                # logger.debug(data)
                # Doesn't convert if USE_PASCALS is false
                data = convertToPascals(data)
                out[s] = data

                # creates temp sData to get median
                sData = sorted(data)
                median = sData[len(sData)//2]
                out['medians'].append(median)

    try:
        # Throws error if student is missing a data set
        # Swaps between use_pascals bc resistance -> pascals is inverse so increase in resistance is decrease in pascals
        if USE_PASCALS:
            out['percentDiff'] = (
                out['medians'][1]-out['medians'][0])/out['medians'][1]
        else:
            out['percentDiff'] = (
                out['medians'][0]-out['medians'][1])/out['medians'][0]
    except:
        # Keeps percentDiff as a str
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

    # Plots the specific colour for each subset (our, notours)
    for s, c in zip(subSets, subSetColours):
        # np.arrange thing just gets the x axis in correct time intervals
        plt.plot(np.arange(0, len(data[s]) *
                           interval, interval), data[s], color=c)
    logger.info(data['medians'])
    logger.info(data['percentDiff'])

    subToNum = {'fran': 1, 'emily': 2}
    # If you're trying to plot a student not in dict then it will throw error and go to except
    try:
        plt.title(f'Subject {subToNum[stu]}')
    except:
        plt.title(f'Subject {stu}')

    # Plotting stuff
    plt.xlabel('Seconds')
    plt.legend(['Comfort Crutch',
                'Standard Crutch'])
    # Change labels based on params
    if USE_PASCALS:
        plt.ylabel('Kilopascals')
        plt.ylim(-1, convertToPascals([0])[0])
    else:
        plt.ylabel('Resistance')
        plt.ylim(-1, 120)


# Plots the percentage difference or real difference of each student and a line of the average
def plotDifferences(doPerc):
    # Pretty confusing
    sData = getStudentsData()

    # If showing percentages or real differences
    if doPerc:
        # Sorts the data but doesn't remove the strs
        sData.sort(key=lambda x: -float('inf')
                   if type(x['percentDiff']) is str else x['percentDiff'], reverse=True)
        # Removes strs. It's a str if there isn't data for either standard or comfort crutches
        inData = [{'data': x['percentDiff'], 'name': x['name']}
                  for x in sData if type(x['percentDiff']) is not str]
    # We didn't really use real difference. only really for averages and SDs of all students
    else:
        # Sorts by real difference
        sData.sort(key=lambda x: abs(
            x['medians'][0] - x['medians'][1]), reverse=True)
        # Rounds the difference and makes it positive.
        inData = [{'data': round(abs(x['medians'][0] - x['medians'][1]), 2),
                   'name': x['name']} for x in sData]
        a, b = np.array([]), np.array([])
        for i in sData:
            a = np.append(a, i['medians'][0])
            b = np.append(b, i['medians'][1])
        # Logs averages and medians for pascals for all students
        logger.info(
            f'{np.average(a)}, {np.std(a)}, {np.average(b)}, {np.std(b)}')

    # Takes inData and plots it. also creating outData
    outData = []
    for i, s in enumerate(inData):
        logger.debug(f"{s['data']}, {s['name']}")
        plt.plot(i, s['data'], 'ro')
        outData.append(s['data'])

    mean = sum(outData) / len(outData)
    # median = outData[len(outData)//2]

    logger.info(f'mean:{mean}')

    # Plotting stuff
    plt.plot(range(len(outData)), [mean] * len(outData), lw=2)
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
parser.add_option('--all-data-json', dest='allData',
                  help='Returns json text', default=False, action='store_true')
# Check options
(options, args) = parser.parse_args()

stu = options.stu
USE_PASCALS = options.usePascals
SENSOR_AREA = 0.14  # n/mm^2 = MPa. Sensor area = 1.4 * 10^-4 m^2. We are getting KPa

if options.allData:
    print(json.dumps(getStudentsData()))
    exit(0)

# Run funcs
if options.doDiff:
    plotDifferences(options.doPerc)
elif stu in students:
    plotStu(stu)
else:
    parser.print_help()

# Will download image and place them into images/final
if options.download:
    if stu != None:
        plt.savefig(f'./{os.path.dirname(__file__)}/images/final/{stu}.jpg')
    else:
        plt.savefig(
            f'./{os.path.dirname(__file__)}/images/final/differences.jpg')
    options.doPlot = False

# Bash command to download certain students
# for s in stu1 ... stuN; do python3 plotter.py -s $s --download; done

# fran emily

# For --noPlot flag when just looking at data output
if options.doPlot:
    plt.show()
