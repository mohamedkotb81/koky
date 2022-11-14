import datetime
from django.utils import timezone

from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length = 250)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        # return self.pub_date >= timezone.now - datetime.timedelta(days=1)



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 250)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Todo(models.Model):
    added_date = models.DateTimeField()
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.todo_text





# ********* For Adding Choices **************
# q = Question.objects.get(pk=4)
# c = q.choice_set.create(choice_text = "Al7amdulleah", votes=0)
# c.save


# ********* For getting Votes count of choice **************
# Question.objects.get(id=1)
# q = Question.objects.get(id=1) 
# q.choice_set.all()
# q.choice_set.all()[1]
# q.choice_set.all()[1].votes

