import sys
import csv


def listify(fileN):
    with open(fileN, 'r') as f:
        lines = f.readlines()
        f.close()
    data = []
    onZStart = True
    for line in lines:
        l = line.split(' ')
        if len(l) == 5:
            val = float(l[-1].strip('\n'))
            if not onZStart or onZStart and val > 0:
                onZStart = False
                data.append([l[0], val])
    return data


if __name__ == '__main__':
    fileName = sys.argv[1]
    data = listify(fileName)
    newN = fileName.split('.')[0] + '.csv'
    with open(newN, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        f.close()

    print(f'Finished: ./{newN}')
