import sys
import os
import csv


# Takes a file and returns array with data
def listify(fileN):
    # Reads file
    with open(fileN, 'r') as f:
        lines = f.readlines()
        f.close()
    data = []
    onZStart = True
    for line in lines:
        l = line.split(' ')
        # We are looing for lines with R = NUM and they have 5 spaces
        if len(l) == 5:
            val = float(l[-1].strip('\n'))
            # Removes entries rom start if they are less than 0 so data lines up when compared
            # 0 means max pressure and -1 means unconnected. Could result in 0 if velostat not connected properly
            if not onZStart or onZStart and val > 0:
                onZStart = False
                data.append([l[0], val])
    return data


# Creates csv of data if file is run by it self.
if __name__ == '__main__':
    fileName = sys.argv[1]
    data = listify(fileName)
    newN = fileName.split('.')[0] + '.csv'
    with open(newN, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        f.close()

    print(f'Finished: {os.path.dirname(__file__)}/{newN}')
