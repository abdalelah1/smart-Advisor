

from django.db import models ,connection
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import date,datetime
class semester_name(models.Model):
    name=models.CharField(max_length=10)
    def __str__(self) :
            return  str(self.name)  
class Level (models.Model):
    level =models.CharField(max_length=50)
    semester_name=models.ForeignKey(semester_name,on_delete=models.CASCADE,null=True)
    def __str__(self) :
            return  str(self.level)    
class University( models.Model):
    name =models.CharField(max_length=50)
    no_university_courses_required = models.IntegerField()
    def __str__(self) :
            return  str(self.name)
class University_Courses (models.Model):
    name =models.CharField(max_length=50)
    code=models.CharField(max_length=20,db_index=True)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=False)
    credit = models.CharField(max_length=10)
    is_reuqired = models.BooleanField(default=True)
    hours_condition= models.IntegerField(null=True,default=0)
    preRequst =models.ManyToManyField('self',blank=True, symmetrical=False)
    def __str__(self) :
            return  str(self.code)

class College(models.Model):
    name =models.CharField(max_length=50)
    number_of_required_optional_course = models.IntegerField(default=2)
    university= models.ForeignKey(University,on_delete=models.CASCADE,null=True)
    number_of_levels= models.IntegerField()
    def __str__(self) :
            return  str(self.name)

class Department(models.Model):
    name =models.CharField(max_length=50)
    college=models.ForeignKey(College,on_delete=models.CASCADE,null=False)
    full_courses_count =models.IntegerField()
    no_hourse_Tobe_graduated = models.IntegerField()
    no_required_Elecvtive=models.IntegerField()
    def __str__(self) :
            return  str(self.name)
class Major(models.Model):
    name =models.CharField(max_length=50)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=False)
    def __str__(self) :
            return  str(self.name)    
class Course_Type (models.Model):
    typeOfCourse =models.CharField(max_length=50)
    def __str__(self) :
            return  str(self.typeOfCourse)     
class Course(models.Model):
    name =models.CharField(max_length=50)
    code=models.CharField(max_length=20,db_index=True)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=False)
    credit = models.CharField(max_length=10)
    is_reuqired = models.BooleanField(default=True) #ساعات مسجلة
    majors = models.ManyToManyField(Major , blank=True)
    instructor =models.BooleanField(default=True)
    type = models.ForeignKey(Course_Type,on_delete=models.CASCADE,null=False)
    hours_condition= models.IntegerField(null=True,default=0)
    preRequst =models.ManyToManyField('self',blank=True, symmetrical=False)
    def __str__(self) :
            return  str(self.code)
class LevelRequirement(models.Model):
    college= models.ForeignKey(College,on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    number_of_required_optional_courses = models.IntegerField(default=2)
    # يمكنك أيضًا إضافة المزيد من الحقول الخاصة بالشروط هنا

    def __str__(self):
        return f"{self.level.level} - {self.number_of_required_optional_courses} courses"

class Student (models.Model):
    university_ID=models.CharField(max_length=50,null=True,db_index=True)
    name = models.CharField(max_length=50 , null=True)
    major=models.ForeignKey(Major,on_delete=models.CASCADE,null=True)
    GPA = models.CharField(max_length=50,null=True)
    level = models.ForeignKey(Level , on_delete=models.CASCADE,null=True)
    Hours_count= models.IntegerField(null=True)
    def __str__(self) :
            return  str(self.university_ID)
class Course_History(models.Model):
    degree = models.CharField(max_length=50)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=False,db_index=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,db_index=True)
    universit_course = models.ForeignKey(University_Courses,on_delete=models.CASCADE,null=True,db_index=True)
class Advisor (models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,null=False)
    name =  models.CharField(max_length=50)
    department = models.OneToOneField(Department , on_delete=models.CASCADE,null=True)
    def __str__(self) :
            return  str(self.name)
