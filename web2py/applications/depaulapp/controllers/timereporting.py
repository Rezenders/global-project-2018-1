@auth.requires_membership('Students')
def ViewHours():
    thequery = (db.WorkWeek.user_id == auth.user.id) & (
        db.WorkShift.WorkWeek_id == db.WorkWeek.id)
    links = [dict(header="", body = lambda row: edit_but(row))]
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)
    grid = SQLFORM.grid(
        query=thequery,
        fields=[
            db.WorkShift.ShiftDay,
            db.WorkShift.WorkedTime,
            db.WorkShift.Description,
            db.WorkShift.Last_Changed,
            db.WorkWeek.Monday,
            db.WorkWeek.Sunday],
        create = False,
        details = False,
        editable = False,
        links = links,
        exportclasses=export_classes
        )
    return dict(grid=grid)

def edit_but(row):
    workshift = db(db.WorkShift.id == row.WorkShift.id).select(db.WorkShift.WorkWeek_id)
    week = db(db.WorkWeek.id == workshift[0].WorkWeek_id).select(db.WorkWeek.Approved_Status)
    ret = ""
    if week[0].Approved_Status != 'Approved':
        ret = A('Edit',_class='button btn btn-sm btn-default',_href=URL(c="timereporting",f="edit_view_hours", args=[row.WorkShift.id]))
    return ret

@auth.requires_login()
def edit_view_hours():
    ws_id = request.args[0]
    ws = db(db.WorkShift.id == ws_id).select(db.WorkShift.WorkWeek_id)
    tws=db(db.WorkShift.id == ws_id)
    tws.update(Last_Changed=request.now)
    week = db(db.WorkWeek.id == ws[0].WorkWeek_id).select(db.WorkWeek.user_id)
    if auth.user.id == week[0].user_id:
        db.WorkShift.id.writable = False
        db.WorkShift.id.readable = False
        db.WorkShift.WorkWeek_id.writable = False
        db.WorkShift.WorkWeek_id.readable = False

        form = SQLFORM(db.WorkShift, ws_id)
        if form.process().accepted:

            redirect(URL(c="timereporting",f="ViewHours"))
        return dict(form=form)
    else:
        return redirect(URL(c="timereporting",f="ViewHours"))

@auth.requires_membership('Students')
def AddHours():
    var = SQLFORM.factory(db.WorkWeek.Monday,
                          Field('Monday_Hours', 'double', default=0),
                          Field('Monday_Description', 'string'),
                          Field('Tuesday_Hours', 'double', default=0),
                          Field('Tuesday_Description', 'string'),
                          Field('Wednesday_Hours', 'double', default=0),
                          Field('Wednesday_Description', 'string'),
                          Field('Thursday_Hours', 'double', default=0),
                          Field('Thursday_Description', 'string'),
                          Field('Friday_Hours', 'double', default=0),
                          Field('Friday_Description', 'string'),
                          Field('Saturday_Hours', 'double', default=0),
                          Field('Saturday_Description', 'string'),
                          Field('Sunday_Hours', 'double', default=0),
                          Field('Sunday_Description', 'string'),
                          )
    md = 'Saturday'
    if var.process().accepted:
        import datetime
        # db.WorkWeek.Sunday,
        # timedelta(days=5)
        # .weekday()
        # md=var.vars.Monday+datetime.timedelta(days=5);
        md = var.vars.Monday.weekday()
        if md != 0:
            response.flash = 'Invalid day'
        else:
            Day1 = var.vars.Monday
            Day2 = var.vars.Monday + datetime.timedelta(days=1)
            Day3 = var.vars.Monday + datetime.timedelta(days=2)
            Day4 = var.vars.Monday + datetime.timedelta(days=3)
            Day5 = var.vars.Monday + datetime.timedelta(days=4)
            Day6 = var.vars.Monday + datetime.timedelta(days=5)
            Day7 = var.vars.Monday + datetime.timedelta(days=6)
            TotalHours = var.vars.Monday_Hours + var.vars.Tuesday_Hours + var.vars.Wednesday_Hours + \
                var.vars.Thursday_Hours + var.vars.Friday_Hours + var.vars.Saturday_Hours + var.vars.Sunday_Hours
            new_var = db.WorkWeek.insert(
                Monday=Day1,
                Sunday=Day7,
                user_id=auth.user.id,
                Total_Hours=TotalHours)
            weekid = new_var.id
            db.WorkShift.insert(
                ShiftDay=Day1,
                WorkedTime=var.vars.Monday_Hours,
                Description=var.vars.Monday_Description,
                WorkWeek_id=weekid)
            db.WorkShift.insert(
                ShiftDay=Day2,
                WorkedTime=var.vars.Tuesday_Hours,
                Description=var.vars.Tuesday_Description,
                WorkWeek_id=weekid)
            db.WorkShift.insert(
                ShiftDay=Day3,
                WorkedTime=var.vars.Wednesday_Hours,
                Description=var.vars.Wednesday_Description,
                WorkWeek_id=weekid)
            db.WorkShift.insert(
                ShiftDay=Day4,
                WorkedTime=var.vars.Thursday_Hours,
                Description=var.vars.Thursday_Description,
                WorkWeek_id=weekid)
            db.WorkShift.insert(
                ShiftDay=Day5,
                WorkedTime=var.vars.Friday_Hours,
                Description=var.vars.Friday_Description,
                WorkWeek_id=weekid)
            db.WorkShift.insert(
                ShiftDay=Day6,
                WorkedTime=var.vars.Saturday_Hours,
                Description=var.vars.Saturday_Description,
                WorkWeek_id=weekid)
            db.WorkShift.insert(
                ShiftDay=Day7,
                WorkedTime=var.vars.Sunday_Hours,
                Description=var.vars.Sunday_Description,
                WorkWeek_id=weekid)

            response.flash = 'Thanks for filling the form'
        #year, month, day = (int(x) for x in md.split('-'))
        #answer = datetime.date(year, month, day).weekday()
    # id = db.client.insert(**db.client._filter_fields(form.vars))
    # var.vars.client=id
    #id = db.address.insert(**db.address._filter_fields(form.vars))

    return dict(a=var, b=md)

