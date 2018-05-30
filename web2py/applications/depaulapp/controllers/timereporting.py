from datetime import date, datetime, timedelta

@auth.requires_membership('Students')
def ViewHours():
    db.WorkWeek.Monday.writable = False
    db.WorkWeek.Sunday.writable = False
    db.WorkWeek.user_id.readable = False
    db.WorkWeek.user_id.writable = False
    db.WorkWeek.id.readable=False;
    db.WorkWeek.Total_Hours.writable = False
    db.WorkWeek.Approved_Status.writable=False;
    db.WorkWeek.Manager_Comment.writable=False
    thequery = (db.WorkWeek.user_id == auth.user.id) & (db.WorkShift.WorkWeek_id == db.WorkWeek.id)
    fields_week = [
       # db.WorkWeek.user_id,
        db.WorkWeek.Monday,
        db.WorkWeek.Sunday,
        db.WorkWeek.Total_Hours,
        db.WorkWeek.Approved_Status,
        db.WorkWeek.Manager_Comment,
    ]

    fields_shift = [
        db.WorkShift.ShiftDay,
        db.WorkShift.WorkedTime,
        db.WorkShift.Description,
        db.WorkShift.Last_Changed
    ]
    export_classes = dict(csv=True, json=False, html=False, tsv=False, xml=False,csv_with_hidden_cols=False,tsv_with_hidden_cols=False)

    links = [
            dict(header="Mo", body = lambda row: monday_hour(row)),
            dict(header="Tu", body = lambda row: tuesday_hour(row)),
            dict(header="We", body = lambda row: wednesday_hour(row)),
            dict(header="Th", body = lambda row: thursday_hour(row)),
            dict(header="Fr", body = lambda row: friday_hour(row)),
            dict(header="Sa", body = lambda row: saturday_hour(row)),
            dict(header="Su", body = lambda row: sunday_hour(row)),
        #    dict(header="", body = lambda row: detail_but(row)),
            ]
    links2 =[dict(header="", body = lambda row: edit_but(row))]
    DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    first_day = request.vars.startdate or date.today() - timedelta(days=date.today().weekday())
    if isinstance(first_day, basestring):
        first_day = datetime.strptime(first_day, '%Y-%m-%d').date()

    # Check to make sure start date is a monday
    if first_day.weekday() != 0:
        first_day = date.today() - timedelta(days=date.today().weekday())
    week_start_str = 'Week of %s' % first_day.strftime('%m/%d')
    previous_week = first_day - timedelta(days=7)
    next_week = first_day + timedelta(days=7)

    Week_constraint=(db.WorkWeek.user_id == auth.user.id)&(db.WorkWeek.Monday==first_day)
    grid = SQLFORM.smartgrid(
            db.WorkWeek,
            linked_tables=['WorkShift'],
            constraints=dict(WorkWeek=Week_constraint),
            fields = dict(WorkWeek = fields_week, WorkShift = fields_shift),
            create = False,
            deletable = False,
            details = False,
            editable = False,
            exportclasses=dict(WorkWeek=export_classes,WorkShift=export_classes),
            links =dict(WorkWeek=links,WorkShift=links2),
            )
    previous_week_button = INPUT(_type='button', _value='Previous Week', _onclick='window.location=\'%s\';;return false' % URL('ViewHours', vars={'startdate': previous_week}))
    next_week_button = INPUT(_type='button', _value='Next Week', _onclick='window.location=\'%s\';;return false' % URL('ViewHours', vars={'startdate': next_week}))

    return dict(grid=grid, week_start=week_start_str, next_week=next_week_button, previous_week=previous_week_button)

def edit_but(row):
    workshift = db(db.WorkShift.id == row.id).select(db.WorkShift.ALL).first()
    week = db(db.WorkWeek.id == workshift.WorkWeek_id).select(db.WorkWeek.ALL).first()
    ret = ""
    if week.Approved_Status != 'Approved':
        ret = A('Edit',_class='button btn btn-sm btn-default',_href=URL(c="timereporting",f="edit_view_hours", args=[row.id]))
    return ret

