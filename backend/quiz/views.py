import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from itertools import groupby
import re
import os

from docx2python import docx2python

from .models import Feedback, Subject, Test, Question, Answer, MyUser, Result, Quiz


def index(request):
    return HttpResponse('Some text')


@csrf_exempt
def get_user(request):
    """ Get user's data by chat_id """
    id = json.loads(request.body.decode('utf-8'))
    user_data = MyUser.objects.filter(chat_id=id['chat_id']).values()
    data = list(user_data)
    return JsonResponse({'data': data})


@csrf_exempt
def get_user_id(request):
    """ Check existing user """
    user_id = json.loads(request.body.decode('utf-8'))
    existing = MyUser.objects.filter(chat_id=user_id['data']).exists()
    return HttpResponse(existing)


@csrf_exempt
def create_user(request):
    user = MyUser()
    data = json.loads(request.body.decode('utf-8'))

    error = check_error(data)
    if len(error) != 0:
        return JsonResponse(error)

    user.chat_id = data["chat_id"]
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.phone = data["phone"]
    user.email = data["email"]
    user.save()
    return HttpResponse('OK')


def check_error(data):
    error = {}
    phone = MyUser.objects.filter(phone=data['phone']).exists()
    email = MyUser.objects.filter(email=data['email']).exists()


    phone_pattern = re.findall('(^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$)|(^\s*$)', data['phone'])
    if not bool(phone_pattern):
        error['phone_error'] = 'Неправильный формат номера'

    email_pattern = re.findall(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)|(^\s*$)', data['email'])
    if not bool(email_pattern):
        error['email_error'] = 'Неправильный формат почты'


    if data['phone']!='' and phone==True:
        error['phone_error'] = 'Номер уже зарегистрирован'
    if data['email']!='' and email==True:
        error['email_error'] = 'Email уже зарегистрирован'

    # if len(data['email']) == 0:
    #     error['email_error'] = 'Поле должно быть заполненным'
    # if len(data['phone']) == 0:
    #     error['phone_error'] = 'Поле должно быть заполненным'

    if len(data['first_name']) == 0:
        error['first_name_error'] = 'Поле должно быть заполненным'
    if len(data['last_name']) == 0:
        error['last_name_error'] = 'Поле должно быть заполненным'

    return error


@csrf_exempt
def get_all_subjects(request):
    """ /quiz/getAllSubjects """
    subjects = Subject.objects.all().values()
    data = list(subjects)
    return JsonResponse({'data': data})


@csrf_exempt
def get_subjects_tests(request):
    subjects = Subject.objects.all().values()
    tests = Test.objects.all().values()
    sub_data = list(subjects)
    test_data = list(tests)
    return JsonResponse({'subjects': sub_data, 'tests': test_data})


@csrf_exempt
def get_subject(request):
    """ Get subject by id 
        /quiz/subject/
        {
            "id": <int>
        }
    """
    req = json.loads(request.body.decode('utf-8'))
    subject = Subject.objects.filter(id=req['id']).values()
    data = list(subject)
    return JsonResponse({'data': data})


@csrf_exempt
def get_test(request):
    """ Get all tests of subject by subject_id
        /quiz/test/ 
        {
            "subject_id": <int>
        }
    """
    req = json.loads(request.body.decode('utf-8'))
    subject = Test.objects.filter(subject=req['subject_id']).values()
    data = list(subject)
    return JsonResponse({'data': data})


@csrf_exempt
def get_question(request):
    """ Get all questions of test by test_id 
        /quiz/question/
        {
            "test_id": <int>
        }
    """
    req = json.loads(request.body.decode('utf-8'))
    questions = Question.objects.filter(test=req['test_id']).values()
    data = list(questions)
    return JsonResponse({'data': data})


@csrf_exempt
def get_answer(request):
    """ Get alls answer of question by question_id 
        /quiz/answer/
        {
            "question_id": <int>
        }
    """
    req = json.loads(request.body.decode('utf-8'))
    answer = Answer.objects.filter(question=req['question_id']).values()
    data = list(answer)
    return JsonResponse({'data': data})


