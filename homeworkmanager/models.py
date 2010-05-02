from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    gender_title = models.CharField(max_length=16)
    surname = models.CharField(max_length=32)

    def __unicode__(self):
        return 'Teacher: %s %s' % (self.gender_title, self.surname)


class Subject(models.Model):
    name = models.CharField(max_length=32)
    teacher = models.ForeignKey(Teacher)

    def __unicode__(self):
        return 'Subject: "%s" of teacher %s %s' % (self.name, 
            self.teacher.gender_title, self.teacher.surname)

class Homework(models.Model):
    short_description = models.CharField(max_length=128)
    long_description = models.TextField()
    subject = models.ForeignKey(Subject)
    date_added = models.DateTimeField(default=datetime.now)
    date_ends = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Homework: "%s" in subject %s' % (self.short_description,
            self.subject.name)


class HomeworkComment(models.Model):
    user = models.ForeignKey(User)
    homework = models.ForeignKey(Homework, related_name='comment_set')
    date_added = models.DateTimeField(default=datetime.now)
    text = models.TextField()

    def __unicode__(self):
        return '%s writes: %s' % (self.user.username, self.text)
