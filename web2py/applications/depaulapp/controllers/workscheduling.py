@auth.requires_membership('Students')
def timereport():
   form = SQLFORM(db.AvailableDH).process()
   form.add_button('Check your hours', URL('depaulapp', 'workscheduling', 'show_hours_student'))
   form.add_button('Home', URL('depaulapp', 'default', 'index'))
   if form.accepted:
       response.flash = 'Hours were registered'
   elif  form.errors:
       response.flash = 'Something went wrong'
   return dict(form = form)

@auth.requires_membership('Managers')
def show_hours():
   db.AvailableDH.student_name.writable = False
   
   grid = SQLFORM.smartgrid(
           db.AvailableDH,
           create = False,
           deletable = False,
           details = False,
           editable = False,
           )
   return dict(hours=grid)

@auth.requires_membership('Students')
def show_hours_student():
   thequery = (db.AvailableDH.student_name == auth.user.id)
   db.AvailableDH.student_name.writable = False
   grid = SQLFORM.grid(
       query=thequery,
#       fields=[
#           db.AvailableDH.monday,
#           db.AvailableDH.tuesday,
#           db.AvailableDH.wednesday,
#           db.AvailableDH.thursday,
#           db.AvailableDH.friday,
#           db.AvailableDH.end_time_on_friday,
#           db.AvailableDH.total_hours_avaliable,
#       ],
       create=False,
       details=False,
       )
   return dict(grid=grid)
