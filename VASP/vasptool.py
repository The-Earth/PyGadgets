from collections import OrderedDict


class OUTCAR:

    def __init__(self, filename='OUTCAR'):
        self.filename = filename
        # get text
        self.__text_list = list(open(filename, 'r'))
        self.len = len(self.__text_list)
        # find poscar
        self.poscar = []  # TODO use POSCAR class
        '''
        poscar is inform:
        [['li','4'],['o','2']]
        which represent sequence of elements and their amount
        '''
        for line in self.__text_list:
            if 'POSCAR' in line:
                for comp in line.split():
                    if 'POSCAR' in comp or '=' in comp:
                        continue
                    for i in range(len(comp)):
                        try:
                            self.poscar.append([comp[:i], comp[i:]])
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
        for i in range(self.len):
            if '  UNSYMMETRIZED TENSORS \n' == self.__text_list[i]:
                csStart = i
            if '  SYMMETRIZED TENSORS \n' == self.__text_list[i]:
                csEnd = i
                break

        i, tensordia = csStart + 1, 0
        while i < csEnd:
            # get atom id (start from 1)
            atomid = self.__text_list[i].split()[1]
            # add diagonal element of cs tensor
            i += 1
            tensordia += float(self.__text_list[i].split()[0])
            i += 1
            tensordia += float(self.__text_list[i].split()[1])
            i += 1
            tensordia += float(self.__text_list[i].split()[2])
            # log data
            cs.setdefault(int(atomid), str(tensordia / 3))
            # move and init
            i += 1
            tensordia = 0

        # merge elements, atomid & cs
        preatom = 0
        for i in range(len(self.poscar)):
            num = int(self.poscar[i][1])
            for j in range(1, num + 1):
                cs[preatom + j] = self.poscar[i][0] + ',' + cs[preatom + j]
            preatom += num

        # write to file
        if out:
            for i in range(len(cs)):
                t = str(i) + ',' + cs[i + 1] + '\n'
                with open(out, 'a') as f:
                    f.write(t)

        return cs

    def get_Afc(self):
        """
        :return: An ordered dict with atom index as keys and Afc as values
                {1: 2.33, 2:3.44 ...}
        """
        start, A_tot_dict = -1, OrderedDict()
        for i in range(self.len):
            if 'Fermi contact (isotropic) hyperfine coupling parameter (MHz)' in self.__text_list[i]:
                start = i + 4
                break

        if start == -1:
            raise Exception('Fermi contact A not found in OUTCAR')
        i = start
        while '--' not in self.__text_list[i].split()[0]:
            ind = int(self.__text_list[i].split()[0])
            Afc = float(self.__text_list[i].split()[5])
            A_tot_dict[ind] = Afc
            i += 1

        return A_tot_dict

    def get_Adp(self):
        import numpy
        start, A_tensor_dict = -1, OrderedDict()
        for i in range(self.len):
            if 'Dipolar hyperfine coupling parameters (MHz)' in self.__text_list[i]:
                start = i + 4
                break

        if start == -1:
            raise Exception('Dipolar A not found in OUTCAR')
        i = start
        while '--' not in self.__text_list[i].split()[0]:
            lt = self.__text_list[i].split()
            ind = int(lt[0])
            Ad = numpy.mat(((lt[1], lt[4], lt[5]),
                            (lt[4], lt[2], lt[6]),
                            (lt[5], lt[6], lt[3])), dtype='float64')
            A_tensor_dict[ind] = Ad
            i += 1

        return A_tensor_dict

    def get_CSA_valence(self):  # Excluding G=0
        start, csa_dict = -1, OrderedDict()
        for i in range(self.len):
            if '(absolute, valence only)' in self.__text_list[i]:
                start = i + 1
                break

        if start == -1:
            raise Exception('CSA tensor valence only not found in OUTCAR.')
        i = start
        while '--' not in self.__text_list[i]:
            ind = int(self.__text_list[i].split()[0])
            shift = float(self.__text_list[i].split()[1])
            csa_dict[ind] = shift
            i += 1

        return csa_dict

    def get_magnetization(self):
        start, mag_dict = -1, OrderedDict()
        for i in range(self.len):
            if 'magnetization (x)' in self.__text_list[i]:
                start = i + 4
                break

        if start == -1:
            raise Exception('magnetization (x) not found in OUTCAR.')
        i = start
        while '--' not in self.__text_list[i]:
            ind = int(self.__text_list[i].split()[0])
            shift = float(self.__text_list[i].split()[4])
            mag_dict[ind] = shift
            i += 1

        return mag_dict

    def get_A1c(self):
        """
        :return: An ordered dict with atom index as keys and A1c as values
                {1: 2.33, 2:3.44 ...}
        """
        start, A_1c_dict = -1, OrderedDict()
        for i in range(self.len):
            if 'Fermi contact (isotropic) hyperfine coupling parameter (MHz)' in self.__text_list[i]:
                start = i + 4
                break

        if start == -1:
            raise Exception('Fermi contact A not found in OUTCAR')
        i = start
        while '--' not in self.__text_list[i].split()[0]:
            ind = int(self.__text_list[i].split()[0])
            A1c = float(self.__text_list[i].split()[4])
            A_1c_dict[ind] = A1c
            i += 1

        return A_1c_dict


