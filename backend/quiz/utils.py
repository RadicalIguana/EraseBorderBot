import re
from docx2python import docx2python

doc = docx2python('Информатика.DOCX')

for i in doc.body:
    for j in i:
        for x in j:
            for y in x:
                if re.findall('^по теме «.$', y):
                    print(y)
