import re
import docx2txt

# Открываем документ и извлекаем текст
text = docx2txt.process('Информатика.DOCX')

for line in text.split('\n'):
    for i in range(len(line)):
        if line[0].isdigit() and line[1] == '.':
            print(line)
            break
    