@csrf_exempt
def get_question_answer(request):
    """ /quiz/getSubTest """
    req = json.loads(request.body.decode('utf-8'))
    test_id = req['test_id']
    question = Question.objects.filter(test=test_id).values()
    answer = Answer.objects.filter().values()
    answer_data = list()

    for q in question:
        for a in answer:
            if a['question_id'] == q['id']:
                answer_data.append(a)

    question_data = list(question)
    return JsonResponse({'questions': question_data, 'answers': answer_data})


@csrf_exempt
def create_result(request):
    """ Store test's result """
    """ /quiz/createResult """
    result = Result()
    req = json.loads(request.body.decode('utf-8'))
    test = Test.objects.filter(id=req['test_id']).values()
    subject = Subject.objects.filter(id=test[0]['subject_id']).values()
    subject_id = subject[0]['id']

    updated_result = {
        "result": req["result"],
    }
    created = Result.objects.update_or_create(
        user_id=req["chat_id"],
        subject_id=subject_id,
        test_id=req["test_id"],
        all_question=req["all_question"],
        defaults=updated_result
    )    
    
    return HttpResponse('OK')


@csrf_exempt
def get_result(request):
    req = json.loads(request.body.decode('utf-8'))
    id = int(req['chat_id'])
    result_obj = Result.objects.filter(user_id=id).values()
    response = []
    
    for i in result_obj:
        subject_id = i['subject_id']
        test_id = i['test_id']
        result = i['result']
        all_question = i['all_question']
        
        subject_title = Subject.objects.get(id=subject_id)
        subject_title = subject_title.title
        
        test_title = Test.objects.get(id=test_id)
        test_title = test_title.title
        response.append({
            "subject": subject_title,
            "test": test_title,
            "result": result,
            "all_question": all_question
        })
        
    return JsonResponse({
        "data": response
    })

@csrf_exempt
def check_test(request):
    """ Update test's result """
    req = json.loads(request.body.decode('utf-8'))
    tests = []
    results = Result.objects.filter(user_id=req['chat_id']).values()
    for test_id in results:
        tests.append(test_id['test_id'])
    return JsonResponse({"data": tests})

@csrf_exempt
def check_result(request):
    """ /quiz/checkResult """
    req = json.loads(request.body.decode('utf-8'))
    data = req['data']
    question_response = list()
    answer_response = list()
    for i in data:
        
        if type(i) == dict and i['q_type'] == "text": 
            correct_question = Question.objects.filter(id=i['q_id']).values()
            correct_answer = Answer.objects.filter(question_id=i['q_id']).values()
            if i['answer'] == None:
                question_response.append(correct_question[0])
                answer_response.append(correct_answer[0])
            else:
                # Changed this for test
                user_answer = i['answer']
                correct_text_answer = correct_answer[0]['text']
                if user_answer.lower() != correct_text_answer.lower():
                    question_response.append(correct_question[0])
                    answer_response.append(correct_answer[0])
            
        elif type(i) == dict and i['q_type'] == "radio":
            if i['answer'] == None:
                correct_question = Question.objects.filter(id=i['q_id']).values()
                correct_answer = Answer.objects.filter(question_id=i['q_id']).values()
                question_response.append(correct_question[0])
                for x in correct_answer:
                    answer_response.append(x)
            else:
                user_answer = i['answer']
                if not user_answer['is_right']:
                    correct_question = Question.objects.filter(id=i['q_id']).values()
                    correct_answer = Answer.objects.filter(question_id=i['q_id']).values()
                    question_response.append(correct_question[0])
                    for x in correct_answer:
                        # Checking
                        if x['id'] == i['answer']['id'] and i['answer']['is_right'] == False: 
                            x['checked'] = True
                        elif  x['id'] == i['answer']['id'] and x['is_right'] == True:
                            x['checked'] = False
                        else:
                            x['checked'] = False                      
                        answer_response.append(x)
        
        elif type(i) == dict and i['q_type'] == 'checkbox' and i['answer'] == None:
            correct_question = Question.objects.filter(id=i['q_id']).values()
            correct_answer = Answer.objects.filter(question_id=i['q_id']).values()
            question_response.append(correct_question[0])
            for x in correct_answer:
                answer_response.append(x)
        
        
        elif type(i) == list:
            answer_array = transform_array_by_id(i)
            for elem in answer_array:
                correct_question = Question.objects.filter(id=elem[0]['question_id']).values()
                question_response.append(correct_question[0])
                correct_answer = list(Answer.objects.filter(question_id = elem[0]['question_id']).values())
                for i in elem:
                    for ca in correct_answer:
                        if i['id'] == ca['id'] and ca['is_right'] == False:
                            ca['checked'] = True
            for i in correct_answer:
                answer_response.append(i)

    return JsonResponse({"questions": question_response, "answers": answer_response})

