from django.contrib import admin
from .models import (
    Student,
    Teacher,
    Manager,)
    
# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Manager)