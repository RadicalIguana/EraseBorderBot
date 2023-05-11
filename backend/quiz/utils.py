import re

text = '''
category 1
1. Действия, выполняемые с информацией, называются…  
а) организационными процессами 
б) структурными процессами 
в) физическими процессами 

2. 1 бит — это… 
а) 1 или 0 
б) 11 
в) 10 
г) 01 


3. Вопрос 3
1) Ответ 1
2) Ответа 2
3) Ответ 3
'''

qa = []
block = []

for chunk in re.split(r"\n(?=[а-я\d][).] )", text):
    if m := re.match(r"\d+\. (.+)", chunk, re.S):
        qa.append(tuple(block))
        block = [m.group(1)]
    elif m := re.match(r"[а-я]+\) (.+?)(?=\n\n|$|[a-z]+\) )", chunk, re.S):
        block.append(m.group(1))

qa = qa[1:] + [tuple(block)]

for line in qa:
    print(line)
