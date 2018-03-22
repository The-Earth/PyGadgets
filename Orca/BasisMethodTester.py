from os import system
from shutil import copy

def main(func, basis, inp)

    with open(inp,'r') as mod:
        modlist = mod.readlines()

    for i in func:
        for j in basis:
            with open(#r'(directory for calculation input) ./calc/xxx.inp' ,'w') as inp:
                inplist = modlist
                inplist[n] = '! %s %s\n' % (i,j)    #replace n with the number blanked line -1
                inp.writelines(inplist)
            system(#r'(orca path) ./calc/xxx.inp > ./calc/xxx.out')
            copy(#r'./calc/xxx.out', r'./xxx.out')

if __name__ == '__main__':
    func = tuple(input('Functions to be tested (seperated by comma): ').split(','))
    basis = tuple(input('Basis sets to be tested (seperated by comma): ').split(','))
    inp = input('Model file name: ')
    main(func, basis, inp)
