from vasptool import INCAR
import os

key = input('Key: ')
values = input('Values (separate by comma ): ').split(',')

model = INCAR() # read model file
model_text = model.text_list()

for i in range(len(values)):    # edit INCAR
    os.makedirs('%s%s' % (key, values[i]))
    future_file = '%s%s/INCAR' % (key, values)
    with open(future_file, 'w') as f:
        f.write('')
    inob = INCAR(filename=future_file)
    inob.text_list = model_text
    inob.set_key(key, values[i])
    inob.save()
    print(future_file, 'created.')

for d in os.listdir():  # submit
    if os.path.isdir(d):
        if 'INCAR' in os.listdir(d):
            os.system('bsub < vasp.sh')
            print(d, 'submitted.')