@auth.requires_membership('Managers')
def ViewStudentHours():
    def week_update(form):
        week_id = form.vars.id
        return redirect(URL(c='email',f='send_hours', args=[ str(week_id), 'ViewStudentHours']))

    db.WorkWeek.Monday.writable = False
    db.WorkWeek.Sunday.writable = False
    db.WorkWeek.user_id.writable = False
    db.WorkWeek.Total_Hours.writable = False

    fields_week = [
        db.WorkWeek.user_id,
        db.WorkWeek.Monday,
        db.WorkWeek.Sunday,
        db.WorkWeek.Total_Hours,
        db.WorkWeek.Approved_Status,
    ]

    fields_shift = [
        db.WorkShift.ShiftDay,
        db.WorkShift.WorkedTime,
        db.WorkShift.Description,
    ]
    export_classes = dict(csv=True, json=False, html=False, tsv=False, xml=False, 
                            csv_with_hidden_cols=False,tsv_with_hidden_cols=False)

    links = [dict(header="", body = lambda row: add_comments(row)),dict(header="", body = lambda row: approve_but(row)), dict(header="", body= lambda row: reject_but(row))]
    grid = SQLFORM.smartgrid(
            db.WorkWeek,
            linked_tables=['WorkShift'],
            fields = dict(WorkWeek = fields_week, WorkShift = fields_shift),
            create = False,
            deletable = False,
            details = False,
            onupdate = week_update,
            editable = False,
            exportclasses=dict(WorkWeek=export_classes),
            links =dict(WorkWeek=links),
            )
    return dict(hours=grid)

def add_comments(row):
    return A('Add Comments',_class='btn btn-info btn-sm')

def approve_but(row):
    week = db(db.WorkWeek.id == row.id).select(db.WorkWeek.ALL).first()
    ret_aux = ''
    if week.Approved_Status == 'Approved':
        ret_aux = 'active'

    return A('Approve',_class='button btn btn-sm btn-success ' + ret_aux, _href=URL(c='timereporting', f='approve', args=[week.id]))

def approve():
    week_id = request.args[0]
    week = db(db.WorkWeek.id == week_id).select().first()

    new_status = 'Approved'
    if week.Approved_Status == 'Approved':
        new_status = 'Needs Approval'

    week.update_record(Approved_Status=new_status)

    return redirect(URL(c='timereporting', f='ViewStudentHours'))

def reject_but(row):
    week = db(db.WorkWeek.id == row.id).select(db.WorkWeek.ALL).first()
    ret_aux = ''
    if week.Approved_Status == 'Rejected':
        ret_aux = 'active'

    return A('Reject',_class='button btn btn-sm btn-danger ' + ret_aux, _href=URL(c='timereporting', f='reject', args=[week.id]))

def reject():
    week_id = request.args[0]
    week = db(db.WorkWeek.id == week_id).select().first()

    new_status = 'Rejected'
    if week.Approved_Status == 'Rejected':
        new_status = 'Needs Approval'

    week.update_record(Approved_Status=new_status)

    return redirect(URL(c='timereporting', f='ViewStudentHours'))

