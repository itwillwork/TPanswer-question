from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import Question, Profile, Answer, Tags, LikeForAnswer, LikeForQuestion
from django import forms
from blog.forms import login_form, signup_form, settings_form, create_ask_form


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
    likes = your_likes_questions(request.user, questions)
    return render(request, 'ask/index.html', {"questions": questions, "likes_question" : likes})

def your_likes_questions(user, questions):
    likes = []
    if user.is_authenticated():
        try:
            for node in reversed(questions):
                prof = Profile.objects.filter(user = user)
                l = LikeForQuestion.objects.filter(question = node, author = prof)
                if (l):
                    likes.append(0)
                else:
                    likes.append(1)
        except:
            prof = Profile.objects.filter(user = user)
            l = LikeForQuestion.objects.filter(question = questions, author = prof)
            if (l):
                likes.append(0)
            else:
                likes.append(1)
            
    else:
        for i in questions:
            likes.append(0)
    return likes

def your_likes_answers(user, answers):
    likes = []
    if user.is_authenticated():
        try:
            for node in reversed(answers):
                prof = Profile.objects.filter(user = user)
                l = LikeForAnswer.objects.filter(answer = node, author = prof)
                if (l):
                    likes.append(0)
                else:
                    likes.append(1)
        except:
            prof = Profile.objects.filter(user = user)
            l = LikeForAnswer.objects.filter(answer = answers, author = prof)
            if (l):
                likes.append(0)
            else:
                likes.append(1)         
    else:
        for i in answers:
            likes.append(0)
    return likes

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
    likes_question = your_likes_questions(request.user, questions)
    return render(request, 'ask/hot_questions.html', {"questions": questions, "likes_question" : likes_question})

def tag(request, tag_name):
    questions = Question.objects.tag(tag_name)
    questions = paginate(questions, request, 10)
    likes_question = your_likes_questions(request.user, questions)
    return render(request, 'ask/tags.html', {
        "questions": questions,
        "likes_question" : likes_question,
        "tag_name": tag_name
        })

@login_required
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
        likes_question = your_likes_questions(request.user, question)
        it_is_author  = Question.objects.it_is_author(question, request.user)
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
        likes_answers = your_likes_answers(request.user, answers)
        return render(request,  'ask/answer.html', {
            "item": question,
            "answers": answers,
            "likes_question" : likes_question,
            "likes_answers" : likes_answers,
            "it_is_author" : it_is_author
            })
    except Question.DoesNotExist:
        raise Http404(u"Такого вопроса нет((")

def log_in(request):
    error = '' 
    if request.user.is_authenticated():
        description = u'Вы уже авторизовались на нашем сайте как, ' + request.user.username
        return render(request, 'ask/log in.html', {'description': description})
    else:
        if request.method == 'POST':
            injected_login = request.POST.get('login')
            injected_password = request.POST.get('password')
            user = authenticate(username=injected_login, password=injected_password)
            if user is not None:
                if user.is_active:
                    df = login(request, user)
                    url = request.GET.get('next')
                    if url:
                        return HttpResponseRedirect(url)
                    else:
                        return HttpResponseRedirect(reverse('index'))
                else:
                    error = u'Пароль верен, но аккаунт заблокирован'
            else:
                error = u'Неверный логин / пароль'
        form = login_form(initial={
            'login' : request.POST.get('login')
            })
        return render(request, 'ask/log in.html', {'form': form , 'error': error})

@login_required
def log_out(request):
    logout(request)
    url = request.META['HTTP_REFERER']
    return HttpResponseRedirect(url)

