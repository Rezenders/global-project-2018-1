from users import _add_to_students

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
	users = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
	return dict(users=users)

@auth.requires_membership('manager')
def delete_user():
	user_id = request.args[0]	
	db(db.auth_user.studentID==user_id).delete()
	return redirect(URL('show'))
    
@auth.requires_membership('students')
def ViewHours():

    bar=db((db.WorkWeek.user_id==auth.user.id)&(db.WorkShift.WorkWeek_id==db.WorkWeek.id)).select(db.WorkShift.WorkedTime.sum())
    ts=bar.first()[db.WorkShift.WorkedTime.sum()]
    thequery=(db.WorkWeek.user_id==auth.user.id)&(db.WorkShift.WorkWeek_id==db.WorkWeek.id)
    var=SQLFORM.grid(query=thequery,fields=[db.WorkShift.ShiftDay,db.WorkShift.WorkedTime,db.WorkShift.Description,db.WorkWeek.Monday,db.WorkWeek.Sunday],create=False)
    return dict(a=var,b=ts)

@auth.requires_membership('students')
def AddHours():
    var=SQLFORM.factory(db.WorkWeek.Monday,
                        Field('Monday_Hours','double',default=0),
                        Field('Monday_Description','string'),
                        Field('Tuesday_Hours','double',default=0),
                        Field('Tuesday_Description','string'),
                        Field('Wednesday_Hours','double',default=0),
                        Field('Wednesday_Description','string'),
                        Field('Thursday_Hours','double',default=0),
                        Field('Thursday_Description','string'),
                        Field('Friday_Hours','double',default=0),
                        Field('Friday_Description','string'),
                        Field('Saturday_Hours','double',default=0),
                        Field('Saturday_Description','string'),
                        Field('Sunday_Hours','double',default=0),
                        Field('Sunday_Description','string'),
                       )
    md='Saturday';
    if var.process().accepted:
            import datetime
            #db.WorkWeek.Sunday,
            #timedelta(days=5)
            #.weekday()
            #md=var.vars.Monday+datetime.timedelta(days=5);
            md=var.vars.Monday.weekday();
            if md!=0:
                response.flash='Invalid day'
            else:
                Day1=var.vars.Monday
                Day2=var.vars.Monday+datetime.timedelta(days=1);
                Day3=var.vars.Monday+datetime.timedelta(days=2);
                Day4=var.vars.Monday+datetime.timedelta(days=3);
                Day5=var.vars.Monday+datetime.timedelta(days=4);
                Day6=var.vars.Monday+datetime.timedelta(days=5);
                Day7=var.vars.Monday+datetime.timedelta(days=6);
                TotalHours=var.vars.Monday_Hours          +var.vars.Tuesday_Hours+var.vars.Wednesday_Hours+var.vars.Thursday_Hours+var.vars.Friday_Hours+var.vars.Saturday_Hours+var.vars.Sunday_Hours;
                new_var=db.WorkWeek.insert(Monday=Day1,Sunday=Day7,user_id=auth.user.id,Total_Hours=TotalHours)
                weekid=new_var.id
                db.WorkShift.insert(ShiftDay=Day1,WorkedTime=var.vars.Monday_Hours,Description=var.vars.Monday_Description,WorkWeek_id=weekid)
                db.WorkShift.insert(ShiftDay=Day2,WorkedTime=var.vars.Tuesday_Hours,Description=var.vars.Tuesday_Description,WorkWeek_id=weekid)
                db.WorkShift.insert(ShiftDay=Day3,WorkedTime=var.vars.Wednesday_Hours,Description=var.vars.Wednesday_Description,WorkWeek_id=weekid)
                db.WorkShift.insert(ShiftDay=Day4,WorkedTime=var.vars.Thursday_Hours,Description=var.vars.Thursday_Description,WorkWeek_id=weekid)
                db.WorkShift.insert(ShiftDay=Day5,WorkedTime=var.vars.Friday_Hours,Description=var.vars.Friday_Description,WorkWeek_id=weekid)
                db.WorkShift.insert(ShiftDay=Day6,WorkedTime=var.vars.Saturday_Hours,Description=var.vars.Saturday_Description,WorkWeek_id=weekid)
                db.WorkShift.insert(ShiftDay=Day7,WorkedTime=var.vars.Sunday_Hours,Description=var.vars.Sunday_Description,WorkWeek_id=weekid)
                
                response.flash='Thanks for filling the form'
            #year, month, day = (int(x) for x in md.split('-'))
            #answer = datetime.date(year, month, day).weekday()
        # id = db.client.insert(**db.client._filter_fields(form.vars))
        #var.vars.client=id
        #id = db.address.insert(**db.address._filter_fields(form.vars))


    return dict(a=var,b=md)

@auth.requires_membership('Manager')
def ViewStudentHours():
    db.WorkWeek.Monday.writable = False
    db.WorkWeek.Sunday.writable = False
    db.WorkWeek.user_id.writable= False
    bar=db((db.WorkShift.WorkWeek_id==db.WorkWeek.id)).select(db.WorkShift.WorkedTime.sum())
    ts=bar.first()[db.WorkShift.WorkedTime.sum()]
    thequery=(db.WorkShift.WorkWeek_id==db.WorkWeek.id)&(db.auth_user.id)
    var=SQLFORM.grid(query=thequery,fields=[db.WorkShift.ShiftDay,db.WorkShift.WorkedTime,db.WorkShift.Description,db.WorkWeek.Monday,db.WorkWeek.Sunday,db.WorkWeek.Approved_Status,db.WorkWeek.Total_Hours],field_id=db.WorkWeek.id,create=False,deletable=False)
    return dict(a=var,b=ts)