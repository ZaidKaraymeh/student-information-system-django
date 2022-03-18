from time import time
from django import template
from users.models import AssignmentSubmission, Assignment, Grade, AttendanceReport, Fee, FeeReport
import html
from django.utils import timezone
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

def is_submitted_late(value, arg):
    assignment_id, user_id = value.id, arg.id
    try:
        asn = Assignment.objects.get(id=assignment_id)
        sub = AssignmentSubmission.objects.get(assignment__id = assignment_id, student__id = user_id)
        
        return sub.submitted_at > asn.due_date
        

    except:
        asn = Assignment.objects.get(id=assignment_id)
        return timezone.now() > asn.due_date

def assignment_grade(value, arg):
    assignment_id, user_id = value.id, arg.id
    try:
        asn = Assignment.objects.get(assignment__id = assignment_id)
        grade = asn.students_grades.filter(student__id=user_id).first()
        print(grade)
        return grade.point_grade
    except:
        return 0

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
    return Assignment.objects.filter(course=value).order_by("due_date")

def reply_sender(value):
    reply = value.replies.last()
    return reply.sender

def absence_student(student, course):
    return AttendanceReport.objects.filter(course=course, student=student, is_absent=True).count()

def average_grade_student(student, course):
    grades = Grade.objects.filter(course=course, student=student)

    if grades.count() == 0:
        return "0.00"

    sum = 0
    for grade in grades:
        sum += (grade.point_grade / grade.possible_points)
    
    avg = (sum/grades.count()) * 100
    avg = round(avg, 2)
    return avg
    


def assignment_unsubmitted(value, arg):
    assignment_id, user_id = value.id, arg.id
    obj = AssignmentSubmission.objects.get(assignment__id=assignment_id, student__id=user_id)
    return obj.submitted
def unread_notif(value):
    return value.notifications.unread().count()

def form_iter(form, iter):
    s = f'{form[iter]}'
    l = ['<td>', '</td>', '<th>', '</th>', '<tr>', '</tr>']
    for tag in l:
        s = s.replace(tag, '')
    
    print(type(form))
    print(type(form[iter]))
    print(form[iter])

    return s

"""

pick year for fee same as course year and student

"""
# def student_fee(value):
#     report = FeeReport.objects.get(student)
#     return reply.sender

def fee_remaining(fee_report):
    report = FeeReport.objects.get(id=fee_report.id)
    fee = Fee.objects.last()

    return fee.amount_needed - report.amount_paid


def paid_full(student):
    try:

        report = FeeReport.objects.get(student=student)
        fee = Fee.objects.get(student_fees__id = report.id)
        return "Yes" if report.amount_paid >= fee.amount_needed else "No"
    except:
        return "No"

def date_paid_full(student):
    try:
        report = FeeReport.objects.get(student=student)
        fee = Fee.objects.get(student_fees__id = report.id)
        return report.date_paid_full if report.amount_paid >= fee.amount_needed else "---"
    except:
        return "---"


register.filter('is_submitted', is_submitted)
register.filter('is_submitted_late', is_submitted_late)
register.filter('date_submitted', date_submitted)
register.filter('student_grade', student_grade)
register.filter('course_id_modulus', course_id_modulus)
register.filter('assignment_grade', assignment_grade)
register.filter('assignments_course', assignments_course)
register.filter('absence_student', absence_student)
register.filter('average_grade_student', average_grade_student)
register.filter('assignment_unsubmitted', assignment_unsubmitted)
register.filter('unread_notif', unread_notif)
register.filter('reply_sender', reply_sender)
register.filter('form_iter', form_iter)
register.filter('fee_remaining', fee_remaining)
register.filter('paid_full', paid_full)
register.filter('date_paid_full', date_paid_full)
# register.filter('all_submitted', all_submitted)