from vasptool import INCAR
import os
import shutil

key = input('Key: ')
values = input('Values (separate by ♂): ').split('♂')

model = INCAR() # read model file
model_text = model.text_list

for i in range(len(values)):    # edit INCAR
    path = '%s_%s' % (key, values[i].replace(' ', '_'))
    if not os.path.exists(path):
        os.makedirs(path)
    future_file = '%s/INCAR' % path
    with open(future_file, 'w') as f:
        f.write('')
    inob = INCAR(filename=future_file)
    inob.text_list = model_text
    inob.set_key(key, values[i])
    inob.save()
    print(future_file, 'created.')

for d in os.listdir():  # copy file
    if os.path.isfile(d):
        for i in values:
            path = '%s_%s' % (key, i.replace(' ', '_'))
            if d == 'vasp.sh':
                with open(d, 'r') as f:
                    sub = f.read().replace('-J U0', '-J U0%s%s' % (key, i.replace(' ', '_')))
                with open(d+'_temp', 'w') as f:
                    f.write(sub)
                shutil.copy(d+'_temp', '%s/%s'%(path, d))
                os.remove(d+'_temp')
            elif d.endswith('.py') or d == 'INCAR':
                pass
            else:
                shutil.copy(d, '%s/%s' % (path, d))

            print('%s/%s' % (path, d), 'copied.')

for d in os.listdir(): # submit
    if os.path.isdir(d) and 'INCAR' in os.listdir(d):
        os.system('bsub < %s/vasp.sh' % d)
        print(d, 'submitted.')
