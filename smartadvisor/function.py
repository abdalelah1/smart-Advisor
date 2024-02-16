from .models import *
from collections import Counter
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from collections import defaultdict
import copy
from itertools import chain

import pymongo
from pymongo import MongoClient
import pandas as pd 
client = MongoClient("mongodb://localhost:27017/")
database = client["advisor"]
def tostring(object1):
    return str(object1)
def RemainingCourses(all_courses, completed_courses):
    all_courses_set = set(all_courses)
    completed_courses_set = set(completed_courses)
    remaining_courses_set = all_courses_set - completed_courses_set
    remaining_courses = list(remaining_courses_set)

    return remaining_courses
def letter_grade_to_numeric(grade):
    if grade =='A+':
        return 98
    elif grade == 'A':
        return 95
    elif grade == 'A-':
        return 90
    elif grade == 'B+':
        return 85
    elif grade == 'B':
        return 80
    elif grade == 'B-':
        return 75
    elif grade == 'C+':
        return 70
    elif grade == 'C':
        return 65  
    elif grade == 'C-':
        return 60 
    elif grade == 'D+':
        return 55 
    elif grade == 'D':
        return 50
    elif grade== 'F' :
        return 0
    elif grade =='W':
        return 'W'
    else :
        
        return 0

def allcourses():
    courses = Course.objects.all()
    university_courses = University_Courses.objects.all()
    list_of_courses = [course.code for course in courses] + [u_course.code for u_course in university_courses]
    return list_of_courses
def get_students_details(student_id):
    completed_courses = []
    fail_courses = []
    conditional_courses = []
    number_elective=0
    number_university_un_required =0
    number_college_un_required=0
    credits_completed=0
    credits_conditional=0
    fail_passed=[]
    elective_complete =[]
    universite_optional_passed =[]
    college_optional_passsed =[]
    elective_remaining =[]
    university_optional_remaining=[]
    college_optional_remaining=[]
    drop_courses = []
    
    optional_map={
        'college':'',
        'elective':'',
        'university':'',
    }

    try:
        student = Student.objects.get(university_ID=student_id)
    except Student.DoesNotExist:
        return "Student not found"
    number_elective=int(student.major.department.no_required_Elecvtive)
    number_college_un_required=int(student.major.department.college.number_of_required_optional_course)
    number_university_un_required = int (student.major.department.college.university.no_university_courses_required)
    all_student_courses = Course_History.objects.filter(student=student)
    for course in all_student_courses:
        if course.course :
          
            credits = course.course.credit  
            course_code = course.course.code
        else : 
            
            credits = course.universit_course.credit  
            course_code = course.universit_course.code
        # uni_code = course.universit_course.code
        ###############################################   
        if course.degree == 'W':
            drop_courses.append(course_code)
        elif letter_grade_to_numeric( course.degree )> 59:
            credits_completed+=int(credits)
            completed_courses.append(course_code)
            # completed_courses.append(uni_code)
        elif letter_grade_to_numeric( course.degree ) < 50:
            fail_courses.append(course_code)
            # fail_courses.append()
        else:
            conditional_courses.append(course_code)
            # conditional_courses.append(uni_code)
            credits_conditional+=int(credits)
    all_courses = allcourses()
    
    remaining_courses_for_student = RemainingCourses(all_courses, completed_courses) +drop_courses
    for course in drop_courses:
        if course in remaining_courses_for_student:
            remaining_courses_for_student.remove(course)
        
    for course in fail_courses:
        if course in completed_courses:
            fail_courses.remove(course)
            fail_passed.append(course)
    for course in conditional_courses:
        if course in completed_courses:
            conditional_courses.remove(course)
    if float(student.GPA) >2.00 :
        conditional_passed = set(remaining_courses_for_student) & set(conditional_courses)
        remaining_courses_for_student = set(remaining_courses_for_student) - conditional_passed
        completed_courses  = set(completed_courses).union(set(conditional_courses))     
    for code in completed_courses :
        course = None
        try :
            course = Course.objects.get(code = code)

            if course.is_reuqired==False and course.type.id==1:
                elective_complete.append(code)

            elif course.is_reuqired==False and course.type.id==2:
                college_optional_passsed.append(code)
        except : 
            course = University_Courses.objects.get(code = code)
  
            if course.is_reuqired==False and code in completed_courses :
                universite_optional_passed.append(code)
    key_delete=[]
    for code in remaining_courses_for_student :
        try :
            course = Course.objects.get(code = code)
            if course.is_reuqired==False and course.type.id==1:            
                elective_remaining.append(code)
                key_delete.append(code)
            elif course.is_reuqired==False and course.type.id==2:
                college_optional_remaining.append(code)
                key_delete.append(code)
        except : 
            course = University_Courses.objects.get(code = code)
            university_optional_remaining.append(code)
            key_delete.append(code)
    for code in key_delete : 
        remaining_courses_for_student.remove(code)
    if len(college_optional_passsed) == number_college_un_required:
        optional_map['college']='Passed'
    else : 
        optional_map['college']=(college_optional_passsed, {'remaining_count ':number_college_un_required - len(college_optional_passsed),
                                                            'remaining_course':college_optional_remaining})
    if len(universite_optional_passed) == number_university_un_required:
        optional_map['university']='Passed'
    else : 
        optional_map['university']=(universite_optional_passed, {'remaining ':number_university_un_required- len(universite_optional_passed),
                                                                'remaining_course':university_optional_remaining
                                                                 })
    if len(elective_complete) == number_elective:
        optional_map['elective']='Passed'
    else : 
        optional_map['elective']=(elective_complete, {'remaining ':number_elective- len(elective_complete),
                                                      'remaining_course':elective_remaining
                                                      })
    for course in fail_courses:
        if course in completed_courses:
            fail_courses.remove(course)
            fail_passed.append(course)
    for course in conditional_courses:
        if course in completed_courses:
            conditional_courses.remove(course)
    return list(remaining_courses_for_student),set( completed_courses), set(conditional_courses), set(fail_courses) , set(fail_passed),optional_map