def transform_array_by_id(arr):
    sorted_array = sorted(arr, key=lambda x: x['question_id'])
    grouped_array = [list(group) for key, group in groupby(sorted_array, key=lambda x: x['question_id'])]
    return grouped_array


@csrf_exempt
def quiz_create(request):
    
    docs_array = ['Информатика.DOCX', 'Дизайн.DOCX', 'Программирование.DOCX', 'Разработка сайтов.DOCX']
    for i in docs_array:
        print(i)
        file_path = os.path.join(settings.BASE_DIR, i)
        
        doc = docx2python(file_path)
        doc_text = doc.text
        
        subject = re.compile(r'(?<=^“)[^+]+(?=”)')
        test = re.compile(r'(?<=«)[^+]+(?=»)')
        question = re.compile(r'^\d+\.\s(.+)')
        answer = re.compile(r'(^[а-я]\)|^[a-b]\.|^\(\d+\)|^\d+\)|^\d+\.|^Ответ:|^[+-])\s(.*)')

        array = []
        for line in doc_text.splitlines():
            if line.startswith('“'):
                array.append(subject.findall(line))
            if line.startswith('Тест'):
                array.append(test.findall(line))
            if question.match(line):
                array.append(question.findall(line))
            elif answer.match(line):
                array[-1].append(answer.findall(line)[0])
                
        # array = [['Предмет'], ['Тест'], ['Радио', ('+', 'Answer 1'), ('-', 'Answer 2')], ['Checkbox', ('+', 'Answer 1'), ('+', 'Answer 2'), ('-', 'Answer 3')], ['Text', ('Test answer')]]
        
        Subject.objects.create(title=array[0][0])
        subject_id = Subject.objects.filter(title=array[0][0]).values()
        subject_id = subject_id[0]['id']
        array.pop(0)

        test_name = ''
        
        for j, row in enumerate(array):
            if len(row) == 1:
                for str in row:
                    test_name = str
                Test.objects.create(subject_id=subject_id, title=test_name)
            else:
                test_query = list(Test.objects.filter(title=test_name).values())
                test_id = test_query[0]['id']
                question = ''
                question_type = ''
                answers = []
                for x in range(len(row)):
                    if x == 0:
                        question = row[x]
                    else:
                        answers.append(row[x])
                        
                
                count = 0
                for i in range(len(answers)):
                    for j in answers[i]:
                        if j == '+':
                            count += 1

                if count == 0:
                    question_type = 'text'
                elif count == 1:
                    question_type = 'radio'
                else:
                    question_type = 'checkbox'
                    
                count = 0   
                Question.objects.create(text=question, test_id=test_id, type=question_type)
                question_query = list(Question.objects.filter(text=question).values())
                question_id = question_query[0]['id']
                answer_list = []
                for a in range(len(answers)):
                    answer_text = answers[a][1]
                    is_right = answers[a][0] == '+'
                    answer_list.append(Answer(question_id=question_id, text=answer_text, is_right=is_right))
                Answer.objects.bulk_create(answer_list)
                
    return HttpResponse("OK")


@csrf_exempt
def send_feedback(request):
    req = json.loads(request.body.decode('utf-8'))
    data = req["data"]
    feedback = Feedback()
    feedback.text = data['text']
    feedback.save()    
    return JsonResponse({"data": "OK"})
    
    