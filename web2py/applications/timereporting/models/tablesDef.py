db.define_table(
    'WorkShift',
    Field('WeekStart', 'date'),
    Field('Start_1', 'time'),
    Field('End_1', 'time'),
    Field('Start_2', 'time'),
    Field('End_2', 'time'),
    Field('Start_3', 'time'),
    Field('End_3', 'time'),
    Field('Start_4', 'time'),
    Field('End_4', 'time'),
    Field('Start_5', 'time'),
    Field('End_5', 'time'),
    Field('Start_6', 'time'),
    Field('End_6', 'time'),
    Field('Start_7', 'time'),
    Field('End_7', 'time')
)

db.define_table(
    'TimeTracker',
    Field('WorkShift_id', 'reference WorkShift'),
    Field('user_id','reference auth_user'),
    Field('Approved','boolean')
)