def courses_with_remaining_students():
    courses_map = {}  
    optinal_map={}

    all_students = Student.objects.all()
    
    for student in all_students:
        student_id = student.university_ID
        remaining_courses_for_student, _, _, _ ,_,optional= get_students_details(student_id=student_id)
        
        courses_map[student_id] = remaining_courses_for_student
        optinal_map[student_id]=optional
    return courses_map,optinal_map
def count_students_per_course():
    courses_map,_ = courses_with_remaining_students()
    course_counts = Counter()

    # Count the number of students for each course
    for student_id, course_code in courses_map.items():
        for course in course_code:
            course_counts[course] += 1

    # Create a dictionary to store the result
    course_data = {}
    # Group the data by course ID
    for student_id, course_code in courses_map.items():
        for course in course_code:
            if course in course_data:
                course_data[course][0].append(student_id)
                course_data[course][1] += 1
            else:
                course_data[course] = [[student_id], 20]

    # Filter courses with 20 or more students
    popular_courses = [data for data in course_data.values() if data[1] >= 20]
    less_popular_courses = [data for data in course_data.values() if data[1] < 20]
    test_courses = course_data.copy()

    keys_to_delete = []

    # التكرار عبر العناصر في القاموس
    for key, value in test_courses.items():
        if value[1] < 20:
            keys_to_delete.append(key)

    # حذف العناصر المحددة
    for key in keys_to_delete:
        del test_courses[key]
 
    return popular_courses, less_popular_courses , test_courses
def split_course_counts_by_conditions():

    popular_courses, less_popular_courses , test_courses = count_students_per_course()

    # Define the conditions
    course_College_required = []
    course_College_not_required = []
    course_major_required = []
    course_major_not_required = []
    course_universite_required = []
    course_university_not_required = []    
    course = None
    for course_code in test_courses:
        try: 
            course = Course.objects.get(code=course_code)
            course_type = course.type.id
            is_required = course.is_reuqired  


        except ObjectDoesNotExist:
            try:
                course = University_Courses.objects.get(code=course_code)

                is_required = course.is_reuqired  
                # هنا يمكنك إضافة المزيد من المعالجة إذا لزم الأمر
            except ObjectDoesNotExist:
                print()
  
        if  isinstance(course, Course):
            if is_required and course_type==1:
                course_major_required.append(((student_id, course_code, count)))
            elif is_required and course_type==2:
                 course_College_required.append(((student_id, course_code, count)))
            elif is_required==False and course_type==1:
                course_major_not_required.append(((student_id, course_code, count)))
            elif is_required==False and course_type==2:
                 course_College_not_required.append(((student_id, course_code, count)))
        else:
            if is_required :
                course_universite_required.append((student_id, course_code, count))
            else :
                course_university_not_required.append((student_id, course_code, count))
    
