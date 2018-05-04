@auth.requires_membership('manager')
def send_hours():
    user_id = request.args[0]
    workshift_id = request.args[1]

    student = db(db.auth_user.id == user_id).select(db.auth_user.first_name)

    workshift = db(db.WorkShift.id == workshift_id).select(db.WorkShift.ALL)

    query = (
        db.TimeTracker.WorkShift_id == workshift_id) & (
        db.TimeTracker.user_id == user_id)
    tracker_status = db(query).select(db.TimeTracker.Approved)

    status = "Rejected"
    if tracker_status:
        status = "Approved"

    context = dict(
        name=student[0].first_name,
        start=workshift[0].WeekStart,
        status=status)
    message = response.render('send_hours.html', context)

    mail_status = mail.send(to=['testidlab@gmail.com'],
                            subject='DePaul time report',
                            message=message)

    return redirect(URL('timereporting', 'default', 'index'))
