db.define_table('WorkWeek', Field('Monday','date'),Field('Sunday','date'),Field('Approved_Status',requires = IS_IN_SET(['Needs Approval', 'Rejected','Approved']),default='Needs Approval'),Field('user_id','reference auth_user'),Field('Manager_Comment','string'),Field('Total_Hours','double'))

db.define_table(
    'WorkShift',
    Field('ShiftDay', 'date'),
    Field('WorkedTime', 'double'),
    Field('Description', 'string'),
    Field('WorkWeek_id','reference WorkWeek'),
    Field('Last_Changed', 'datetime', default=request.now)
)

db.define_table('avaliabledh', Field('user_id','reference auth_user', default=auth.user_id, writable=False), Field('monday', 'date', requires = IS_DATE(format=('%Y-%m-%d'))), Field('start_time_on_monday', 'time', requires = IS_DATE(format=('%H:%M:%S'))), Field('end_time_on_monday', 'time', requires = IS_DATE(format=('%H:%M:%S'))), Field('tuesday', 'date', requires = IS_DATE(format=('%Y-%m-%d'))), Field('start_time_on_tuesday', 'time', requires = IS_DATE(format=('%H:%M:%S'))), Field('end_time_on_tuesday', 'time', requires = IS_DATE(format=('%H:%M:%S'))), Field('wednesday', 'date', requires = IS_DATE(format=('%Y-%m-%d'))), Field('start_time_on_wednesday', 'time', requires = IS_DATE(format=('%H:%M:%S'))), Field('end_time_on_wednesday', 'time', requires = IS_DATE(format=('%H:%M:%S'))), Field('thursday', 'date', requires = IS_DATE(format=('%Y-%m-%d'))),Field('start_time_on_thursday', 'time', requires = IS_DATE(format=('%H:%M:%S'))), Field('end_time_on_thursday', 'time', requires = IS_DATE(format=('%H:%M:%S'))), Field('friday', 'date', requires = IS_DATE(format=('%Y-%m-%d'))), Field('start_time_on_friday', 'time', requires = IS_DATE(format=('%H:%M:%S'))), Field('end_time_on_friday', 'time', requires = IS_DATE(format=('%H:%M:%S')))
