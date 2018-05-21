from datetime import date, datetime, timedelta

DAYS_OF_WEEK = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')

def new_time_report():
    first_day = request.vars.startdate or date.today() - timedelta(days=date.today().isoweekday() % 7)
    if isinstance(first_day, basestring):
        first_day = datetime.strptime(first_day, "%Y-%m-%d").date()
    previous_week = first_day - timedelta(days=7)
    next_week = first_day + timedelta(days=7)
    labels = {}
    for day in range(1, 8):
        labels['Start_%d' % day] = '%s Start' % DAYS_OF_WEEK[day-1]
        labels['End_%d' % day] = '%s End' % DAYS_OF_WEEK[day-1]
    form = SQLFORM(db.WorkShift, labels=labels)
    form.vars.WeekStart = first_day
    form.element('#WorkShift_WeekStart')['_readonly']=True
    form.add_button('Back',URL('default', 'index'))
    form.add_button('Next Week', URL('new_time_report', vars={'startdate': next_week}))
    form.add_button('Previous Week', URL('new_time_report', vars={'startdate': previous_week}))


    if form.process().accepted:
        # TODO: Notify manager, insert row into TimeTracker with user_id and WorkShift id
        redirect(URL(a='depaulapp','default', 'index'))
    elif form.errors:
        #form has errors
        response.flash = T('Form Errors')

    return dict(form=form)
