@auth.requires_membership('manager')
def send_hours():
    WorkWeek_id = request.args[0]
    WeekWorked = db(db.WorkWeek.id == WorkWeek_id).select(db.WorkWeek.ALL)

    try:
        user_id = WeekWorked[0].user_id
        #workshift_id = tracker[0].WorkShift_id
        tracker_status = WorkWeek[0].Approved_Status

        student = db(db.auth_user.id == user_id).select(db.auth_user.ALL)
        #workshift = db(db.WorkShift.id == workshift_id).select(db.WorkShift.ALL)

        send_to = student[0].email

        status = "Rejected"
        if tracker_status:
            status = "Approved"

        context = dict(
                name=student[0].first_name,
                start=WorkWeek[0].Monday,
                status=status)
            
        message = response.render('send_hours.html', context)

        mail_status = mail.send(to=[send_to],
                                subject='DePaul time report',
                                message=message)
    except:
        pass

    return redirect(URL('timereporting', 'default', 'index'))
