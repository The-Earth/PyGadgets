file = open(input('Dirty file: '), 'r')
clean_dir = input('Clean file: ')

refined_list = ''
char = '-'
line_count = 0

while char != '':
    try:
        refined_list += char
        char = file.read(1)
        if char == '\n':
            line_count += 1
            if line_count % 500 == 0:
                print(line_count)
    except UnicodeDecodeError:
        pass


file.close()
refined_list = refined_list[1:]

with open(clean_dir, 'w', encoding='utf-8') as f:
    f.write(refined_list)
