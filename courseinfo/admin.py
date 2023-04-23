from django.contrib import admin

from .models import Semester, Section, Course, Student, Instructor, Registration, Period, Year

admin.site.register(Period)
admin.site.register(Year)
admin.site.register(Section)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Registration)
