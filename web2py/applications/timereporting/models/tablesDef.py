db.define_table('WorkShift', Field('InitialTime', 'datetime'),Field('EndTime', 'datetime'))
db.define_table('TimeTracker', Field('WorkShift_id', 'reference WorkShift'),Field('user_id','reference auth_user'),Field('Approved','boolean'))
