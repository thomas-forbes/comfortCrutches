import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from txtToCsv import listify


# groups = ['bio', 'chem', 'thomasHouse', 'tuesday', 'vedhBeingAnnoying', 'thursday']
groups = ['monday']
subSets = ['ours', 'notours']

interval = 0.5

# namesToSubN = {'adrian': 0, 'andrew': 11, 'bree': 2, 'fran': 12, 'hanna': 9, 'issy': 5, 'jack': 6,
#                'killian': 7, 'sophie': 8, 'thomas': 4, 'tristan': 10, 'vedh': 1, 'will': 3, 'zoe': 13}


def getStudentData(stu):
    out = {'name': stu, 'ours': [], 'notours': [], 'medians': [],
           'median': 'Not enough data for median'}
    for s in subSets:
        for g in groups:
            fileN = f'./{g}/{s}/{stu}.txt'
            if os.path.exists(fileN):
                data = listify(fileN)
                data = [float(x[1]) for x in data]

                out[s] = data

                sData = sorted(data)
                median = sData[len(sData)//2]
                out['medians'].append(median)

    try:
        out['median'] = (out['medians'][0]-out['medians'][1])/out['medians'][0]
    except:
        pass
    return out


def plotStu(stu):
    data = getStudentData(stu)
    # medians = data['medians']

    for s in subSets:
        plt.plot(np.arange(0, len(data[s])*interval, interval), data[s])
    print(data['medians'], '\n', data['median'])

    plt.xlabel('Seconds')
    plt.ylabel('Resistance')
    plt.title(f'Subject {stu}')
    plt.legend(['Comfort Crutch',
               'Control'])
    plt.ylim(-1, 120)


def plotMedians():
    students = []
    for g in groups:
        students += [x.split('.')[0]
                     for x in os.listdir(f'./{g}/{subSets[0]}')]
    students.sort()

    sData = []
    for stu in students:
        stuD = getStudentData(stu)
        sData.append(stuD)

    sData.sort(key=lambda x: -float('inf')
               if type(x['median']) is str else x['median'], reverse=True)
    for i, s in enumerate(sData):
        print(s['median'], s['name'])
        if type(s['median']) is not str:
            plt.plot(i, s['median'], 'ro')

    plt.ylim(-1, 1)
    # print({x: i for i, x in enumerate(students)})


stu = sys.argv[1]
plotStu(stu)
plt.show()
