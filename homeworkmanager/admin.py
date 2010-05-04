from django.contrib import admin
from homeworkmanager.models import Teacher, Subject, Homework, HomeworkComment, FinishedHomework, UserProfile

admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Homework)
admin.site.register(HomeworkComment)
admin.site.register(FinishedHomework)
admin.site.register(UserProfile)
