def getCor(string, index):
    if 'END OF INPUT' in string:
        return 'end'
    
    array = string.split()
    element = array[2]
    x = float(array[3])
    y = float(array[4])
    z = float(array[5])
    return [str(index)+element, x, y, z]

def getData(string):
    if string == '\n':
        return 'end'

    array = string.split()
    index = array[0]+array[1]
    iso = float(array[2])
    return [index, iso]

def main(outname, targetname):
    with open(outname, 'r', encoding = 'utf-16-le') as out:
        text_array = out.readlines()
    index = 0
    res = [['index','x','y','z','iso']]

    for i in range(len(text_array)):
        if 'xyz' in text_array[i]:
            for j in range(i+2, len(text_array), 2):
                cor = getCor(text_array[j], index)
                if cor == 'end':
                    break
                res.append(cor)
                index += 1

        if text_array[i].startswith('  Nucleus'):
            for j in range(i+2, len(text_array)):
                data = getData(text_array[j])
                if data == 'end':
                    break
                for k in range(len(res)):
                    if res[k][0] == data[0]:
                        res[k].append(data[1])

    for i in range(len(res)):
        for j in range(len(res[i])):
            res[i][j] = str(res[i][j])

        res[i] = ','.join(res[i])
        res[i] += '\n'

    with open(targetname, 'a') as tar:
        tar.writelines(res)

if __name__ == '__main__':
    outname = input('Output File Name:')
    targetname = input('Target File Name(end with .csv):')
    main(outname, targetname)
