from vasptool import OUTCAR

Li = OUTCAR(filename='OUTCAR')

cs = Li.getcs(out=r'cs.csv')
print(cs)
