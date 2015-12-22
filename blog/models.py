from django.db import models
from django.conf import settings
# Create your models here.
from  django.contrib.auth.models import User
from ask_nurullin.settings import MEDIA_URL

class Tags(models.Model):
    name = models.CharField(max_length=30)

class treatment_profile(models.Manager):
    def create_profile(self, login, email, password):
        u = User.objects.create_user(login, email, password)
        userdf = Profile.objects.create( user = u )
        return userdf

class Profile(models.Model):
    avatar = models.ImageField(upload_to = '', default = 'none/no-img.jpg')
    user = models.OneToOneField(User, unique=True, parent_link=True)
    objects = treatment_profile()

class treatment_questions(models.Manager):
    def last_posts(self):
    	return self.all().order_by('date').reverse()
    def post(self, id_post):
    	return self.get(id = id_post)
    def it_is_author(self, question, user):
        if question.author.user.username == user.username:
            return True
        else:
            return False
    def otvet(self, id_post):
        question = self.get(id = id_post)
        old_value = question.count_ans
        question.count_ans = old_value + 1
        question.save()
        return question
    def best_post(self):
    	return self.all().order_by('rating').reverse()
    def tag(self, tag_name):
    	return self.filter(tags__name = tag_name).order_by('date').order_by('rating')
    def get_quest(self, id_question, difference):
        quest = self.get(id = id_question)
        old_value = quest.rating
        quest.rating = old_value + difference
        quest.save()
        return quest

class Question(models.Model):
    title = models.CharField(max_length=120)
    text_qest = models.TextField()
    count_ans = models.PositiveIntegerField()
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags)
    author = models.ForeignKey(Profile)
    objects = treatment_questions()

class treatment_answers(models.Manager):
    def get_answer(self, question_id):
        answers = self.filter(question__id = question_id).order_by('-date').order_by('-rating')

        return answers
    def get_ans(self, id_answer, difference):
        ans = self.get(id = id_answer)
        old_value = ans.rating
        ans.rating = old_value + difference
        ans.save()
        return ans
    def create_rating(self, id_answer, difference):
        answer = self.get(id = id_answer)
        old_value = answer.rating
        answer = answer.update(rating = old_value + 1)
        return answer.rating
    def mark_ans(self, id_answer, mark):
        answer = self.get(id = id_answer)
        print mark
        if mark == "true":
            answer.correct = True
        else: 
            answer.correct = False
        answer.save()
        return answer
            

class Answer(models.Model):
	question = models.ForeignKey(Question)
	text_ans = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Profile)
	rating = models.IntegerField()
	correct = models.BooleanField()
	objects = treatment_answers()

class LikeForAnswer(models.Model):
    mark = models.IntegerField()
    answer = models.ForeignKey(Answer, null=True)
    author = models.ForeignKey(Profile)

class LikeForQuestion(models.Model):
    mark = models.IntegerField()
    question = models.ForeignKey(Question, null=True)
    author = models.ForeignKey(Profile)

