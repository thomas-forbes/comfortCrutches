import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from txtToCsv import listify


groups = ['bio', 'chem', 'thomasHouse', 'tuesday']
subSets = ['ours', 'notours']

interval = 0.5

namesToSubN = {'adrian': 0, 'andrew': 11, 'bree': 2, 'fran': 12, 'hanna': 9, 'issy': 5, 'jack': 6,
               'killian': 7, 'sophie': 8, 'thomas': 4, 'tristan': 10, 'vedh': 1, 'will': 3, 'zoe': 13}


def plotStu(stu):
    medians = []
    for s in subSets:
        for g in groups:
            fileN = f'./{g}/{s}/{stu}.txt'
            if os.path.exists(fileN):
                data = listify(fileN)
                data = [float(x[1]) for x in data]

                plt.plot(np.arange(0, len(data)*interval, interval), data)
                sData = sorted(data)
                median = sData[len(sData)//2]
                medians.append(median)
                # plt.plot(data.index(median), median, 'o')

    try:
        print(medians)
        print((medians[0]-medians[1])/medians[0])
    except:
        pass

    plt.xlabel('Seconds')
    plt.ylabel('Resistance')
    try:
        plt.title(f'Subject {namesToSubN[stu]}')
    except:
        plt.title(f'Subject {stu}')
    plt.legend(['Comfort Crutch',
               'Control'])
    # plt.legend(['Comfort Crutch', 'Comfort Crutch Median',
    #    'Control', 'Control Median'])

    plt.ylim(-1, 120)


# students = []
# for g in groups:
#     students += [x.split('.')[0]
#                  for x in os.listdir(f'./{g}/{subSets[0]}')]
# students.sort()
# print({x: i for i, x in enumerate(students)})

stu = sys.argv[1]
plotStu(stu)
plt.show()