@auth.requires_login()
def edit_view_hours():
    ws_id = request.args[0]
    ws = db(db.WorkShift.id == ws_id).select(db.WorkShift.WorkWeek_id)

    tws=db(db.WorkShift.id == ws_id)
    tws.update(Last_Changed=request.now)
    week = db(db.WorkWeek.id == ws[0].WorkWeek_id).select(db.WorkWeek.ALL).first()
    if auth.user.id == week.user_id:
        db.WorkShift.id.writable = False
        db.WorkShift.id.readable = False
        db.WorkShift.WorkWeek_id.writable = False
        db.WorkShift.WorkWeek_id.readable = False

        form = SQLFORM(db.WorkShift, ws_id)
        if form.process().accepted:

            redirect(URL(c="timereporting",f="ViewHours/WorkWeek/WorkShift.WorkWeek_id",args=[week.id]))
        return dict(form=form)
    else:
        return redirect(URL(c="timereporting",f="ViewHours/WorkWeek/WorkShift.WorkWeek_id"))

@auth.requires_membership('Students')
def AddHours():
    DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    first_day = request.vars.startdate or date.today() - timedelta(days=date.today().weekday())
    if isinstance(first_day, basestring):
        first_day = datetime.strptime(first_day, '%Y-%m-%d').date()

    # Check to make sure start date is a monday
    if first_day.weekday() != 0:
        first_day = date.today() - timedelta(days=date.today().weekday())
    week_start_str = 'Week of %s' % first_day.strftime('%m/%d')
    previous_week = first_day - timedelta(days=7)
    next_week = first_day + timedelta(days=7)

    labels = {}
    for idx, day in enumerate(DAYS_OF_WEEK):
        day_idx = day + '_Hours'
        date_string = (first_day + timedelta(days=idx)).strftime('%m/%d')
        labels[day_idx] = '%s - %s' % (day[:3], date_string)

    form = SQLFORM.factory(
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
                          labels=labels
    )

    previous_week_button = INPUT(_type='button', _value='Previous Week', _onclick='window.location=\'%s\';;return false' % URL('AddHours', vars={'startdate': previous_week}))
    next_week_button = INPUT(_type='button', _value='Next Week', _onclick='window.location=\'%s\';;return false' % URL('AddHours', vars={'startdate': next_week}))

    DAYS = [first_day + timedelta(days=n) for n in range(7)]

    existing_week = db(
            (db.WorkWeek.user_id == auth.user.id) &
            (db.WorkWeek.Monday == DAYS[0])
    ).select().first()

    if existing_week:
        for idx, day in enumerate(DAYS_OF_WEEK):
            current_shift = db(
                (db.WorkShift.ShiftDay == DAYS[idx]) &
                (db.WorkShift.WorkWeek_id == existing_week.id)
            ).select().first()
            if current_shift:
                hours = current_shift.WorkedTime
                comment = current_shift.Description

                setattr(form.vars, day + '_Hours', int(hours) if hours.is_integer() else hours)
                setattr(form.vars, day + '_Description', comment)

    if form.process().accepted:

        total_hours = 0
        for day in DAYS_OF_WEEK:
            try:
                hours = float(getattr(form.vars, day + '_Hours'))
                total_hours += hours if hours > 0 else 0
            except Exception:
                # Field was blank, no hours to add
                pass

        if total_hours > 0 or existing_week is not None:
            week = db.WorkWeek.update_or_insert(
                (db.WorkWeek.Monday == DAYS[0]) & (db.WorkWeek.user_id == auth.user.id),
                Monday=DAYS[0],
                Sunday=DAYS[6],
                user_id=auth.user.id,
                Total_Hours=total_hours)
            if week:
                weekid = week.id
            else:
                weekid = existing_week.id

            for idx, day in enumerate(DAYS_OF_WEEK):
                curr_date = DAYS[idx]
                try:
                    hours = float(getattr(form.vars, day + '_Hours'))
                    if hours < 0:
                        hours = 0
                except Exception:
                    hours = 0
                comment = getattr(form.vars, day + '_Description')

                old_row = db(
                    (db.WorkShift.ShiftDay == curr_date) &
                    (db.WorkShift.WorkWeek_id == weekid)
                ).select().first()

                if old_row:
                    old_hours = old_row.WorkedTime
                    old_comment = old_row.Description

                    if old_hours != hours or old_comment != comment:
                        old_row.update_record(
                            WorkedTime=hours,
                            Description=comment,
                            Last_Changed=datetime.now())

                else:
                    db.WorkShift.insert(
                        ShiftDay=curr_date,
                        WorkedTime=hours,
                        Description=comment,
                        WorkWeek_id=weekid,
                        Last_Changed=datetime.now())

            redirect(URL(c="timereporting",f="ViewHours"))
        
        else:
            response.flash = T('No Hours Entered!')

    return dict(form=form, week_start=week_start_str, next_week=next_week_button, previous_week=previous_week_button)

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def ViewStudentHours():
    return dict()

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def StudentHours():
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
        db.WorkWeek.Manager_Comment,
    ]

    fields_shift = [
        db.WorkShift.ShiftDay,
        db.WorkShift.WorkedTime,
        db.WorkShift.Description,
    ]
    export_classes = dict(csv=True, json=False, html=False, tsv=False, xml=False,csv_with_hidden_cols=False,tsv_with_hidden_cols=False)

    links = [
            dict(header="Mo", body = lambda row: monday_hour(row)),
            dict(header="Tu", body = lambda row: tuesday_hour(row)),
            dict(header="We", body = lambda row: wednesday_hour(row)),
            dict(header="Th", body = lambda row: thursday_hour(row)),
            dict(header="Fr", body = lambda row: friday_hour(row)),
            dict(header="Sa", body = lambda row: saturday_hour(row)),
            dict(header="Su", body = lambda row: sunday_hour(row)),
            dict(header="Send Email", body = lambda row: email_but(row)),
            dict(header="Add Comments", body = lambda row: comments_but(row)),
            dict(header="", body = lambda row: approve_but(row)), 
            dict(header="", body= lambda row: reject_but(row)),
            ]

    first_day = request.vars.startdate or date.today() - timedelta(days=date.today().weekday())
    if isinstance(first_day, basestring):
        first_day = datetime.strptime(first_day, '%Y-%m-%d').date()

    # Check to make sure start date is a monday
    if first_day.weekday() != 0:
        first_day = date.today() - timedelta(days=date.today().weekday())
    week_start_str = 'Week of %s' % first_day.strftime('%m/%d')
    previous_week = first_day - timedelta(days=7)
    next_week = first_day + timedelta(days=7)

    Week_constraint=(db.WorkWeek.Monday==first_day)

    grid = SQLFORM.smartgrid(
            db.WorkWeek,
            linked_tables=['WorkShift'],
            fields = dict(WorkWeek = fields_week, WorkShift = fields_shift),
            create = False,
            deletable = False,
            details = False,
            editable = False,
            exportclasses=dict(WorkWeek=export_classes),
            links =dict(WorkWeek=links),
            constraints=dict(WorkWeek=Week_constraint),
            )
    previous_week_button = INPUT(_type='button', _value='Previous Week', _onclick='web2py_component("%s","hourform");' % URL(c='timereporting', f='StudentHours.load', vars={'startdate':previous_week}))
    next_week_button = INPUT(_type='button', _value='Next Week', _onclick='web2py_component("%s","hourform");' % URL(c='timereporting', f='StudentHours.load', vars={'startdate':next_week}))

    return dict(hours=grid, week_start=week_start_str, next_week=next_week_button, previous_week=previous_week_button)

