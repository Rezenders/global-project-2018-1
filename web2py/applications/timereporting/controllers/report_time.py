from datetime import date, datetime, timedelta

DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def new_time_report():
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
        date_string = (first_day + timedelta(days=idx)).strftime('%m/%d')
        labels[day] = '%s - %s' % (day, date_string)

    current_record = db.WorkShift(db.WorkShift.WeekStart == first_day.strftime('%Y-%m-%d'))
    fields = DAYS_OF_WEEK.append('Comments')
    form = SQLFORM(
                db.WorkShift,
                record=current_record,
                labels=labels,
                showid=False,
                fields=fields
                )
    form.vars.WeekStart = first_day
    form.add_button('Back',URL('default', 'index'))
    form.add_button('Previous Week', URL('new_time_report', vars={'startdate': previous_week}))
    form.add_button('Next Week', URL('new_time_report', vars={'startdate': next_week}))


    if form.process().accepted:
        # TODO: Notify manager, insert row into TimeTracker with user_id and WorkShift id
        response.flash = T('Hours Submitted Successfully!')
    elif form.errors:
        #form has errors
        response.flash = T('Form Errors')

    return dict(form=form)
