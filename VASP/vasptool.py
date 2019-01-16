class OUTCAR:

    def __init__(self, filename='OUTCAR'):
        self.filename = filename
        # get text
        self.text = list(open(filename, 'r'))
        # find poscar
        self.poscar = []
        '''
        postcar is inform:
        [['li','4'],['o','2']]
        which represent sequence of elements and their amount
        '''
        for line in self.text:
            if 'POSCAR' in line:
                print(line)
                for comp in line.split():
                    if 'POSCAR' in comp or '=' in comp:
                        continue
                    for i in range(len(comp)):
                        try:
                            a = int(comp[i])
                            self.poscar.append([comp[:i],comp[i:]])
                        except ValueError:
                            pass
                break

    def getcs(self, out):
        print(self.poscar)
        '''
        cs is in form of:
        {1: 'li 2.345',
         2: 'li 2.346',
         3: 'o 16.321',
        }
        '''
        cs = dict()
        # Find start and end
        csStart, csEnd = 0, 0
        for i in range(len(self.text)):
            if '  UNSYMMETRIZED TENSORS \n' == self.text[i]:
                csStart = i
            if '  SYMMETRIZED TENSORS \n' == self.text[i]:
                csEnd = i
                break

        i, tensordia = csStart + 1, 0
        while i < csEnd:
            # get atom id (start from 1)
            atomid = self.text[i].split()[1]
            # add diagonal element of cs tensor
            i += 1
            tensordia += float(self.text[i].split()[0])
            i += 1
            tensordia += float(self.text[i].split()[1])
            i += 1
            tensordia += float(self.text[i].split()[2])
            # log data
            cs.setdefault(int(atomid), str(tensordia/3))
            # move and init
            i += 1
            tensordia = 0

        # merge elements, atomid & cs
        preatom = 0
        for i in range(len(self.poscar)):
            num = int(self.poscar[i][1])
            for j in range(1,num+1):
                cs[preatom+j] = self.poscar[i][0] + ','+cs[preatom+j]
            preatom += num

        # write to file
        if out:
            for i in range(len(cs)):
                t = str(i)+','+cs[i+1]+'\n'
                with open(out, 'a') as f:
                    f.write(t)

        return cs


class INCAR:

    def __init__(self, filename='INCAR'):
        self.filename=filename
        # get text
        self.text = list(open(filename, 'r'))

    def set_key(self, key, value):
        text_to_set = '%s = %s # Set by vasptool\n' % (key, value)
        done = 0
        for i in range(len(self.text)):
            if key in self.text[i]:
                self.text[i] = text_to_set
                done = 1
        if not done:
            self.text.append(text_to_set)

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(''.join(self.text))
                

if __name__ == '__main__':
    pass
