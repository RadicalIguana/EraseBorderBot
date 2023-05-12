import re
from docx2python import docx2python

# from .models import Subject, Test, Question, Answer, MyUser, Result

doc = docx2python('Информатика_new_template.DOCX')
doc_text = doc.text

text = '''
"Subject name"
Тест 1 по теме «Общее» (правильные ответы отмечены «+») 

1. Как называется группа файлов, которая хранится отдельной группой и имеет собственное имя? 
- Байт 
+ Каталог 

2. Как называются данные или программа на магнитном диске? 
- Папка 
+ Файл 

Тест 4 по теме «Основы алгоритмики. Языки высокого уровня программирования» (правильные ответы отмечены «+») 

1. Распространенные формы представления алгоритмов 
- образная 
+ словесная 


2. Операторы … являются простой конструкцией условия 
+ If-Then 
- Select Case 
'''

subject = re.compile(r'(?<=^“)[^+]+(?=”)')
test = re.compile(r'(?<=«)[^+]+(?=»)')
question = re.compile(r'^\d+\.\s(.+)')
answer = re.compile(r'(^[а-я]\)|^[a-b]\.|^\(\d+\)|^\d+\)|^\d+\.|^Ответ:|^[+-])\s(.*)')

output = []
for line in doc_text.splitlines():
    if line.startswith('“'):
        output.append(subject.findall(line))
    if line.startswith('Тест'):
        output.append(test.findall(line))
    if question.match(line):
        output.append(question.findall(line))
    elif answer.match(line):
        output[-1].append(answer.findall(line)[0])
        
for test in output:
    print(test)
    
test_name = ''

# for i in range(len(output)):
#     for j in range(len(output[i])):
        
        
# test_array = ['Question', ('+', 'Answer 1'), ('-', 'Answer 2')]
# question = ''
# answers = []print(f"Question: {question}\nAnswers: {answers}")

# for i, row in enumerate(test_array):
#     if i == 0:
#         question = row
#     else:
#         answers.append(row)
        

        

        
    
    
    