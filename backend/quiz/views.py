import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

import re

import os

from docx2python import docx2python

from .models import Subject, Test, Question, Answer, MyUser, Result


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

    phone_pattern = re.findall(r'^(\+7|)[0-9]{10,11}$',
                               data['phone'])
    if phone_pattern is not None:
        error['phone_error'] = 'Wrong phone number format'

    email_pattern = re.findall(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email'])
    if email_pattern is not None:
        error['email_error'] = 'Wrong email format'

    if phone:
        error['phone_error'] = 'Phone is existing'
    if email:
        error['email_error'] = 'Email is existing'

    if len(data['email']) == 0:
        error['email_error'] = 'Field must not be empty'
    if len(data['phone']) == 0:
        error['phone_error'] = 'Field must not be empty'

    if len(data['first_name']) == 0:
        error['first_name_error'] = 'Field must not be empty'
    if len(data['last_name']) == 0:
        error['last_name_error'] = 'Field must not be empty'

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
    subject = Subject.objects.filter(id=req["test_id"]).values()
    for s in subject:
        subject_id = s['id']
    result.user_id = req["chat_id"]
    result.subject_id = subject_id
    result.test_id = req["test_id"]
    result.result = req["result"]
    result.all_question = req['all_question']
    result.save()
    return JsonResponse({"data": "Creating"})


@csrf_exempt
def update_result(request):
    """ Update test's result """
    return JsonResponse({"data": "Updating"})


# @csrf_exempt
# def check_result(request):
#     """ /quiz/checkResult """
#     req = json.loads(request.body.decode('utf-8'))
#     data = req['data']
#     question_response = list()
#     answer_response = list()
#     for i in data:
#         answers = Answer.objects.filter(id=i['a_id']).values()
#         for a in answers:
#             print(a)
#             if not a['is_right']:
#                 que = Question.objects.filter(id=a['question_id']).values()
#                 ans = Answer.objects.filter(question_id=que[0]['id']).values()
#                 for j in ans:
#                     if j == a:
#                         j.update(is_clicked=True)
#                 question_response.append(que[0])
#                 answer_response.append(list(ans))

#     return JsonResponse({"questions": question_response, "answers": answer_response})

@csrf_exempt
def check_result(request):
    """ /quiz/checkResult """
    req = json.loads(request.body.decode('utf-8'))
    data = req['data']
    question_response = list()
    answer_response = list()
    for i in data:
        answers = Answer.objects.filter(id=i['a_id']).values()
        
        for a in answers:
            if not a['is_right']:
                que = Question.objects.filter(id=a['question_id']).values()
                ans = Answer.objects.filter(question_id=que[0]['id']).values()
                
                question_response.append(que[0])
                answer_response.append(list(ans))

    return JsonResponse({"questions": question_response, "answers": answer_response})


@csrf_exempt
def quiz_create(request):
    file_path = os.path.join(settings.BASE_DIR, 'Информатика_new_template.DOCX')
    
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
            
    
    
    # array = [['Предмет'], ['Первый тест'], ['10 вопрос', ('-', 'Первый 10 ответ'), ('+', 'Второй 10 ответ')], ['Второй 10 вопрос', ('-', 'Первый ответ на второй 10 вопрос'), ('+', 'Второй ответ на второй 10 вопрос')], ['Второй тест'], ['20 вопрос', ('-', 'Первый 20 вопрос'), ('+', 'Второй 20 вопрос')], ['Второй 20 вопрос', ('-', 'Первый ответ на второй 20 вопрос'), ('+', 'Второй ответ на второй 20 вопрос')]]
    
    # for i in range(len(array)):
    #     if i == 0:
    #         print(array[i][0])
    #         break
    #     print('qwe')
    
    Subject.objects.create(title=array[0][0])
    subject_id = Subject.objects.filter(title=array[0][0]).values()
    subject_id = subject_id[0]['id']
    array.pop(0)

    test_name = ''
    
    for j, row in enumerate(array):
        if len(row) == 1:
            for str in row:
                test_name = str
            # test_name = row
            Test.objects.create(subject_id=subject_id, title=test_name)
        else:
            test_query = list(Test.objects.filter(title=test_name).values())
            test_id = test_query[0]['id']
            question = ''
            answers = []
            for x in range(len(row)):
                if x == 0:
                    question = row[x]
                else:
                    answers.append(row[x])
                    
                        
            # print(f"Test:{test_name}\nQuestion: {question}\nAnswers: {answers}")
            Question.objects.create(text=question, test_id=test_id)
            question_query = list(Question.objects.filter(text=question).values())
            question_id = question_query[0]['id']
            answer_list = []
            for a in range(len(answers)):
                answer_text = answers[a][1]
                is_right = answers[a][0] == '+'
                answer_list.append(Answer(question_id=question_id, text=answer_text, is_right=is_right))
            Answer.objects.bulk_create(answer_list)
            # print('-------------------------------')
            
    return HttpResponse("OK")