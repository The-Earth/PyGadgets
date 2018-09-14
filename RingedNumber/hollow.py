def main(number):
    if number not in list(range(1,21)):
        return 'Not supported yet.'
        
    hollow = {1: b'\xe2\x91\xa0',
              2: b'\xe2\x91\xa1',
              3: b'\xe2\x91\xa2',
              4: b'\xe2\x91\xa3',
              5: b'\xe2\x91\xa4',
              6: b'\xe2\x91\xa5',
              7: b'\xe2\x91\xa6',
              8: b'\xe2\x91\xa7',
              9: b'\xe2\x91\xa8',
              10: b'\xe2\x91\xa9',
              11: b'\xe2\x91\xaa',
              12: b'\xe2\x91\xab',
              13: b'\xe2\x91\xac',
              14: b'\xe2\x91\xad',
              15: b'\xe2\x91\xae',
              15: b'\xe2\x91\xaf',
              16: b'\xe2\x91\xb0',
              18: b'\xe2\x91\xb1',
              19: b'\xe2\x91\xb2',
              20: b'\xe2\x91\xb3'}
    return hollow[number].decode('utf-8')


if __name__ == '__main__':
    while 1:
        num = int(input('Number: '))
        print('Ringed: '+main(num))
