from django.shortcuts import render,redirect
from .function import *
from .algorithm import *
from .models import *
from django.http import JsonResponse
import timeit
from django.utils import timezone
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
database = client["advisor"]
# Create your views here.

def test(request):
    insertStudentMajor()
    courses_map={}
    start_time = timezone.now()
    map = getCourseswithstudents(1)
    end_time = timezone.now()
    elapsed_time = end_time - start_time
    print(elapsed_time)
    collection = database["courses"]
    result = collection.find({}, {"_id": 0})
    for r in result:
        for key, value in r.items():
             courses_map[key]=value    
    context={
        'final_map' : courses_map
    }
    return render(request, 'test/test.html', context)
def elective(request):
    electivemap={}
    all_graduate_courses()
    # university_map, college_map=all_optinal_courses()
    collection = database["elective"]
    result = collection.find({}, {"_id": 0})
    for r in result:
        for key, value in r.items():
             electivemap[key]=value
    context ={
        'elective' : electivemap    
    }
    return render(request, 'elective/elective.html',context)
###############
@login_required(login_url='login')
def home (request) : 
    if request.user.is_superuser:
        User.objects.filter(is_staff=True).exclude(username=request.user.username).update(is_active=False)
        
        # تسجيل الخروج من الحساب الحالي
        logout(request) 
    user  = request.user
    context = {}
    context= {
        'user':user
    }
    return render (request,'home/home.html',context)
@login_required(login_url='login')
def allcourses(request):
    courses_required = Course.objects.filter(is_reuqired=True)
    courses_not_required = Course.objects.filter(is_reuqired=False ,type=2)
    elective = Course.objects.filter(is_reuqired=False ,type=1)
    context={
        'courses_required':courses_required,
        'courses_not_required':courses_not_required,
        'elective':elective
    }
    return render (request,'allcourses/allcourses.html',context)
def courses(request):
    collection = database["courses"]
    elective_result = database["elective"]
    university_result = database["university"]
    faculity_result = database["college"]
    result = collection.find({}, {"_id": 0})  
    courses_map={}
    elective = elective_result.find({}, {"_id": 0})  
    elective_map = {}
    faculity = {}
    university={}
    faculity_result.find_one({}, {"_id": 0})
    university_result.find_one({}, {"_id": 0})
    for r in result:
    # الوصول إلى الـ key والـ value لكل وثيقة
        for key, value in r.items():
            getcourse = None
            try:
                getcourse = Course.objects.get(code=key )
            except:
                getcourse = University_Courses.objects.get(code=key )
            courses_map[getcourse]=value
    for r in elective:
    # الوصول إلى الـ key والـ value لكل وثيقة
        for key, value in r.items():
            getcourse = Course.objects.get(code=key )
            elective_map[getcourse]=value
    test_map={}
    test_map = faculity_result.find_one({}, {"_id": 0})
    

    for key  in test_map:
        course = Course.objects.get(code = key)
        faculity[course]=test_map[key]
    test_map = university_result.find_one({}, {"_id": 0})

    for key  in test_map:
        course = University_Courses.objects.get(code = key)
        university[course]=test_map[key]
            
    context={
        'final_map' : courses_map,
        'elective_map':elective_map,
        'college_map':faculity,
        'university_map':university
    }           
    
    return render (request,'courses/courses.html',context)
def student_on_course (request,course , key):
    list_of_student=[]
    if key == 'elective':
        collection = database["elective"]
        document = collection.find_one({course: {"$exists": True}},{"_id": 0})
        for i in document[course]:
            student = Student.objects.get(university_ID=i)
            list_of_student.append(student)
        getcourse = Course.objects.get(code=course )
        context={
            'students':list_of_student,
            'course':getcourse,
        }
        return render (request,'students/students.html', context)
    else: 
        collection = database["courses"]
        list_of_student =[]
        document = collection.find_one({course: {"$exists": True}},{"_id": 0})
        for i in document[course][key]:
            student = Student.objects.get(university_ID=i)
            list_of_student.append(student)
        getcourse = None
        try:
            getcourse = Course.objects.get(code=course )
        except:
            getcourse = University_Courses.objects.get(code=course )

        context={
            'students':list_of_student,
            'course':getcourse,
        }
        return render (request,'students/students.html', context)
def help(request):
    return render (request,'help/help.html')
def general(request):
    return render (request,'general/general.html')
def college(request):
    return render (request,'college/college.html')
def department(request):
    return render (request,'department/department.html')
def major(request):
    return render (request,'major/major.html')
@login_required(login_url='login')
def students(request):
    user = request.user
    
    students = Student.objects.filter(major__department=user.advisor.department )
    context={}
    context={
        'students':students
    }
    return render (request,'students/students.html',context)

def department_details(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render( request,'report/report.html', context)
@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin:index')
            else : 
                login(request, user)
                return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login/login.html', {'error': error_message})
    return render(request, 'login/login.html')
def update_instructor(request):
    Course.objects.all().update(instructor=False)
    selected_courses = request.POST.getlist('selected_courses[]')
    Course.objects.filter(pk__in=selected_courses).update(instructor=True)
    all_graduate_courses()
    return render(request, 'home/home.html') 
