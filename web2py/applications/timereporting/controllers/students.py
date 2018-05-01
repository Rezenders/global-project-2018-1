def _add_to_students(form):
    group_id = auth.id_group(role='students')
    user_id = form.vars.id
    if group_id == None:
        group_id = auth.add_group('students', 'students group')
    auth.add_membership(group_id, user_id)

@auth.requires_membership('manager')
def register():
    form = SQLFORM(db.auth_user)
    if form.validate():
        admin_user = auth.user
        auth.get_or_create_user(form.vars)
        _add_to_students(form)
        auth.user = admin_user

    return dict(form=form)

@auth.requires_membership('manager')
def show():
	students = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
	return dict(students=students)

@auth.requires_membership('manager')
def delete_user():
	user_id = request.args[0]	
	db(db.auth_user.studentID==user_id).delete()
	return redirect(URL('show'))
