from users import _add_to_students

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
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

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def manage_level():
   grid = SQLFORM.smartgrid(db.auth_membership)
   return locals()

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def manage_users():
   grid = SQLFORM.smartgrid(db.auth_user)
   #db.auth_user.show_if = (db.auth_membership.group_id=='Student')
   #form = SQLFORM(db.purchase).process()
   #return dict(form = form)
   return locals()

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def show_inactive():
   users = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
   return dict(users=users)

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def show_active():
   users = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
   return dict(users=users)

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def show_all():
    return dict()

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def show_users():

    export_classes = dict(csv=True, json=False, html=False, tsv=False, xml=False,csv_with_hidden_cols=False,tsv_with_hidden_cols=False)
    
    auth_fields = [
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email,
        db.auth_user.Phone_Number,
    ]

    links = [
        dict(header="Role", body = lambda row: role(row)),    
        dict(header="", body = lambda row: activate_but(row)),    
        dict(header="", body = lambda row: deactivate_but(row)),    
    ]

    grid = SQLFORM.smartgrid(
           db.auth_user,
           linked_tables =[],
           fields = dict(auth_user=auth_fields),
           create = False,
           editable = False,
           details = False,
           deletable = False,
           exportclasses=dict(auth_user=export_classes),
           links = links,
           )
    return dict(users=grid)

def role(row):
    user = db(db.auth_user.id == row.id).select().first()
    ret =''
    if auth.has_membership(user_id=user.id, role='Students'):
        ret = 'Student'
    elif auth.has_membership(user_id=user.id, role='Managers'):
        ret = 'Manager'
    elif auth.has_membership(user_id=user.id, role='Upper Managers'):
        ret = 'Upper Manager'
    return ret

def deactivate_but(row):
    user = db(db.auth_user.id == row.id).select().first()
    upper_manager  = auth.has_membership(user_id=auth.user.id, role='Upper Managers')
    if user.registration_key =='' and not auth.has_membership(user_id=user.id, role='Upper Managers'):
        if auth.has_membership(user_id=user.id, role='Managers') and not upper_manager:
            return ""
        return BUTTON('Deactivate', _class='btn-sm btn-danger',_onclick="ajax('%s', [], ':eval')" % URL(c='users',f='deactivate_user',args=[user.id]))
    else:
        return ""

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def deactivate_user():
   user_id = request.args[0]
   db.auth_user.update_or_insert(db.auth_user.id == user_id , registration_key='disabled')
   return 'web2py_component("%s","users_table");' % URL(c='users',f='show_users.load'); 

def activate_but(row):
    user = db(db.auth_user.id == row.id).select().first()
    if user.registration_key !='' and not auth.has_membership(user_id=user.id, role='Upper Managers'):
        return BUTTON('Activate', _class='btn-sm btn-success',_onclick="ajax('%s', [], ':eval')" % URL(c='users',f='activate_user',args=[user.id]))
    else:
        return ""

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def activate_user():
   user_id = request.args[0]
   db.auth_user.update_or_insert(db.auth_user.id == user_id , registration_key='')
   return 'web2py_component("%s","users_table");' % URL(c='users',f='show_users.load');
