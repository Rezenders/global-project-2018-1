from gluon import current

def _add_to_students(form):
    group_id = current.auth.id_group(role='Students')
    user_id = form.vars.id
    if group_id is None:
        group_id = current.auth.add_group('Students', 'students group')
    current.auth.add_membership(group_id, user_id)

def _add_to_manager(form):
    group_id = current.auth.id_group(role='Managers')
    user_id = form.vars.id
    if group_id is None:
        group_id = current.auth.add_group('Managers', 'Managers group')
    current.auth.add_membership(group_id, user_id)

def _add_to_upper_manager(form):
    group_id = current.auth.id_group(role='Upper Managers')
    user_id = form.vars.id
    if group_id is None:
        group_id = current.auth.add_group('Upper Managers', 'Upper Managers group')
    current.auth.add_membership(group_id, user_id)
