from os import system
from shutil import copy

def main(func, basis, inp)

    with open(inp,'r') as mod:
        modlist = mod.readlines()

    for i in func:
        for j in basis:
            with open(#r'(directory for calculation input)' ,'w') as inp:
                inplist = modlist
                inplist[n] = '! %s %s\n' % (i,j)    #replace n with the number of blanked line
                inp.writelines(inplist)
            #system(r'(orca path) ./calc/xxx_%s_%s.inp > ./calc/xxx_%s_%s.out' %(i,j,i,j))
            #copy(#r'./calc/xxx_%s%s.out'%(i,j), r'./xxx_%s_%s.out'%(i,j))

if __name__ == '__main__':
    func = tuple(input('Functions to be tested (seperated by comma): ').split(','))
    basis = tuple(input('Basis sets to be tested (seperated by comma): ').split(','))
    inp = input('Model file name: ')
    main(func, basis, inp)
