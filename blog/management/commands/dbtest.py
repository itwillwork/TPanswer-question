from django.core.management.base import BaseCommand, CommandError
from blog.models import Tags
from blog.models import Profile
from blog.models import Question
from blog.models import Answer
from  django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        tag1 = Tags.objects.create(name = "bender") 
        tag2 = Tags.objects.create(name = "black-jack") 
        u = User.objects.create(username="Test_user", password = "5905")
        user1 = Profile.objects.create( user = u ,avatar = "http://placekitten.com/g/90/90/")
        for i in xrange(1,15):
            q = Question.objects.create(
                    title = str(i) + "Title of question", 
                    text_qest = str(i) + "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque efficitur sem quis rutrum gravida. Pellentesque vel mi aliquet diam sodales gravida a quis massa. Duis bibendum magna ac sollicitudin condimentum. Nam nibh orci, cursus ut tortor ac, tincidunt feugiat odio. Phasellus suscipit accumsan mauris sed elementum. Nullam id arcu quis tellus bibendum blandit pretium id leo. Cras eu cursus urna. ",
                    count_ans = 4,
                    rating = i,
                    author = user1,
                )
            q.tags.add(tag1, tag2)
            q.save()
            #Question.tags.add(tag1)
            for j in xrange(1, 4):
                a = Answer(
                    question = q,
                    text_ans = str(j) + " asnwer Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque efficitur sem quis rutrum gravida. Pellentesque vel mi aliquet diam sodales gravida a quis massa. Duis bibendum magna ac sollicitudin condimentum. Nam nibh orci, cursus ut tortor ac, tincidunt feugiat odio. Phasellus suscipit accumsan mauris sed elementum. Nullam id arcu quis tellus bibendum blandit pretium id leo. Cras eu cursus urna. ",
                    author = user1,
                    rating = j,
                    correct = True,
                    )
                a.save()
