from vasptool import INCAR
import os
import shutil

key = input('Key: ')
values = input('Values (separate by comma ): ').split(',')

model = INCAR() # read model file
model_text = model.text_list

for i in range(len(values)):    # edit INCAR
    if not os.path.exists('%s%s' % (key, values[i])):
        os.makedirs('%s%s' % (key, values[i]))
    future_file = '%s%s/INCAR' % (key, values[i])
    with open(future_file, 'w') as f:
        f.write('')
    inob = INCAR(filename=future_file)
    inob.text_list = model_text
    inob.set_key(key, values[i])
    inob.save()
    print(future_file, 'created.')

for d in os.listdir():  # copy file
    if os.path.isfile(d, ):
        for i in values:
            if d == 'vasp.sh':
                with open(d, 'r') as f:
                    sub = f.read().replace('-J VASP', '-J VASP%s%s' % (key, i))
                with open(d+'_temp', 'w') as f:
                    f.write(sub)
                shutil.copy(d+'_temp', '%s%s/%s'%(key, i, d))
                os.remove(d+'_temp')
            elif d.endswith('.py') or d == 'INCAR':
                pass
            else:
                shutil.copy(d, '%s%s/%s' % (key, i, d))

            print('%s%s/%s' % (key, i, d), 'copied.')

for d in os.listdir(): # submit
    if os.path.isdir(d) and 'INCAR' in os.listdir(d):
        os.system('bsub < %s/vasp.sh'%d)
        print(d, 'submitted.')
