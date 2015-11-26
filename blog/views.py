from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import Question, Profile, Answer, Tags
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
            userdf = Profile.objects.create( user = u , avatar = "http://placekitten.com/g/90/90/")
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
            if request.POST.get('avatar'):
                print('izm avatar')
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


