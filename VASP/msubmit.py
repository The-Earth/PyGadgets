import os

for d in os.listdir():  # submit
    if os.path.isdir(d) and 'INCAR' in os.listdir(d):
        os.chdir(d)
        os.system('bsub < vasp.sh')
        print(d, 'submitted.')
        os.chdir('..')
