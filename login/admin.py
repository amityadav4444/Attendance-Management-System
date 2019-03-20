from django.contrib import admin
from login.models import TimeTable,Teacher,Semester,Subject,Section,Attendance_table,Student,Attendance_cell, Holiday
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import path
from login import forms
from django.shortcuts import render,redirect 
from io import StringIO
import csv
# Register your models here.

#admin.site.register(teacher)
class teacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'teacher'

class UserAdmin(BaseUserAdmin):
	inlines = (teacherInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(TimeTable)
admin.site.register(Subject)
admin.site.register(Section)
admin.site.register(Semester)
admin.site.register(Attendance_table)
admin.site.register(Attendance_cell)
admin.site.register(Holiday)

@admin.register(Student)
class Student_admin(admin.ModelAdmin):
	change_list_template = "login/heroes_changelist.html"
	def get_urls(self):
		urls = super().get_urls()
		my_urls = [path('import-csv/', self.import_csv),]
		return my_urls + urls
	
	def import_csv(self, request):
		if request.method == "POST":
			csv_file = request.FILES['csv_file']
			csvf = StringIO(csv_file.read().decode())
			reader = csv.reader(csvf, delimiter=',')
			for row in reader:
				sec = Section.objects.get(section_name=row[2])
				created = Student.objects.get_or_create(rollno=str(row[0]),name=str(row[1]),section=sec)
			
			self.message_user(request, "Your csv file has been imported")
			return redirect("..")
		
		form = forms.CsvImportForm()
		payload = {"form": form}
		return render(request, "login/csv_form.html", payload)