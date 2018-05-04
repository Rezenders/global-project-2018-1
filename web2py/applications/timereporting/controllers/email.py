@auth.requires_membership('manager')
def send_hours():
    tracker_id = request.args[0]
    tracker = db(db.TimeTracker.id == tracker_id).select(db.TimeTracker.ALL)

    try:
        user_id = tracker[0].user_id
        workshift_id = tracker[0].WorkShift_id
        tracker_status = tracker[0].Approved

        student = db(db.auth_user.id == user_id).select(db.auth_user.ALL)
        workshift = db(db.WorkShift.id == workshift_id).select(db.WorkShift.ALL)

        send_to = student[0].email

        status = "Rejected"
        if tracker_status:
            status = "Approved"

        context = dict(
                name=student[0].first_name,
                start=workshift[0].WeekStart,
                status=status)
            
        message = response.render('send_hours.html', context)

        mail_status = mail.send(to=[send_to],
                                subject='DePaul time report',
                                message=message)
    except:
        pass

    return redirect(URL('timereporting', 'default', 'index'))
