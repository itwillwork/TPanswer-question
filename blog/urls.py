from django.conf.urls import url
from views import simple, index, hot_questions
from views import tag, question, log_in, log_out, signup, ask, settings, create_answer
from views import change_rating_answer, change_rating_question, check_answer
from ask_nurullin.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	url(r'^a/$', simple, name = 'simple'),
	url(r'^$', index, name = 'index'),
	url(r'^hot/$', hot_questions, name = 'hot_questions'),
	url(r'^tag/(?P<tag_name>[-\w]+)/$', tag, name = 'tag'),
	url(r'^create_answer/$', create_answer, name = 'create_answer'),
	url(r'^question/(?P<question_id>[0-9]+)/$', question, name = 'question'),
	url(r'^accounts/login/$', log_in, name = 'log_in'),
	url(r'^accounts/logout/$', log_out, name = 'log_out'),
	url(r'^signup/$', signup, name = 'signup'),
	url(r'^accounts/$', settings, name = 'settings'),
	url(r'^accounts/ask/$', ask, name = 'ask'),
	url(r'^change_rating_answer/$', change_rating_answer, name = 'change_rating_answer'),
	url(r'^change_rating_question/$', change_rating_question, name = 'change_rating_question'),
	url(r'^check_answer/$', check_answer, name = 'check_answer'),


] 
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()