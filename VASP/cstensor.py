from vasptool import OUTCAR

Li = OUTCAR(filename='OUTCAR')

cs = Li.getcs_tensor(out=r'cs.csv')
print(cs)