def email_but(row):
    return BUTTON(IMG(_src=URL('static','images/email.png')),_onclick="jQuery.ajax('"+URL('email','send_hours', args=[row.id])+"');",_class='logos')

def comments_but(row):
    return BUTTON(IMG(_src=URL('static','images/comment.png')), _onclick="show_modal("+str(row.id)+")",_class='logos')

@auth.requires(auth.has_membership('Managers') or auth.has_membership('Upper Managers'))
def add_comments():
    week_id = long(request.args[0])
    text = request.args[1].replace("_", " ")
    week = db(db.WorkWeek.id == long(week_id)).select().first()
    week.update_record(Manager_Comment=text)
    
    return 'web2py_component("%s","hourform");' % URL(c='timereporting', f='StudentHours.load')

def approve_but(row):
    week = db(db.WorkWeek.id == row.id).select(db.WorkWeek.ALL).first()
    ret_aux = ''
    if week.Approved_Status == 'Approved':
        ret_aux = 'active'

    return BUTTON('Approve',_name=week.id,_class='button btn btn-sm btn-success ' + ret_aux, _onclick="ajax('%s',[],':eval')" % URL(c='timereporting', f='approve', args=[week.id]))

def approve():
    week_id = request.args[0]
    week = db(db.WorkWeek.id == week_id).select().first()

    new_status = 'Approved'
    if week.Approved_Status == 'Approved':
        new_status = 'Needs Approval'

    week.update_record(Approved_Status=new_status)

    return 'web2py_component("%s","hourform");' % URL(c='timereporting', f='StudentHours.load')

