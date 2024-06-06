file_name = 'text.txt'

with open(file_name, 'r', encoding='utf-8') as file:
    text = file.read()
    file.close()
text = text.split('\n')

with open('output.txt', 'w', encoding='utf-8') as file:

    for line in text:
        letter = 'о'
        cht = 0.11
        cht_res = line.lower().count(letter) / len(line)

        if cht_res > cht:
            print(line + ' - ДА')
            print(f'Буква {letter}: {line.lower().count(letter)} / {len(line)} = {cht_res}\n')
            file.write(line + ' - ДА\n')

        else:
            print(line + ' - НЕТ')
            print(f'Буква {letter}: {line.lower().count(letter)} / {len(line)} = {cht_res}\n')
            file.write(line + ' - НЕТ\n')
