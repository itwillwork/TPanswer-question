from django.conf.urls import url
from views import simple
from views import index
from views import hot_questions
from views import tag
from views import question
from views import log_in
from views import log_out
from views import signup
from views import ask
from views import settings

urlpatterns = [
	url(r'^a/$', simple, name = 'simple'),
	url(r'^$', index, name = 'index'),
	url(r'^hot/$', hot_questions, name = 'hot_questions'),
	url(r'^tag/(?P<tag_name>[-\w]+)/$', tag, name = 'tag'),
	url(r'^question/(?P<question_id>[0-9]+)/$', question, name = 'question'),
	url(r'^accounts/login/$', log_in, name = 'log_in'),
	url(r'^accounts/logout/$', log_out, name = 'log_out'),
	url(r'^signup/$', signup, name = 'signup'),
	url(r'^accounts/$', settings, name = 'settings'),
	url(r'^accounts/ask/$', ask, name = 'ask'),
]