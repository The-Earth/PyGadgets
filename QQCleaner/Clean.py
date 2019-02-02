import os

cwd = '/storage/emulated/0/tencent/'
os.chdir(cwd)


def listdr(directory):
    rst = []
    for dirs in os.listdir(directory):
        if os.path.isdir(dirs):
            rst.extend(listdr(directory + '/' + dirs))
        rst.append(directory + '/' + dirs)
    return set(rst)


def cldir(directory):
    for d in listdr(directory):
        if 'QQ' in d:
            if os.path.isdir(d):
                try:
                    os.rmdir(d)
                    print(d + ' removed.')
                    continue
                except OSError:
                    cldir(d)

            else:
                os.remove(d)
                print(d + ' removed.')


cldir(cwd)
print('Done!')
