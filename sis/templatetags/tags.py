from django import template
from users.models import AssignmentSubmission, Assignment, Grade

register = template.Library()


# @register.simple_tag
# def is_student_assignment_submitted(user_id, assignment_id):
#     try:
#         exists = AssignmentSubmission.objects.get(assignment__id = assignment_id, customuser__id = user_id)
#         if (exists.submitted == True):
#             return True
#         return False
#     except:
#         return False

def is_submitted(value, arg):
    assignment_id, user_id = value.id, arg.id
    try:
        exists = AssignmentSubmission.objects.get(assignment__id = assignment_id, student__id = user_id)
        return exists.submitted
    except:
        return False
def assignment_grade(value, arg):
    assignment_id, user_id = value.id, arg.id
    try:
        asn = Assignment.objects.get(assignment__id = assignment_id)
        grade = asn.students_grades.filter(student__id=user_id).first()

        return grade.point_grade
    except:
        return False

def date_submitted(value, arg):
    assignment_id, user_id = value.id, arg.id
    try:
        exists = AssignmentSubmission.objects.get(assignment__id = assignment_id, student__id = user_id)
        return exists.submitted_at
    except:
        return "---"
def student_grade(value, arg):
    assignment_id, user_id = value.id, arg.id
    try:
        asn = Assignment.objects.get(id=assignment_id)
        grade_obj = asn.students_grades.filter(student__id=user_id).first()
        return grade_obj.point_grade
    except:
        return 0

# def all_submitted(value):
    # return Assignment.objects.filter(assignment__id = value.id).student_submissions.all()


def course_id_modulus(value):
    return value.id % 10


def assignment_grade(value, arg):
    return value.students_grades.get(student__id=arg.id).point_grade

def assignments_course(value):
    return Assignment.objects.filter(course=value)
def unread_notif(value):
    return value.notifications.unread().count()

register.filter('is_submitted', is_submitted)
register.filter('date_submitted', date_submitted)
register.filter('student_grade', student_grade)
register.filter('course_id_modulus', course_id_modulus)
register.filter('assignment_grade', assignment_grade)
register.filter('assignments_course', assignments_course)
register.filter('unread_notif', unread_notif)
# register.filter('all_submitted', all_submitted)