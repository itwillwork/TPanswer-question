from django.db import models

# Create your models here.
from  django.contrib.auth.models import User

class Tags(models.Model):
    name = models.CharField(max_length=30)

class Profile(models.Model):
	avatar = models.ImageField(max_length=200)
	user = models.OneToOneField(User)

class treatment_questions(models.Manager):
    def last_posts(self):
    	return self.all().order_by('date').reverse()
    def post(self, id_post):
    	return self.get(id = id_post)
    def best_post(self):
    	return self.all().order_by('rating').reverse()
    def tag(self, tag_name):
    	return self.filter(tags__name = tag_name).order_by('date').order_by('rating')

class Question(models.Model):
    title = models.CharField(max_length=120)
    text_qest = models.TextField()
    count_ans = models.PositiveIntegerField()
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags)
    author = models.ForeignKey(Profile)
    objects = treatment_questions()

class Answer(models.Model):
	question = models.ForeignKey(Question)
	text_ans = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Profile)
	rating = models.IntegerField()
	correct = models.BooleanField()
	def get_answer(question_id):
		return self.filter(question__id= question_id).order_by('-date').order_by('-rating')

class Like(models.Model):
	entity = models.BooleanField()
	numer = models.ForeignKey(Profile)
	mark = models.BooleanField()
	author = models.PositiveIntegerField()

