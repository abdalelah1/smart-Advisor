from .function import *
def recommendation_course(semester):
    combined_map = {}
    full_count=course_with_count(semester)
    _,_,combine_map=course_with_level(semester)
    fail , condition=fail_course_with_count(semester)
    same_level , less_level , course_level_greater_than_student=course_with_count_same_level_or_above(course_with_count(semester))
    for level, courses in combine_map.items():
        combined_map[level] = {}  
        for course_code in courses:
            combined_map[level][course_code] = {
                'full_count': full_count.get(course_code, [[], 0]),
                'fail': fail.get(course_code, [[], 0]),
                'condition': condition.get(course_code, [[], 0]),
                'same_level': same_level.get(course_code, [[], 0]),
        }
    return combined_map 
def elective_Algorthm():
    elective = all_graduate_courses()
    return elective