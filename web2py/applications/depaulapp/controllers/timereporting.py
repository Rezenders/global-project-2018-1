from datetime import date, datetime, timedelta

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

    for idx, day in enumerate(DAYS_OF_WEEK):
        current_shift = db.WorkShift(db.WorkShift.ShiftDay == DAYS[idx])
        if current_shift:
            hours = current_shift.WorkedTime
            comment = current_shift.Description

            setattr(form.vars, day + '_Hours', int(hours) if hours.is_integer() else hours)
            setattr(form.vars, day + '_Description', comment)

    if form.process().accepted:

        total_hours = 0
        for day in DAYS_OF_WEEK:
            try:
                total_hours += float(getattr(form.vars, day + '_Hours'))
            except Exception:
                # Field was blank, no hours to add
                pass

        week = db.WorkWeek.update_or_insert(
            db.WorkWeek.Monday == DAYS[0],
            Monday=DAYS[0],
            Sunday=DAYS[6],
            user_id=auth.user.id,
            Total_Hours=total_hours)
        if week:
            weekid = week.id
        else:
            weekid = db.WorkWeek(db.WorkWeek.Monday == DAYS[0]).id

        for idx, day in enumerate(DAYS_OF_WEEK):
            curr_date = DAYS[idx]
            try:
                hours = float(getattr(form.vars, day + '_Hours'))
            except Exception:
                hours = 0
            comment = getattr(form.vars, day + '_Description')

            old_row = db.WorkShift(db.WorkShift.ShiftDay == curr_date)

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

    return dict(form=form, week_start=week_start_str, next_week=next_week_button, previous_week=previous_week_button)

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
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False                          ,tsv_with_hidden_cols=False)

    links = [dict(header="", body = lambda row: approve_but(row)), dict(header="", body= lambda row: reject_but(row))]
    grid = SQLFORM.smartgrid(
            db.WorkWeek,
            linked_tables=['WorkShift'],
            fields = dict(WorkWeek = fields_week, WorkShift = fields_shift),
            create = False,
            deletable = False,
            details = False,
            onupdate = week_update,
            editable = False,
            exportclasses=export_classes,
            links =dict(WorkWeek=links),
            )
    return dict(hours=grid)

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

