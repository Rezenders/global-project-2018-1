from users import _add_to_students

@auth.requires_membership('Upper Managers','Managers')
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

@auth.requires_membership('Upper Managers','Managers')
def manage_level():
   grid = SQLFORM.smartgrid(db.auth_membership)
   return locals()

@auth.requires_membership('Upper Managers','Managers')
def manage_users():
   grid = SQLFORM.smartgrid(db.auth_user)
   #db.auth_user.show_if = (db.auth_membership.group_id=='Student')
   #form = SQLFORM(db.purchase).process()
   #return dict(form = form)
   return locals()

@auth.requires_membership('Upper Managers','Managers')
def show_inactive():
   users = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
   return dict(users=users)

@auth.requires_membership('Upper Managers','Managers')
def show_active():
   users = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
   return dict(users=users)

@auth.requires_membership('Upper Managers','Managers')
def show_all():
   users = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
   return dict(users=users)

@auth.requires_membership('Upper Managers','Managers')
def deactivate_user():
   user_id = request.args[0]
   db.auth_user.update_or_insert(db.auth_user.id == user_id , registration_key='disabled')
   return redirect(URL('show_all'))

@auth.requires_membership('Upper Managers','Managers')
def activate_user():
   user_id = request.args[0]
   db.auth_user.update_or_insert(db.auth_user.id == user_id , registration_key='')
   return redirect(URL('show_all'))