def check_prerequist(course_code , student_id): 

    course =None
    student = Student.objects.get(university_ID=student_id)
    try  : 
        course = Course.objects.get(code=course_code)
    except : 
        course = University_Courses.objects.get(code= course_code)
    
    prerequisites = course.preRequst.all()
    missing_pre=[]
    remaining_courses_for_student,completed_courses,conditional_courses ,fail_courses,_,_=get_students_details(student_id) 
    for pre in prerequisites :
        if pre.code in completed_courses:
            missing_pre=[]
        else:
             missing_pre.append(pre.code)
    if missing_pre==[]:
        return True
    else :
        return False
def course_with_level(semester):
    levels = Level.objects.filter(semester_name=semester)
    courses_with_levels = {}
    university_courses_with_levels = {}
    combine_map = {}
    courses =Course.objects.filter(level__in=levels,is_reuqired=True)
    uni_courses =University_Courses.objects.filter(level__in=levels,is_reuqired=True)
    all_courses = list(chain(courses, uni_courses))

    for level in levels:
        condition1 = Q(level=level)
        condition2 = Q(is_reuqired=True)
        conditions = condition1 & condition2
        course = Course.objects.filter(conditions)
        university_courses = University_Courses.objects.filter(conditions)
        

        # Get the lists of course codes
        university_courses_list = [c.code for c in university_courses]
        courses_list = [c.code for c in course]

        # Combine both lists into a single list
        combined_courses_list = university_courses_list + courses_list

        # Store the combined list for this level
        courses_with_levels[level.level] = combined_courses_list

        # Create a map with course codes as keys and their level as values
        combine_map[level.level]=[c for c in combined_courses_list]
    return courses_with_levels, university_courses_with_levels, combine_map
def get_graduted_student():
    graduated_student={}
    list_of_studnet=[]
    students=Student.objects.filter()
    for student in students :
        if student.major :
            if int(student.major.department.full_courses_count) == int(student.Hours_count):
                continue
            else:
                if int(student.major.department.full_courses_count ) - int(student.Hours_count) <=int(student.major.department.no_hourse_Tobe_graduated):
                    graduated_student[student.university_ID]=int(student.major.department.full_courses_count ) - int(student.Hours_count) 
                    list_of_studnet.append(student)
        else :
            continue
    return graduated_student,list_of_studnet


def calculate_credits(list_of_courses): 
    course=None
    counter=0
    for code in list_of_courses:
        try:
            course= Course.objects.get(code=code)
            counter += int(course.credit)
        except :
            course=University_Courses.objects.get(code=code)
            counter += int(course.credit)
    return counter
    
def calculate_gpa(student_id):
    student = Student.objects.get(university_ID=student_id)
    remaining_courses_for_student, completed_courses, conditional_courses, fail_courses, fail_passed,_ = get_students_details(student_id)

    highest_degree = {}
    course_credits = {}

    for course_code in completed_courses.union(conditional_courses):
        highest_degree[course_code] = -1

    for course_code in completed_courses.union(conditional_courses):
        try:
            course = Course.objects.get(code=course_code)
            degree_numeric = highest_degree[course_code]

            for course_history in Course_History.objects.filter(student=student, course=course):
                degree_numeric = float(max(degree_numeric, letter_grade_to_numeric(course_history.degree)))
                highest_degree[course_code] = float(degree_numeric)
                course_credits[course_code] = float(course.credit)
        except Course.DoesNotExist:
            try:
                university_course = University_Courses.objects.get(code=course_code)
                degree_numeric = float(highest_degree[course_code])
                for course_history in Course_History.objects.filter(student=student, universit_course=university_course):
                    print(course_history.degree)
                    degree_numeric = float(max(degree_numeric, letter_grade_to_numeric(course_history.degree)))
                    highest_degree[course_code] = float(degree_numeric)
                    course_credits[course_code] = float(university_course.credit)
            except University_Courses.DoesNotExist:
                continue

    total_points = 0.0
    total_credits = 0.0

    gpa_scale = {
        50: 1.5,
        55: 1.75,
        60: 2.0,
        65: 2.25,
        70: 2.5,
        75: 2.75,
        80: 3.0,
        85: 3.25,
        90: 3.5,
        95: 3.75,
        98: 4.0
    }
    for course_code in completed_courses.union(conditional_courses):
        degree_numeric = highest_degree[course_code]
        credits = course_credits[course_code]
        gpa = gpa_scale.get(degree_numeric, 0)
        total_points += gpa * credits
        total_credits += credits

    if total_credits == 0:
        return 0

    gpa = total_points / total_credits
    rounded_gpa = round(gpa, 2)
    student.GPA=rounded_gpa
    student.Hours_count = float(total_credits)
    student.save()
    return rounded_gpa 

