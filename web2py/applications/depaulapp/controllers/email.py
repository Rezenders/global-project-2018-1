@auth.requires_membership('Manager')
def send_hours():
    WorkWeek_id = request.args[0]
    WeekWorked = db(db.WorkWeek.id == WorkWeek_id).select(db.WorkWeek.ALL)

    try:
        user_id = WeekWorked[0].user_id
        tracker_status = WeekWorked[0].Approved_Status

        student = db(db.auth_user.id == user_id).select(db.auth_user.ALL)

        send_to = student[0].email

        context = dict(
                name=student[0].first_name,
                start=WeekWorked[0].Monday,
                status=tracker_status,
                comments=WeekWorked[0].Manager_Comment,
                )
            
        message = response.render('send_hours.html', context)

        mail_status = mail.send(to=[send_to],
                                subject='DePaul time report',
                                message=message)
    except:
        pass
    return redirect(URL('timereporting','users',request.args[1]))
