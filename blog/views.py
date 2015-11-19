from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Question, Profile, Answer
from django.http import Http404

def index(request):
    questions = Question.objects.last_posts()
    # TEST DATA
    #questions = []
    #title1 = "Lorem ipsum dolor sit amet, consectetur adipiscing .. ?"
    #text1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque efficitur sem quis rutrum gravida. Pellentesque vel mi aliquet diam sodales gravida a quis massa. Duis bibendum magna ac sollicitudin condimentum. Nam nibh orci, cursus ut tortor ac, tincidunt feugiat odio. Phasellus suscipit accumsan mauris sed elementum. Nullam id arcu quis tellus bibendum blandit pretium id leo. Cras eu cursus urna."
    #for i in xrange(1,28):
    #    questions.append({
    #    'title': str(i) + ' ' + title1,
    #    'id': i,
    #    'text': str(i) + ' ' + text1,
    #    })
    questions = paginate(questions, request, 10)
    return render(request, 'ask/index.html', {"questions": questions})

def paginate(objects_list, request, quantity_per_page):
    paginator = Paginator(objects_list, quantity_per_page) # Show 10 objects per page
    page = request.GET.get('page')
    try:
        objects_list = paginator.page(page)
    except PageNotAnInteger:
        objects_list = paginator.page(1)
    except EmptyPage:
        objects_list = paginator.page(paginator.num_pages)
    return objects_list


def hot_questions(request):
    #questions = []
    #title1 = "HOTTTT!!!! Lorem ipsum dolorng .. ?"
    #text1 = "sdLorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque efficitur sem quis rutrum gravida. Pellentesque vel mi aliquet diam sodales gravida a quis massa. Duis bibendum magna ac sollicitudin condimentum. Nam nibh orci, cursus ut tortor ac, tincidunt feugiat odio. Phasellus suscipit accumsan mauris sed elementum. Nullam id arcu quis tellus bibendum blandit pretium id leo. Cras eu cursus urna."
    #for i in xrange(1,28):
    #    questions.append({
    #    'title': str(i) + ' ' + title1,
    #    'id': i,
    #    'text': str(i) + ' ' + text1,
    #    })
    questions = Question.objects.best_post()
    questions = paginate(questions, request, 10)
    return render(request, 'ask/hot_questions.html', {"questions": questions})

def tag(request, tag_name):
    questions = Question.objects.tag(tag_name)
    questions = paginate(questions, request, 10)
    return render(request, 'ask/tags.html', {
        "questions": questions,
        "tag_name": tag_name
        })

def question(request, question_id):
    try:
        #вопрос
        #TEST DATA
        #title1 = "i am hungry!!! Lorem ipsum dolorng .. ?"
        #text1 = "sdLorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque efficitur sem quis rutrum gravida. Pellentesque vel mi aliquet diam sodales gravida a quis massa. Duis bibendum magna ac sollicitudin condimentum. Nam nibh orci, cursus ut tortor ac, tincidunt feugiat odio. Phasellus suscipit accumsan mauris sed elementum. Nullam id arcu quis tellus bibendum blandit pretium id leo. Cras eu cursus urna."
        #question = {
        #'title': str(question_id) + ' ' + title1,
        #'id': question_id,
        #'text': str(question_id) + ' ' + text1,
        #}
        question = Question.objects.post(int(question_id))
        #ответы
        #TEST DATA
        #answers = []
        #text1 = "sdLorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque efficitur sem quis rutrum gravida. Pellentesque vel mi aliquet diam sodales gravida a quis massa. Duis bibendum magna ac sollicitudin condimentum. Nam nibh orci, cursus ut tortor ac, tincidunt feugiat odio. Phasellus suscipit accumsan mauris sed elementum. Nullam id arcu quis tellus bibendum blandit pretium id leo. Cras eu cursus urna."
        #for i in xrange(1,10):
        #    answers.append({
        #    'id': i,
        #    'text': str(i) + ' ' + text1,
        #    })
        answers = Answer.objects.get_answer(int(question_id))
        return render(request,  'ask/answer.html', {
            "item": question,
            "answers": answers
            })
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

def login(request):
    return render(request, 'ask/log in.html')

def signup(request):
    return render(request, 'ask/register.html')

def ask(request):
    return render(request, 'ask/ask.html')

def settings(request):
    return render(request, 'ask/settings.html')
# быдло код для 1 ДЗ

html = """
<html>
<body>
    <form href='/a/' method = 'get'>
        <input name='a' type = 'text'>
        <input name='b' type = 'text'>
        <input type = 'submit' value = 'submit'>
    </form>
    <p> %s </p>
</body>
</html>
"""

@csrf_exempt
def simple(request):
    if request.method == 'POST':
        dataq = 'a = ' + request.POST.get('a') + ' b = ' + request.POST.get('b')
    else:
        dataq = 'empty post'

    if 'a' in request.GET:
        dataq = 'a = ' + request.GET.get('a') + ' b = ' + request.GET.get('b')
    else:
        dataq = 'empty post'

    response = html % (dataq)

    return HttpResponse(response)