def assign_course_priorities():
    graduated_student_ids,_ = get_graduted_student()
    remaining_courses_map,optional_map = courses_with_remaining_students()

    course_priorities = {
        "1": {}
    }
    newmap={}
    # Assign max priority '1' to remaining courses for graduated students
    for student_id in graduated_student_ids:
        remaining_courses = remaining_courses_map.get(student_id, [])
        for course in remaining_courses:
            if course in course_priorities["1"]:
                course_priorities["1"][course].append(student_id)
            else:
                course_priorities["1"][course] = [student_id]
    modified_data = course_priorities.copy()  # لنقم بنسخ البيانات الأصلية

    for semester, courses in modified_data.items():
        for course, student_list in courses.items():
            student_count = len(student_list)
            courses[course] = (student_list, student_count)

    return modified_data,modified_data.values()
def course_with_count_same_level_or_above(test_courses):
    same_level={}
    less_level ={}
    course_level_greater_than_student={}
    
    for course_code, course_info in test_courses.items():
        course = None
        try:
            course = Course.objects.get(code=course_code)
        except:
            course = University_Courses.objects.get(code=course_code)
        for university_id in course_info[0]:
            student = Student.objects.get(university_ID=university_id)
            if int(course.level.id) ==int(student.level.id) and check_if_passed(course.code,student.university_ID) and int(student.Hours_count) >= int(course.hours_condition) :
                same_level[course_code]=course_info
                course_info[1]=len(course_info[0])
            elif int(course.level.id) <int(student.level.id):
                less_level[course_code] = course_info

            else :   
                course_level_greater_than_student[course_code]=course_info
    return same_level , less_level , course_level_greater_than_student
def number_of_student_per_course(code):
    course = None
    try:
            course = Course.objects.get(code=code)
    except:
            course = University_Courses.objects.get(code=code)
    students = Student.objects.all()
    counter = 0

    map ={}
    student_passed=[]
    for student in students: 
        if check_prerequist(code,student.university_ID) and check_if_passed(code,student.university_ID) and int(student.Hours_count) >= int(course.hours_condition) :
            student_passed.append(student.university_ID)
            counter = counter+1
    
    return [student_passed,counter ]
def check_if_passed(code, student_id):
    remaining_courses_for_student,_,_,_,_,_=get_students_details(student_id)
    if code  in remaining_courses_for_student:
        return True 
    else : 
        False
def check_course_state(code , student_id):
    _,_,conditional_courses,fail_courses,_,_=get_students_details(student_id)

    if code  in fail_courses:
        return 'f'
    elif  code  in conditional_courses :
        return 'd'
    else : return 'c' 
def number_of_student_per_fail_course (code):
    course = None
    try:
            course = Course.objects.get(code=code)
    except:
            course = University_Courses.objects.get(code=code)
    students = Student.objects.all()
    counter = 0
    cond_counter = 0
    student_cond = []
    map ={}
    student_fail=[]
    for student in students: 
        if  check_course_state(code,student.university_ID)=='f'  :
            student_fail.append(student.university_ID)
            counter = counter+1
        elif check_course_state(code,student.university_ID) =='d' and float(student.GPA)<= 2 :
            student_cond.append(code)
            cond_counter = cond_counter+1
    return [student_fail,counter ] , [student_cond,cond_counter]
def course_with_count(semester):
    course_with_count={}
    courses_with_levels , university_courses_with_levels,_=course_with_level(semester)
    list_of_course_on_this_semester = []
    for key in courses_with_levels:
        for course in courses_with_levels[key]:
         list_of_course_on_this_semester.append(course)
    for course in list_of_course_on_this_semester:
       
       course_with_count[course]=(number_of_student_per_course(course))
    return course_with_count
