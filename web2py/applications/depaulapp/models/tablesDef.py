db.define_table(
        'WorkWeek',
        Field('Monday','date'),
        Field('Sunday','date'),
        Field('Approved_Status',requires = IS_IN_SET(['Needs Approval', 'Rejected','Approved']),default='Needs Approval'),
        Field('user_id','reference auth_user'),
        Field('Manager_Comment','string'),
        Field('Total_Hours','double'))

db.define_table(
    'WorkShift',
    Field('ShiftDay', 'date'),
    Field('WorkedTime', 'double'),
    Field('Description', 'string'),
    Field('WorkWeek_id','reference WorkWeek'),
    Field('Last_Changed', 'datetime', default=request.now)
)
db.define_table(
        'AvailableDH', 
        Field('student_name','reference auth_user', writable=False, default=auth.user_id), 
        Field('Monday', 'date'), 
        Field('StartTimeMonday', 'time'), 
        Field('EndTimeMonday', 'time'), 
        Field('Tuesday', 'date'), 
        Field('StartTimeTuesday', 'time'), 
        Field('EndTimeTuesday', 'time'),
        Field('Wednesday', 'date'), 
        Field('StartTimeWednesday', 'time'), 
        Field('EndTimeWednesday', 'time'), 
        Field('Thursday', 'date'),
        Field('StartTimeThursday', 'time'), 
        Field('EndTimeThursday', 'time'), 
        Field('Friday', 'date'), 
        Field('StartTimeFriday', 'time'), 
        Field('EndTimeFriday', 'time'), 
        Field('TotalHoursAvaliable', requires = IS_NOT_EMPTY())
)
