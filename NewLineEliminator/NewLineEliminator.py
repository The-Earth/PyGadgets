import os

def eliminator(file):
    print(file.read().replace('\n',' '))

if __name__ == '__main__':
    while 1:
        with open('1.txt','r',encoding='utf-8') as f:
            eliminator(f)
        os.system('pause')