def fail_course_with_count(semester):
    course_with_count={}    
    cond_course={}
    students = Student.objects.all()
    courses_with_levels , _,_=course_with_level(semester)
    list_of_course_on_this_semester = []
    for key in courses_with_levels:
        for course in courses_with_levels[key]:
         list_of_course_on_this_semester.append(course)
    for course in list_of_course_on_this_semester:
       
       course_with_count[course]=(number_of_student_per_fail_course(course)[0])
       cond_course[course]=(number_of_student_per_fail_course(course)[1])
    return course_with_count , cond_course
def calculate_gpa_directly(student_id, completed_courses, conditional_courses, fail_courses):
    highest_degree = {}
    course_credits = {}

    all_courses = set(completed_courses).union(conditional_courses).union(fail_courses)

    total_points = 0.0
    total_credits = 0.0

    gpa_scale = {
        50: 1.5,
        55: 1.75,
        60: 2.0,
        65: 2.25,
        70: 2.5,
        75: 2.75,
        80: 3.0,
        85: 3.25,
        90: 3.5,
        95: 3.75,
        98: 4.0
    }

    for course_info in all_courses:
        course_code, (credit, grade) = course_info
        degree_numeric = letter_grade_to_numeric(grade)
        credits = float(credit)

        highest_degree[course_code] = degree_numeric
        course_credits[course_code] = credits

        gpa = gpa_scale.get(degree_numeric, 0)
        total_points += gpa * credits
        total_credits += credits

    if total_credits == 0:
        return 0

    gpa = total_points / total_credits
    rounded_gpa = round(gpa, 2)
    return rounded_gpa
def get_remaining_courses_for_graduates():
    remaining_graduates,_ = get_graduted_student()
    remaining_courses_data = {}
    courses_map={}
    elective_map={}
    list = []
    for student_id in remaining_graduates:
        courses_map={}
        remaining_courses_for_student, _, _, _, _, optional = get_students_details(student_id) 
        courses_map['courses'] = remaining_courses_for_student
        courses_map['college'] = optional['college']
        courses_map['elective'] = optional['elective']
        courses_map['university'] = optional['university']
        elective_map['elective'] =(optional['elective'])
        remaining_courses_data[student_id]=courses_map

    return remaining_courses_data , elective_map

def all_graduate_courses():
    client = MongoClient("mongodb://localhost:27017/")
    database = client["advisor"]
    collection = database["elective"]
    collection.delete_many({})
    elective_courses=Course.objects.filter(is_reuqired=0,type=1) 
    list_of_student=[]
    map_of_elective={}
    datatoinsert=[]
    all_Remening , elective = get_remaining_courses_for_graduates()
    for course in elective_courses :
        list_of_student=[]
        datatoinsert={}
        print(course.code)
        if course.instructor ==False:
          datatoinsert[course.code]=list_of_student
          collection.insert_one(datatoinsert)
          continue
        for student in all_Remening.keys():
             if all_Remening[student]['elective']=='Passed' :
                continue
             s = Student.objects.get(university_ID=student)
             if course.code in all_Remening[student]['elective'][1]['remaining_course'] and course.majors.filter(pk=s.major.pk).exists() :
                
                 list_of_student.append(student)
                 map_of_elective[course.code]=set(list_of_student)
        datatoinsert[course.code] = list(set(list_of_student))
        collection.insert_one(datatoinsert)
    print('daata',datatoinsert.keys())
       
    client.close( )
    return map_of_elective
def all_optinal_courses():
    client = MongoClient("mongodb://localhost:27017/")
    database = client["advisor"]
    collection1 = database["college"]
    collection2 = database["university"]
    university_optional = University_Courses.objects.filter(is_reuqired=0)
    college_optional = Course.objects.filter(is_reuqired=0, type=2)
    university_map = {}
    college_map = {}
    students = Student.objects.all()

    for student in students:
        _, _, _, _, _, optional = get_students_details(student.university_ID)

        for course in college_optional:

            if optional['college']== "Passed" :
                break
            if course.code in optional['college'][1]['remaining_course']:
                if course.code not in college_map:
                    college_map[course.code] = []
                college_map[course.code].append(student.university_ID)
        for course in university_optional:
            if optional['university'] == "Passed" :
                break
            if course.code in optional['university'][1]['remaining_course']:
                if course.code not in university_map:
                    university_map[course.code] = []
                university_map[course.code].append(student.university_ID)
    collection1.insert_one(college_map)
    collection2.insert_one(university_map)
    return university_map, college_map
