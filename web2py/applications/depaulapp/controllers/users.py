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
    show_all = BUTTON('Show all', _onclick='web2py_component("%s","users_table");' % URL(c='users', f='show_users.load', vars={'status':'all'}))
    show_active = BUTTON('Show active', _onclick='web2py_component("%s","users_table");' % URL(c='users', f='show_users.load', vars={'status':'active'}))
    show_disabled = BUTTON('Show disabled', _onclick='web2py_component("%s","users_table");' % URL(c='users', f='show_users.load', vars={'status':'disabled'}))
    return dict(all=show_all, active=show_active, disabled=show_disabled)

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
    if auth.has_membership(user_id=auth.user.id, role='Upper Managers'):
        links.append(dict(header="", body = lambda row: toogle_but(row)))

    user_query = True
    if request.vars.status == 'active':
        user_query = user_query & (db.auth_user.registration_key == '')
    elif request.vars.status == 'disabled':
        user_query = user_query & (db.auth_user.registration_key != '')

    grid = SQLFORM.smartgrid(
           db.auth_user,
           linked_tables = [],
           constraints = dict(auth_user=user_query),
           fields = auth_fields,
           create = False,
           editable = False,
           details = False,
           deletable = False,
           exportclasses=dict(auth_user=export_classes),
           links = links,
           )
    return dict(users=grid)

def toogle_but(row):
    if auth.has_membership(user_id=row.id, role='Students'):
        return BUTTON('Promote', _class='btn-sm btn-primary',_onclick="ajax('%s', [], ':eval')" % URL(c='users',f='toogle_role',args=[row.id]))
    elif auth.has_membership(user_id=row.id, role='Managers'):
        return BUTTON('Demote', _class='btn-sm btn-primary',_onclick="ajax('%s', [], ':eval')" % URL(c='users',f='toogle_role',args=[row.id]))
    else:
        return ''

def toogle_role():
    user_id = request.args[0]
    students_id = auth.id_group(role='Students')
    managers_id = auth.id_group(role='Managers')

    if auth.has_membership(user_id=user_id, role='Students'):
        auth.del_membership(group_id=students_id, user_id=user_id)
        auth.add_membership(group_id=managers_id, user_id=user_id)
    elif auth.has_membership(user_id=user_id, role='Managers'):
        auth.del_membership(group_id=managers_id, user_id=user_id)
        auth.add_membership(group_id=students_id, user_id=user_id)
    return 'web2py_component("%s","users_table");' % URL(c='users',f='show_users.load');

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