def reject_but(row):
    week = db(db.WorkWeek.id == row.id).select(db.WorkWeek.ALL).first()
    ret_aux = ''
    if week.Approved_Status == 'Rejected':
        ret_aux = 'active'

    return BUTTON('Reject',_class='button btn btn-sm btn-danger ' + ret_aux, _onclick="ajax('%s',[],':eval')"%URL(c='timereporting', f='reject', args=[week.id]))

def reject():
    week_id = request.args[0]
    week = db(db.WorkWeek.id == week_id).select().first()

    new_status = 'Rejected'
    if week.Approved_Status == 'Rejected':
        new_status = 'Needs Approval'

    week.update_record(Approved_Status=new_status)

    return 'web2py_component("%s","hourform");' % URL(c='timereporting', f='StudentHours.load')

def monday_hour(row):
    ws = db(db.WorkShift.WorkWeek_id == row.id).select(orderby=db.WorkShift.ShiftDay)
    time = 0
    for w in ws:
        if w.ShiftDay.weekday() == 0:
            time = w.WorkedTime
            break
    return time

def tuesday_hour(row):
    ws = db(db.WorkShift.WorkWeek_id == row.id).select(orderby=db.WorkShift.ShiftDay)
    time = 0
    for w in ws:
        if w.ShiftDay.weekday() == 1:
            time = w.WorkedTime
            break
    return time

def wednesday_hour(row):
    ws = db(db.WorkShift.WorkWeek_id == row.id).select(orderby=db.WorkShift.ShiftDay)
    time = 0
    for w in ws:
        if w.ShiftDay.weekday() == 2:
            time = w.WorkedTime
            break
    return time

def thursday_hour(row):
    ws = db(db.WorkShift.WorkWeek_id == row.id).select(orderby=db.WorkShift.ShiftDay)
    time = 0
    for w in ws:
        if w.ShiftDay.weekday() == 3:
            time = w.WorkedTime
            break
    return time

def friday_hour(row):
    ws = db(db.WorkShift.WorkWeek_id == row.id).select(orderby=db.WorkShift.ShiftDay)
    time = 0
    for w in ws:
        if w.ShiftDay.weekday() == 4:
            time = w.WorkedTime
            break
    return time

def saturday_hour(row):
    ws = db(db.WorkShift.WorkWeek_id == row.id).select(orderby=db.WorkShift.ShiftDay)
    time = 0
    for w in ws:
        if w.ShiftDay.weekday() == 5:
            time = w.WorkedTime
            break
    return time

def sunday_hour(row):
    ws = db(db.WorkShift.WorkWeek_id == row.id).select(orderby=db.WorkShift.ShiftDay)
    time = 0
    for w in ws:
        if w.ShiftDay.weekday() == 6:
            time = w.WorkedTime
            break
    return time


