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

register.filter('is_submitted', is_submitted)
register.filter('date_submitted', date_submitted)
register.filter('student_grade', student_grade)
# register.filter('all_submitted', all_submitted)