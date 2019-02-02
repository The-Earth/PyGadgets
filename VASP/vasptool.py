class OUTCAR:

    def __init__(self, filename='OUTCAR'):
        self.filename = filename
        # get text
        self.text_list = list(open(filename, 'r'))
        # find poscar
        self.poscar = []
        '''
        poscar is inform:
        [['li','4'],['o','2']]
        which represent sequence of elements and their amount
        '''
        for line in self.text_list:
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

    def getcs_tensor(self, out=None):
        """
        cs is in form of:
        {1: 'li 2.345',
         2: 'li 2.346',
         3: 'o 16.321',
        }
        """
        cs = dict()
        # Find start and end
        csStart, csEnd = 0, 0
        for i in range(len(self.text_list)):
            if '  UNSYMMETRIZED TENSORS \n' == self.text_list[i]:
                csStart = i
            if '  SYMMETRIZED TENSORS \n' == self.text_list[i]:
                csEnd = i
                break

        i, tensordia = csStart + 1, 0
        while i < csEnd:
            # get atom id (start from 1)
            atomid = self.text_list[i].split()[1]
            # add diagonal element of cs tensor
            i += 1
            tensordia += float(self.text_list[i].split()[0])
            i += 1
            tensordia += float(self.text_list[i].split()[1])
            i += 1
            tensordia += float(self.text_list[i].split()[2])
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

    def get_Afc(self, out=None):
        start, A_tot_list = -1, dict()
        for i in range(len(self.text_list)):
            if 'Fermi contact (isotropic) hyperfine coupling parameter (MHz)' in self.text_list[i]:
                start = i + 4
                break

        if start == -1:
            raise Exception('Fermi contact A not found in OUTCAR')
        i = start
        while not '--' in self.text_list[i].split()[0]:
            A_tot_list[int(self.text_list[i].split()[0])] = float(self.text_list[i].split()[5])
            i += 1

        if out:
            with open(out, 'a') as f:
                f.write('\natom index,A_tot\n')
            for i in range(len(A_tot_list)):
                t = '%s,%s\n' % (str(i+1), str(A_tot_list[i+1]))
                with open(out, 'a') as f:
                    f.write(t)

        return A_tot_list


class INCAR:

    def __init__(self, filename='INCAR'):
        self.filename=filename
        # get text
        try:
            self.text_list = list(open(filename, 'r'))
        except FileNotFoundError:
            self.text_list = list()

    def set_key(self, key, value):
        text_to_set = '\n%s = %s # Set by vasptool\n' % (key, value)
        done = 0
        for i in range(len(self.text_list)):
            if key in self.text_list[i]:
                self.text_list[i] = text_to_set
                done = 1
                break
        if not done:
            self.text_list.append(text_to_set)

    def save(self):
        with open(self.filename, 'w') as f:
            f.write(''.join(self.text_list))

    def save_as(self, target):
        with open(target, 'w') as f:
            f.write(''.join(self.text_list))


class POSCAR:

    def __init__(self, filename='POSCAR'):
        self.filename = filename
        self.text_list = list(open(filename, 'r'))
        self.len = len(self.text_list)
        self.atoms = self.text_list[5].split()
        self.atoms_num = self.text_list[6].split()
        self.cord_type = self.text_list[7].strip()[0]
        # Verify POSCAR
        if len(self.atoms) != len(self.atoms_num):
            raise IndexError("POSCAR: Line 7 doesn't match line 6.")
        for i in range(len(self.atoms_num)):
            self.atoms_num[i] = int(self.atoms_num[i])
        if sum(self.atoms_num) != self.len - 8:
            raise IndexError("POSCAR: Positions doesn't match numbers defined in line 7.")

    def get_num_dict(self):
        """
        :return: A dict with elements as key and numbers of them as value. {'Li'":2, 'O':4}
        """
        num_dict = dict()
        for i in range(len(self.atoms)):
            num_dict[self.atoms[i]] = self.atoms_num[i]
        return num_dict

    def get_full_pos(self, out=None):
        """
        :return: A dict containing all atoms and their position.
        Positions are in tuple and in form of coordinate type defined in POSCAR
        """
        from collections import OrderedDict
        line_id = 8
        pos_dic = OrderedDict()
        for i in range(len(self.atoms)):
            for j in range(self.atoms_num[i]):
                a = float(self.text_list[line_id].split()[0])
                b = float(self.text_list[line_id].split()[1])
                c = float(self.text_list[line_id].split()[2])
                pos_dic[line_id-7] = (self.atoms[i], a, b, c)
                line_id += 1

        if out:
            with open(out, 'a') as f:
                f.write('\natom,element,a,b,c\n')
            for ele in pos_dic:
                element = pos_dic[ele][0]
                a = pos_dic[ele][1]
                b = pos_dic[ele][2]
                c = pos_dic[ele][3]
                with open(out, 'a') as f:
                    f.write('%d,%s,%f,%f,%f\n' % (ele, element, a, b, c))

        return pos_dic


if __name__ == '__main__':
    pass