def insert_excel_file():
    studentFile = pd.read_excel('./static/excel/itstudents.xlsx')
    historyFile = pd.read_excel('./static/excel/itstudents.xlsx')
    Course_History.objects.all().delete()
    Student.objects.all().delete()
    for index, row in studentFile.iterrows():

        if not Student.objects.filter(university_ID=row['ID']).exists():
            student = Student()
            student.university_ID = row['ID']
            student.name= row['الاسم']
            student.GPA = 0  # قيمة افتراضية لل GPA يمكنك تعديلها بناءً على البيانات الحقيقية
            student.Hours_count = 0
            major_name = row['major']
            try:    
                    student.major = Major.objects.get(name=major_name)
            except Major.DoesNotExist:
            # إذا لم يتم العثور على اختصاص، قم بإنشاء اختصاص جديد بقيمة افتراضية (مثل القيمة 3)
                student.major = Major.objects.get(id=3)   # قيمة افتراضية لعدد الساعات يمكنك تعديلها بناءً على البيانات الحقيقية
            student.save()
            
    for index , row in historyFile.iterrows():
        course_History = Course_History()
        student= Student.objects.get(university_ID=row['ID'])
        if row['Grade']=='-':
            continue
        if row['Grade']=='I':
            continue
        course = None
        try:

            course = Course.objects.get(code=row['Course #'])
            course_History.student = student
            course_History.course = course
            course_History.degree = row['Grade']
        except Course.DoesNotExist:
            try:
                course = University_Courses.objects.get(code=row['Course #'])

                course_History.student = student
                course_History.universit_course = course
                course_History.degree = row['Grade']
            except University_Courses.DoesNotExist:
                continue
        course_History.save()

def calcGpaForAllStydents():
    students = Student.objects.all()
    for student in students :
        gpa=calculate_gpa(student.university_ID)

def savetonosql():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["advisor"]
    results_collection = database["electiveResult"]

def coursesonlevelwithstudents(semester):
    _,graduated_students=get_graduted_student()
    levels = Level.objects.filter(semester_name=semester)   
    final_map={}
    courses =Course.objects.filter(level__in=levels,is_reuqired=True)
    uni_courses =University_Courses.objects.filter(level__in=levels,is_reuqired=True)
    all_courses = list(chain(courses, uni_courses))
    students = Student.objects.all()   
     
    for course in all_courses:
        combine_map = {'fault':[],'same level':[],'condition':[],'graduate':[],'students':[]}
        for s  in students:
            remaining_courses_for_student,completed,_,_,_,_,=get_students_details(s.university_ID)
            c=None
            try:
                c = Course.objects.get(code=course.code)
                if not Course_History.objects.filter(Q(student=s) & Q(course=c)).exists() :
                    if s in graduated_students:
                        combine_map['graduate'].append(s)
                        continue
                    elif course.level==s.level:
                        combine_map['same level'].append (s) 
                        continue
            except : 
                c= University_Courses.objects.get(code=course.code)
                if not Course_History.objects.filter(Q(student=s) & Q(universit_course=c)).exists() :
                    if s in graduated_students:
                        combine_map['graduate'].append(s)
                        continue
                    elif course.level==s.level:
                        combine_map['same level'].append (s) 
                        continue
           

        final_map[course]=combine_map
                
        return final_map
