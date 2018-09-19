import os


def main(inp, out, centerElement):
    while 1:
        for string in list(open(inp, 'r', encoding='utf-8')):  # Read orca executable path
            if string.startswith('# orca'):
                orcapath = string.split()[2]

            if string.startswith('Q '):  # Read old point charge value
                OldSurrCharge = string.split()[1]
                print(OldSurrCharge)
                break

        os.system(orcapath + ' ' + inp + ' > ' + out)
        outlist = list(open(out, 'r', encoding='utf-8'))

        for i in range(len(outlist)):   # Find MULLIKEN analysis
            if outlist[i] == 'MULLIKEN ATOMIC CHARGES\n':
                chargeStart = i
            if 'Sum of atomic charges' in outlist[i]:
                chargeEnd = i

        for i in range(chargeStart, chargeEnd): # Read new point charge value
            if centerElement in outlist[i]:
                NewSurrCharge = outlist[i].split()[2]

        with open(inp+'.log', 'a', encoding='utf-8') as log:    # Write log
            log.write('--------\nSurrounding charge set as '+OldSurrCharge+'\nCore '+centerElement\
                      +' charge '+NewSurrCharge+'\n--------\n')

        if abs(NewSurrCharge - OldSurrCharge) < 0.1:
            break

        with open(inp, 'r', encoding='utf-8') as fin:   # Edit input file
            inputText = fin.read().replace('Q '+OldSurrCharge, 'Q '+NewSurrCharge)

        with open(inp, 'w', encoding='utf-8') as fin:
            fin.write(inputText)


if __name__ == '__main__':
    main('TMS.inp', 'TMS.out', 'Si')
