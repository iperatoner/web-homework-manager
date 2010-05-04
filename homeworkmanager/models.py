from datetime import datetime
from django.db import models
from django.contrib.auth.models import User    

class Teacher(models.Model):
    gender_title = models.CharField(max_length=16)
    surname = models.CharField(max_length=32)

    def __unicode__(self):
        return '%s %s' % (self.gender_title, self.surname)


class Subject(models.Model):
    name = models.CharField(max_length=32)
    teacher = models.ForeignKey(Teacher)

    def __unicode__(self):
        return '"%s" (%s %s)' % (self.name, 
            self.teacher.gender_title, self.teacher.surname)


class Homework(models.Model):
    short_description = models.CharField(max_length=128)
    long_description = models.TextField()
    subject = models.ForeignKey(Subject)
    date_added = models.DateTimeField(default=datetime.now)
    date_ends = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '"%s" (%s)' % (self.short_description,
            self.subject.name)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    test = models.CharField(max_length=10,default='')
    finished_homework = models.ManyToManyField(Homework, 
        through='FinishedHomework')

    def __unicode__(self):
        return '%s\'s profile' % self.user.username


class FinishedHomework(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    homework = models.ForeignKey(Homework)
    date_finished = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return '%s finished "%s" (%s)' % (self.user_profile.user.username,
            self.homework.short_description, self.homework.subject.name)


class HomeworkComment(models.Model):
    user = models.ForeignKey(User)
    homework = models.ForeignKey(Homework, related_name='comment_set')
    date_added = models.DateTimeField(default=datetime.now)
    text = models.TextField()

    def __unicode__(self):
        return '%s writes: %s' % (self.user.username, self.text)
