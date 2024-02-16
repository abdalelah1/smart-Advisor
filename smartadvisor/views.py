from django.shortcuts import render,redirect
from .function import *
from .algorithm import *
from .models import *
import os
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
    all_course_names=[]
    courses_map={}
    start_time = timezone.now()
    map = getCourseswithstudents(1)
    end_time = timezone.now()
    all_graduate_courses()
    university_map, college_map=all_optinal_courses()
    print(len(all_course_names))
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
    if request.method == 'POST' and request.FILES.get('excelFile'):
        uploaded_file = request.FILES['excelFile']
        with open('static/excel/' + uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
    return render(request, 'help/help.html', {'uploaded_success': True})
def elective(request):
    electivemap={}
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
    if request.method == 'POST':
        semester_level = request.POST.get('SemesterLevel')
        uploaded_file = request.FILES['excelFile']

        # تحديد مسار مجلد التخزين
        storage_path = 'static/excel/'

        # حذف الملفات السابقة
        for file_name in os.listdir(storage_path):
            file_path = os.path.join(storage_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

        # تخزين الملف الجديد
        with open(os.path.join(storage_path, uploaded_file.name), 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        print(semester_level)

        # قد تقوم هنا بتحديث النموذج أو أداء أي عملية أخرى
        return render(request, 'help/help.html', {'uploaded_success': True})

    return render(request, 'help/help.html')
def general(request):
    return render (request,'general/general.html')
def college(request):
    return render (request,'college/college.html')
def department(request):
    return render (request,'department/department.html')
def major(request):
    majors=Major.objects.all()
    print(majors)
    context={
        'majors':majors
    }
    return render (request,'major/major.html',context)
@login_required(login_url='login')
def students(request):
    if request.user.is_staff:
        logout(request)
    user = request.user
    
    students = Student.objects.filter(major__department=user.advisor.department )
    print(len(students))
    context={}
    context={
        'students':students
    }
    return render (request,'students/students.html',context)
def student_details(request, student_id):
    # Retrieve the student object from the database using the student_id
    try:
        student = Student.objects.get(university_ID=student_id)
    except Student.DoesNotExist:
        # Handle the case where the student is not found
        return render(request, 'student_details/student_not_found.html')

    # Fetch details for the selected student using the function
    student_details = get_students_details(student_id)

    # Pass the student object and their details to the template
    context = {
        'student': student,
        'student_details': student_details,
    }
    return render(request, 'student_details/student_details.html', context)
def department_details(request):
    
    departments = Department.objects.all()
    
    for department in departments:
        majors = department.major_set.all()
        department.filtered_majors = majors
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
def student_details(request, student_id):
    student2= Student.objects.get(university_ID=201810098)
    coursess= Course.objects.get(code='ENIT4315')
    remaining_courses, completed_courses, conditional_courses, fail_courses, _, optional_map = get_students_details(student2.university_ID)
    if coursess.code in remaining_courses and  student2.level != coursess.level and check_prerequist(coursess.code,student2.university_ID) and int(student2.Hours_count) >= int(coursess.hours_condition):
        print(True,True)
    print('preREquistis',check_prerequist('ENIT4315',201810098))
    try:
        student = Student.objects.get(university_ID=student_id)
    except Student.DoesNotExist:
        return render(request, 'student_details/student_not_found.html')

    remaining_courses_for_student , completed_courses , conditional_courses,fail_courses ,fail_passed,optional_map= get_students_details(student_id)

    for key in optional_map:
        if optional_map[key]=='Passed':
            continue
        remaining_courses_for_student=remaining_courses_for_student+optional_map[key][1]['remaining_course']
    
    print(len(remaining_courses_for_student))
    filtered_courses = []

    for index, course_code in enumerate(remaining_courses_for_student):
        course=None
        try :
            course = Course.objects.get(code=course_code)
            if not course.is_reuqired and course.type.id == 1 and student.major not in course.majors.all():
               print(course.name, True)
            else:
                filtered_courses.append(course)

        except :
          course=  University_Courses.objects.get(code=course_code)
          filtered_courses.append(course)
          continue
      
    # الآن يمكنك استخدام filtered_courses كقائمة جديدة
    remaining_courses_for_student = filtered_courses
    conditional_courses = list(conditional_courses)
    fail_courses = list(fail_courses)
    completed_courses=list(completed_courses)

    # تحديث العناصر في القوائم
    for index, course_code in enumerate(conditional_courses):
        course=None
        try :
             course = Course.objects.get(code=course_code)
        except :
          course=  University_Courses.objects.get(code=course_code)
        conditional_courses[index] = course
    for index, course_code in enumerate(fail_courses):
        course=None
        try :
             course = Course.objects.get(code=course_code)
        except :
          course=  University_Courses.objects.get(code=course_code)
        fail_courses[index] = course
    for index, course_code in enumerate(completed_courses):
        course=None
        try :
             course = Course.objects.get(code=course_code)
        except :
          course=  University_Courses.objects.get(code=course_code)
        completed_courses[index] = course
    same_level,less_level=get_recomended_for_student(student_id,remaining_courses_for_student)
    print(remaining_courses_for_student)
    context = {
        'same_level':same_level,
        'less_level':less_level,
        'student': student, 
        'remaining_courses_for_student': remaining_courses_for_student,
        'completed_courses':completed_courses,
        'conditional_courses':conditional_courses,
        'fail_courses':fail_courses,
      }
    return render(request, 'student_details/student_details.html', context)
@csrf_exempt
def save_major(request):
    majors=Major.objects.all()
    print(majors)
    context={
        'majors':majors
    }
    if request.method == 'POST':
        department=request.user.advisor.department
        major_name = request.POST.get('majorName')
        # Validate the data if needed
        Major.objects.create(name=major_name,department=department)
        print(major_name)
        return render(request, 'major/major.html',context) 

@csrf_exempt 
def save_course(request):
    majors=Major.objects.all()
    print(majors)
    context={
        'majors':majors
    }
    print('from sav_course')
    if request.method == 'POST':
        course_name = request.POST.get('courseName')
        course_code = request.POST.get('courseCode')
        courseCredit = request.POST.get('courseCredit')
        type = request.POST.getlist('coursetype')
        courseRequired = request.POST.get('courseRequired')
        hoursCondition = request.POST.get('hoursCondition')
        major_id = request.POST.get('majorId') 
        level = Level.objects.get(level='3.1')
        course_type = Course_Type.objects.get(id=1)
        
        for major_pk in type:
            major = Major.objects.get(pk=major_pk)
            Course.objects.create(
                name=course_name,
                code=course_code,
                level=level,
                credit=courseCredit,
                is_reuqired=0,
                type=course_type,
                hours_condition=hoursCondition,
            ).majors.add(major)

        return render(request, 'major/major.html', context)
@csrf_exempt 
def insert_excelFile(request):
    # insert_excel_file()
    # calcGpaForAllStydents()
    level_for_students()
    return render(request, 'help/help.html', {'uploaded_success': False})
def logout_view(request):
    logout(request)
    # قد ترغب في توجيه المستخدم إلى صفحة معينة بعد تسجيل الخروج، على سبيل المثال:
    return redirect('login')