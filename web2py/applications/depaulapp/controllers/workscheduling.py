@auth.requires_membership('Students')
def timereport():
   form = SQLFORM(db.avaliabledh).process()
   form.add_button('Check your hours', URL('depaulapp', 'workscheduling', 'show_hours_student'))
   form.add_button('Home', URL('depaulapp', 'default', 'index'))
   if form.accepted:
       response.flash = 'Hours were registered'
   elif  form.errors:
       response.flash = 'Something went wrong'
   return dict(form = form)

@auth.requires_membership('Managers')
def show_hours():
   db.avaliabledh.user_id.writable = False
   
   fields_week = [
       db.avaliabledh.start_time_on_monday,
       db.avaliabledh.end_time_on_monday,
       db.avaliabledh.user_id,
   ]

   grid = SQLFORM.smartgrid(
           db.avaliabledh,
           create = False,
           deletable = False,
           details = False,
           )
   return dict(hours=grid)

@auth.requires_membership('Students')
def show_hours_student():
   thequery = (db.avaliabledh.user_id == auth.user.id)
   db.avaliabledh.user_id.writable = False
   grid = SQLFORM.grid(
       query=thequery,
       fields=[
           db.avaliabledh.monday,
           db.avaliabledh.tuesday,
           db.avaliabledh.wednesday,
           db.avaliabledh.thursday,
           db.avaliabledh.friday,
           db.avaliabledh.end_time_on_friday,
           db.avaliabledh.total_hours_avaliable,
       ],
       create=False,
       details=False,
       )
   return dict(grid=grid)