def signup(request):
    error = {}
    if request.method == 'POST':
        form = signup_form(request.POST)
        if form.is_valid():
            injected_login = request.POST.get('login_user')
            injected_password = request.POST.get('password')
            injected_email = request.POST.get('email')
            u = User.objects.create_user(injected_login, injected_email, injected_password)
            userdf = Profile.objects.create( user = u )
            created_user = authenticate(username=injected_login, password=injected_password)
            df = login(request, created_user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = signup_form()
    return render(request, 'ask/register.html', {'form': form , 'error': error})

@login_required
def ask(request):
    if request.method == 'POST':
        form = create_ask_form(request.POST)
        if form.is_valid():
            print(request.user.id)
            data = form.cleaned_data
            tags = data['tags'].replace(" ","").split(",")
            q = Question.objects.create( 
                title = data['title'], 
                text_qest = data['text'], 
                count_ans = 0, 
                rating = 0, 
                author_id = request.user.id
                )
            for tag in tags:
                if len(tag) > 0:
                    try:
                        currentTag = Tags.objects.get(name = tag.lower())
                    except:
                        currentTag = Tags(name = tag.lower())
                        currentTag.save()
                    q.tags.add(currentTag)
            return HttpResponseRedirect(reverse('question', kwargs={'question_id': q.id}))
    else:
        form = create_ask_form()
    return render(request, 'ask/ask.html', {'form': form})
    
@login_required
def settings(request):
    if request.method == 'POST':
        form = settings_form(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('login_user') != request.user.username:
                if User.objects.filter(username=request.POST.get('login_user')):
                    duplicate = u"Такое имя уже есть в базе!"
                    return render(request, 'ask/settings.html', {'form': form, 'duplicate': duplicate})
                else:
                    u = User.objects.get(username=request.user.username)
                    u.username = request.POST.get('login_user')
                    u.save()
            if request.POST.get('password'):
                u = User.objects.get(username=request.user.username)
                u.set_password(request.POST.get('password'))
                u.save()
                #заново логинимся
                userdf = authenticate(username= request.POST.get('login_user'), password= request.POST.get('password'))
                df = login(request, userdf)
            if form.cleaned_data['avatar']:
                m = Profile.objects.get(user = request.user)
                m.avatar = form.cleaned_data['avatar']
                m.save()
            if request.POST.get('email') != request.user.email:
                u = User.objects.get(username=request.user.username)
                u.email = request.POST.get('email')
                u.save()

            
    else:
        form = settings_form(initial = {
            'login_user': request.user.username,
            'email': request.user.email
        })
    return render(request, 'ask/settings.html', {'form': form})

#AJAX добавление ответа на вопрос
def create_answer(request):
    if request.method == 'POST':
        post_text = request.POST.get('text')
        post_id = request.POST.get('question_id')
        q = Question.objects.otvet(int(post_id))
        prof = Profile.objects.get(user = request.user)
        ans = Answer.objects.create(
                    question = q,
                    text_ans = post_text,
                    author = prof,
                    rating = 0,
                    correct = False,
                    );
        response_data = {}
        response_data['result'] = 'Create answer successful!'
        return HttpResponse(
            JsonResponse(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            JsonResponse({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

#AJAX лайк или дизлайк ответу
def change_rating_answer(request):
    if request.method == 'POST':
        inject_answer_id = request.POST.get('answer_id')
        inject_mark = request.POST.get('mark')
        inject_answer = Answer.objects.get_ans(int(inject_answer_id), int(inject_mark))
        inject_profile = Profile.objects.get(user = request.user)
        ans = LikeForAnswer.objects.create(
                    answer = inject_answer,
                    mark = inject_mark,
                    author = inject_profile,
                    );
        response_data = {}
        response_data['rating'] = inject_answer.rating
        response_data['result'] = 'Create like or dislike successful!'
        return HttpResponse(
            JsonResponse(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            JsonResponse({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

#AJAX лайк или дизлайк вопросу
def change_rating_question(request):
    if request.method == 'POST':
        inject_question_id = request.POST.get('question_id')
        inject_mark = request.POST.get('mark')
        inject_quest = Question.objects.get_quest(int(inject_question_id), int(inject_mark))
        inject_profile = Profile.objects.get(user = request.user)
        quest = LikeForQuestion.objects.create(
                    question = inject_quest,
                    mark = inject_mark,
                    author = inject_profile,
                    );
        response_data = {}
        response_data['rating'] = inject_quest.rating
        response_data['result'] = 'Create like or dislike successful!'
        return HttpResponse(
            JsonResponse(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            JsonResponse({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

#AJAX выбор правильного ответа
def check_answer(request):
    if request.method == 'POST':
        inject_answer_id = request.POST.get('answer_id')
        inject_mark = request.POST.get('mark')
        ans = Answer.objects.mark_ans(inject_answer_id, inject_mark)
        response_data = {}
        response_data['res'] = ans.correct
        response_data['result'] = 'Mark answer is successful!'
        return HttpResponse(
            JsonResponse(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            JsonResponse({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

##################################################################################
# быдло код для 1 ДЗ
##################################################################################

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


