# -*- coding: utf-8 -*-
# try something like
# response.flash = T(db.TimeTracker.user_id)
var=(db.TimeTracker.WorkShift_id==db.WorkShift.id)&(db.TimeTracker.user_id==db.auth_user.id);#db(db.TimeTracker.user_id == 2).select(db.TimeTracker.user_id);
# varto=db(var).select(db.auth_user.first_name,db.auth_user.last_name,db.auth_user.email,db.WorkShift.InitialTime,db.WorkShift.EndTime);
fields=[db.auth_user.email,db.auth_user.first_name,db.auth_user.last_name];

var2=SQLFORM.grid(query=var,fields=[db.TimeTracker.Approved,db.auth_user.email,db.auth_user.first_name,db.auth_user.last_name,db.WorkShift.WeekStart,db.WorkShift.Start_1,db.WorkShift.End_1,db.WorkShift.Start_2,db.WorkShift.End_2,db.WorkShift.Start_3,db.WorkShift.End_3,db.WorkShift.Start_4,db.WorkShift.End_4,db.WorkShift.Start_5,db.WorkShift.End_5,db.WorkShift.Start_6,db.WorkShift.End_6,db.WorkShift.Start_7,db.WorkShift.End_7],
               deletable=True,user_signature=True
                 );
var6=db(var).select();
var3=SQLFORM.grid(db.TimeTracker,user_signature=True);

def index(): return dict(a=var3,b=var2)