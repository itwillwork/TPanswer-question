from django.conf.urls import url
from views import simple
from views import index
from views import hot_questions
from views import tag
from views import question
from views import login
from views import signup
from views import ask
from views import settings

urlpatterns = [
	url(r'^a/$', simple, name = 'simple'),
	url(r'^$', index, name = 'index'),
	url(r'^hot/$', hot_questions, name = 'hot_questions'),
	url(r'^tag/$', tag, name = 'tag'),
	url(r'^question/(?P<question_id>[0-9]+)/$', question, name = 'question'),
	url(r'^login/$', login, name = 'login'),
	url(r'^signup/$', signup, name = 'signup'),
	url(r'^settings/$', settings, name = 'settings'),
	url(r'^ask/$', ask, name = 'ask'),
]