from django.db import models
from django.contrib.auth.models import User


class Semester(models.Model):
	CHOICES = (
		(1, 'First'),
		(2, 'Second'),
		(3, 'Third'),
		(4, 'Fourth'),
		(5, 'Fifth'),
		(6, 'Sixth'),
		(7, 'Seventh'),
		(8, 'Eighth'),
	)

	semester = models.IntegerField(default=0, choices=CHOICES)
	def __str__(self):
		return str(self.semester)
		
	class Meta:
		unique_together=(('semester'),)
	

class Teacher(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	teacher_name = models.CharField(max_length=40)
	department = models.CharField(max_length=10)

	def __str__(self):
		return self.user.username
		
	class Meta:
		unique_together=(('user'),)


class TimeTable(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	
	Monday1 = models.CharField(max_length=100, blank=True)
	Monday2 = models.CharField(max_length=10, blank=True)
	Monday3 = models.CharField(max_length=10, blank=True)
	Monday4 = models.CharField(max_length=10, blank=True)
	Monday5 = models.CharField(max_length=10, blank=True)
	Monday6 = models.CharField(max_length=10, blank=True)
	Monday7 = models.CharField(max_length=10, blank=True)
	Monday8 = models.CharField(max_length=10, blank=True)
	
	Tuesday1 = models.CharField(max_length=10, blank=True)
	Tuesday2 = models.CharField(max_length=10, blank=True)
	Tuesday3 = models.CharField(max_length=10, blank=True)
	Tuesday4 = models.CharField(max_length=10, blank=True)
	Tuesday5 = models.CharField(max_length=10, blank=True)
	Tuesday6 = models.CharField(max_length=10, blank=True)
	Tuesday7 = models.CharField(max_length=10, blank=True)
	Tuesday8 = models.CharField(max_length=10, blank=True)
	
	Wednesday1 = models.CharField(max_length=10, blank=True)
	Wednesday2 = models.CharField(max_length=10, blank=True)
	Wednesday3 = models.CharField(max_length=10, blank=True)
	Wednesday4 = models.CharField(max_length=10, blank=True)
	Wednesday5 = models.CharField(max_length=10, blank=True)
	Wednesday6 = models.CharField(max_length=10, blank=True)
	Wednesday7 = models.CharField(max_length=10, blank=True)
	Wednesday8 = models.CharField(max_length=10, blank=True)
	
	Thursday1 = models.CharField(max_length=10, blank=True)
	Thursday2 = models.CharField(max_length=10, blank=True)
	Thursday3 = models.CharField(max_length=10, blank=True)
	Thursday4 = models.CharField(max_length=10, blank=True)
	Thursday5 = models.CharField(max_length=10, blank=True)
	Thursday6 = models.CharField(max_length=10, blank=True)
	Thursday7 = models.CharField(max_length=10, blank=True)
	Thursday8 = models.CharField(max_length=10, blank=True)
	
	Friday1 = models.CharField(max_length=10, blank=True)
	Friday2 = models.CharField(max_length=10, blank=True)
	Friday3 = models.CharField(max_length=10, blank=True)
	Friday4 = models.CharField(max_length=10, blank=True)
	Friday5 = models.CharField(max_length=10, blank=True)
	Friday6 = models.CharField(max_length=10, blank=True)
	Friday7 = models.CharField(max_length=10, blank=True)
	Friday8 = models.CharField(max_length=10, blank=True)
	
	def __str__(self):
		return self.user.username
		
	class Meta:
		unique_together=(('user'),)

class Subject(models.Model):
	subject_name = models.CharField(max_length=10)
	semester = models.ForeignKey(Semester,on_delete=models.CASCADE)

	def __str__(self):
		return self.subject_name
		
	class Meta:
		unique_together=(('subject_name'),)
	

class Section(models.Model):
	section_name = models.CharField(max_length=10)
	semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.section_name
		
	class Meta:
		unique_together=(('section_name'),)
		
		
class Student(models.Model):
	rollno = models.IntegerField()
	name = models.CharField(max_length=64)
	section = models.ForeignKey(Section, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
		
	class Meta:
		unique_together=(('rollno'),)


class Attendance_cell(models.Model):
	student = models.ForeignKey(Student,on_delete=models.CASCADE)
	date = models.DateTimeField()
	att = models.IntegerField(default=0)
	def __str__(self):
		return self.student.name+' '+str(self.date)


class Attendance_table(models.Model):
	section = models.ForeignKey(Section, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	attendance = models.ManyToManyField(Attendance_cell)
	def __str__(self):
		return self.section.section_name+' '+self.subject.subject_name
		
	class Meta:
		unique_together=(('section','subject'),)
	
class Holiday(models.Model):
	date = models.DateField();
	description = models.TextField()
	def __str__(self):
		return str(self.date)+' '+self.description
		
	class Meta:
		unique_together=(('date'),)