class INCAR:

    def __init__(self, filename='INCAR'):
        self.filename = filename
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
        self.elements = self.text_list[5].split()
        self.ele_num = self.text_list[6].split()
        self.cord_type = self.text_list[7].strip()[0]
        # Verify POSCAR
        if len(self.elements) != len(self.ele_num):
            raise IndexError("POSCAR: Line 7 doesn't match line 6.")
        for i in range(len(self.ele_num)):
            self.ele_num[i] = int(self.ele_num[i])

        # Detect end of positions
        ifbreak = 0
        for i in range(self.len):
            if len(self.text_list[i].split()) == 0:
                self.pos_end = i
                ifbreak = 1
                break
        if ifbreak:
            self.pos_len = self.pos_end - 8
        else:
            self.pos_len = self.len - 8
        # Verify positions and numbers in line 7
        if sum(self.ele_num) != self.pos_len:
            raise IndexError("POSCAR: Positions doesn't match numbers defined in line 7.")

    def get_num_dict(self):
        """
        :return: A dict with elements as key and numbers of them as value. {'Li'":2, 'O':4}
        """
        num_dict = dict()
        for i in range(len(self.elements)):
            num_dict[self.elements[i]] = self.ele_num[i]
        return num_dict

    def get_full_pos(self, out=None):
        """
        :return: A dict containing all atoms and their position.
        Positions are in tuple and in form of coordinate type defined in POSCAR
        """
        line_id = 8
        pos_dic = OrderedDict()
        for i in range(len(self.elements)):
            for j in range(self.ele_num[i]):
                a = float(self.text_list[line_id].split()[0])
                b = float(self.text_list[line_id].split()[1])
                c = float(self.text_list[line_id].split()[2])
                pos_dic[line_id - 7] = (self.elements[i], a, b, c)
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

    def get_pos(self, ind):
        li = []
        for i in range(3):
            li.append(float(self.text_list[ind + 7].split()[i]))
        return tuple(li)

    def get_element(self, ind=None, pos=None) -> str:
        if not (ind or pos):
            raise TypeError('get_element takes atom id or position but none was given.')
        if ind and pos:
            raise TypeError('get_element takes one of atom id or position but 2 were given')
        if ind > sum(self.ele_num):
            raise IndexError('Atom id is too large')
        if ind:
            for i in range(len(self.elements)):
                if ind <= self.ele_num[i]:
                    return self.elements[i]
                else:
                    ind -= self.ele_num[i]
        if pos:
            pass

    def get_id(self, pos):
        pass


class CONTCAR(POSCAR):

    def __init__(self, filename='CONTCAR'):
        POSCAR.__init__(self, filename=filename)

    def save_as(self, out='POSCAR'):
        with open(out, 'w') as f:
            f.write(''.join(self.text_list))


if __name__ == '__main__':
    pass
