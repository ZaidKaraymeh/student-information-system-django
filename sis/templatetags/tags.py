from django import template
from users.models import AssignmentSubmission

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
    
register.filter('is_submitted', is_submitted)