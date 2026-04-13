from django.shortcuts import render, redirect
from .models import Question
import random
import time 

def quiz_page(request, category):
    if 'quiz_started' not in request.session:
        request.session['start_time'] = time.time() 

        questions = list(Question.objects.filter(category=category))
        random.shuffle(questions)
        request.session['questions'] = [q.id for q in questions[:10]]  
        request.session['current_question'] = 0
        request.session['quiz_started'] = True
        request.session['last_answer_feedback'] = '' 
        request.session['correct_answers'] = 0 
        
    start_time = request.session.get('start_time')
    elapsed_time = time.time() - start_time  
    remaining_time = max(0, 60 - elapsed_time)  #value ng timer

    if remaining_time == 0:
        return redirect('quiz_complete?timeout=true') 

    current_question_index = request.session.get('current_question', 0)
    questions = request.session.get('questions', [])

    if current_question_index >= len(questions):
        return redirect('quiz_complete')

    question_id = questions[current_question_index]
    question = Question.objects.get(id=question_id)

    if request.method == 'POST' and 'answer' in request.POST:
        user_answer = request.POST.get('answer')
        correct_answer = question.correct_answer

        if user_answer == correct_answer:
            request.session['last_answer_feedback'] = 'Correct'
            request.session['correct_answers'] += 1
        else:
            request.session['last_answer_feedback'] = 'Incorrect'

        if current_question_index < len(questions) - 1:
            request.session['current_question'] += 1
        else:
            request.session['quiz_started'] = False 
            return redirect('quiz_complete')

    if request.method == 'POST' and 'next_question' in request.POST:
        request.session['last_answer_feedback'] = ''

    question_number = current_question_index + 1

    return render(request, 'questions/quiz.html', {
        'category': category,
        'question': question,
        'last_answer_feedback': request.session.get('last_answer_feedback', ''),
        'question_number': question_number,
        'total_questions': len(questions),
        'remaining_time': int(remaining_time), 
    })


def home(request):
    return render(request, 'questions/home.html')  


def quiz_complete(request):
    correct_answers = request.session.get('correct_answers', 0)
    total_questions = 10  
    score = (correct_answers / total_questions) * 100 # temporary computation ng score. dapat score = min(100, (correct_answers * 10) + (20 / 60 * time_remaining))

    timeout = request.GET.get('timeout', False)  
    if 'ran_out_of_time' in request.session:
        del request.session['ran_out_of_time']

    request.session.flush()

    return render(request, 'questions/quiz_complete.html', {
        'score': score,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'timeout': timeout,  
    })
