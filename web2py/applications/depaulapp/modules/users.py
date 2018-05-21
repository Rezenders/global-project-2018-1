from gluon import current

def _add_to_students(form):
    group_id = current.auth.id_group(role='students')
    user_id = form.vars.id
    if group_id is None:
        group_id = current.auth.add_group('students', 'students group')
    current.auth.add_membership(group_id, user_id)

