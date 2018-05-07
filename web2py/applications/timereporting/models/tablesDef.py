db.define_table('WorkWeek', Field('Monday','date'),Field('Sunday','date'),Field('Approved_Status',requires = IS_IN_SET(['Needs Approval', 'Rejected','Approved']),default='Needs Approval'),Field('user_id','reference auth_user'),Field('Manager_Comment','string'),Field('Total_Hours','double'))

db.define_table(
    'WorkShift',
    Field('ShiftDay', 'date'),
    Field('WorkedTime', 'double'),
    Field('Description', 'string'),
    Field('WorkWeek_id','reference WorkWeek')
)
