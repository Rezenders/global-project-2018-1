from users import _add_to_students

@auth.requires_membership('Managers')
def add_student():
    form = SQLFORM(db.auth_user)
    if form.validate():
        admin_user = auth.user
        auth.get_or_create_user(form.vars)
        _add_to_students(form)
        auth.user = admin_user

    return dict(form=form)

@auth.requires_membership('Upper Managers')
def add_manager():
    form = SQLFORM(db.auth_user)
    if form.validate():
        admin_user = auth.user
        auth.get_or_create_user(form.vars)
        _add_to_managers(form)
        auth.user = admin_user

    return dict(form=form)

@auth.requires_membership('Upper Managers')
def add_uppermanager():
    form = SQLFORM(db.auth_user)
    if form.validate():
        admin_user = auth.user
        auth.get_or_create_user(form.vars)
        _add_to_upper_managers(form)
        auth.user = admin_user

    return dict(form=form)

@auth.requires_membership('Managers')
def show():
    users = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
    return dict(users=users)

@auth.requires_membership('Managers')
def delete_user():
    user_id = request.args[0]
    db(db.auth_user.id == user_id).delete()
    return redirect(URL('show'))
