from os import system
from shutil import copy


def main(basisSet, methodSet, orcaPath, rootName, modelFile, calcPath, blankLine):
    modelTextList = list(open('%s%s' % (rootName, modelFile), 'r'))

    if modelTextList[blankLine - 1] != '\n':
        raise Exception('检查：指定的空行不为空')

    for i in basisSet:
        for j in methodSet:
            modelTextList[blankLine - 1] = '! %s %s\n' % (i, j)
            calcName = '%s%s%s_%s_%s.inp' % (rootName, calcPath, modelFile, i, j)
            with open(calcName, 'w') as calcInp:
                calcInp.write(''.join(modelTextList))

            system('%s %s > %s' % (orcaPath, calcName, calcName.replace('.inp', '.out')))
            copy(calcName.replace('.inp', '.out'), rootName)


if __name__ == '__main__':
    basisSet = tuple(input('Basis Set (Separate each one with comma(,)): ').split(','))
    methodSet = tuple(input('Method (Separate each one with comma(,)): ').split(','))
    orcaPath = input(r'Directory of ORCA executable file (e.g. C:\orca\orca.exe): ')
    rootName = input('Directory of the inp file as a model: ')
    modelFile = input('Name of the inp file as a model: ')
    calcPath = input(r'Directory to be used for calculation: (Should be started AND ended with \ or /): ')
    blankLine = int(input('Line NO. of a blank line ready for insert basis and method: '))

    main(basisSet=basisSet, methodSet=methodSet, orcaPath=orcaPath, modelFile=modelFile, calcPath=calcPath,
         blankLine=blankLine, rootName=rootName)