def getCourseswithstudents(semester):
    from collections import Counter

    # قائمة لتخزين أسماء المواد
    all_course_names = []

    # قائمة لتخزين الطلاب الذين تكررت أسماء المواد لديهم أكثر من 20 مرة
    students_with_repeated_courses = []
    client = MongoClient("mongodb://localhost:27017/")
    database = client["advisor"]
    collection = database["courses"]
    collection.delete_many({})
    _, graduated_students = get_graduted_student()
    levels = Level.objects.filter(semester_name=semester)
    final_map = {}
    courses = list(chain(Course.objects.filter(is_reuqired=True), University_Courses.objects.filter( is_reuqired=True)))

    for course in courses:
        combine_map = {'fault': [], 'same_level': [], 'condition': [], 'graduate': [], 'students': []}
        final_map2 = {}
        students_data = {'fault': [], 'same_level': [], 'condition': [], 'graduate': [], 'students': []}
        
        students = Student.objects.all()

        for student in students:
            remaining_courses, completed_courses, conditional_courses, fail_courses, _, optional_map = get_students_details(student.university_ID)
            if course.code in fail_courses and  student.university_ID not in  graduated_students:
                combine_map['fault'].append(student)
                students_data['fault'].append(student.university_ID)
                continue
            elif course.code in remaining_courses and student.level == course.level and student not in graduated_students and check_prerequist(course.code,student.university_ID)and  int(student.Hours_count) >= int(course.hours_condition):
                combine_map['same_level'].append(student)
                students_data['same_level'].append(student.university_ID)
                continue
            elif course.code in conditional_courses and student.university_ID not in graduated_students:
                combine_map['condition'].append(student)
                students_data['condition'].append(student.university_ID)
                continue
            elif course.code in remaining_courses and  student.level != course.level and student not in graduated_students and check_prerequist(course.code,student.university_ID) and int(student.Hours_count) >= int(course.hours_condition):
                combine_map['students'].append(student)
                students_data['students'].append(student.university_ID)
                continue
            elif course.code in remaining_courses and student in graduated_students and check_prerequist(course.code,student.university_ID):
                combine_map['graduate'].append(student)
                students_data['graduate'].append(student.university_ID)
        print(course.code)
        final_map[course] = combine_map
        final_map2[course.code]= students_data
        
        collection.insert_one(final_map2)

    return final_map

            

def insertStudentMajor():    
    student_count = Student.objects.filter(major__isnull=False).count()
    major = Major.objects.get(id=3)
    # studentFile=pd.read_excel('./static/excel/studentswithmajor.xlsx')
    # for index , row in studentFile.iterrows():
    #     if not Student.objects.filter(university_ID=row['ID']).exists():
    #         continue
    #     else:
    
    #         student= Student.objects.get(university_ID=row['ID'])
  
    #         major = Major.objects.get(name = row['major'])
    #         student.major=major
    #         student.save()
    for student in Student.objects.filter(major__isnull=True):
            student.major=major
            student.save()


def get_recomended_for_student(student_id,remaining_courses):
    student  =Student.objects.get(university_ID=student_id)
    _, completed_courses , conditional_courses,fail_courses ,fail_passed,optional_map=get_students_details(student_id)

    collection_college =database["college"]
    collection_university =database["university"]
    collection_courses = database['courses']
    collection_elective = database['elective']
    
    document_college = collection_college.find_one()
    documents_university = collection_university.find_one()
    document_courses = collection_courses.find()
    document_elective = collection_elective.find()
    all_keys = set()
    same_level=[]
    less_level=[]
    for document in document_elective:
        all_keys.update(document.keys())
    for document in document_courses:
        all_keys.update(document.keys())
    for course in remaining_courses :
        if course.code in all_keys:
            if course.level==student.level:
               same_level.append(course)
            elif float(course.level.level)<= float(student.level.level):
                less_level.append(course)
    return same_level ,less_level

def levels_with_requirements():
    # استعلام يسترجع جميع المستويات التي تحتوي على شروط
    levels_with_requirements = Level.objects.filter(levelrequirement__isnull=False).distinct()
    level_for_students()

def level_for_spacific_student(student_id):
    student = Student.objects.get(university_ID= student_id)
    hours_count =student.Hours_count
    college = student.major.department.college
    # الحصول على المستويات التي تحتوي على شروط للكلية المحددة
    levels_with_requirements = Level.objects.filter(
        levelrequirement__isnull=False,
        levelrequirement__college=college
    ).distinct()
    student_level = None
    for level in levels_with_requirements:
        level_requirement = level.levelrequirement_set.first()
        if level_requirement.number_of_required_optional_courses <= hours_count:
            student_level = level
    level_student = Level.objects.get(level=student_level)
    student.level=level_student
    student.save()

def level_for_students():
    students= Student.objects.all()
    for student in students:
         level_for_spacific_student(student.university_ID)

