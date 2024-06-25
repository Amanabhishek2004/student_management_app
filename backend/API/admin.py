from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(staff_data)
admin.site.register(Grade)
admin.site.register(assignements)
admin.site.register(Assignmnet_given_by_teacher)
admin.site.register(Assignment_uploaded)