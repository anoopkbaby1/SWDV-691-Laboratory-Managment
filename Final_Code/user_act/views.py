from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.cache import never_cache

import MySQLdb as mdb

import hashlib
import datetime
import dateutil.parser

from random import randint

db = mdb.connect('localhost','root','','lab_management')
cur = db.cursor()

@never_cache
def load_home(request): #load dashboard for the user
	if "user" in request.session:
		return render(request,'user_home.html',{'text':request.session["user"]})
	else:
		return redirect('/')
@never_cache
def go_home(request): #goto home of the user
	#k = request.session['user']
	try:
		del request.session['user']
		return redirect('/')
	except:
		return redirect("/user/")
@never_cache
def book(request): #book a test form rendering
	if "user" not in request.session:
		return redirect('/')
	patients = []
	lt = []
	city = []
    

    
	try:
		ID = request.session["user"]
		cur.execute("select ID from patient where ID=%s",(ID,));
		patients = cur.fetchall()
	except:
		db.rollback()
		return render(request,'user_home.html',{'ERROR':'UNEXPECTED ERROR001'})
	db.rollback()

	try:
		cur.execute("select ID from lab_test"); #select a lab ID
		lt = cur.fetchall()
	except:
		db.rollback()
		return render(request,'user_home.html',{'ERROR':'UNEXPECTED ERROR002'})
	db.rollback()

	try:
		cur.execute("select ID from tests"); #select a lab ID
		tt = cur.fetchall()
	except:
		db.rollback()
		return render(request,'user_home.html',{'ERROR':'UNEXPECTED ERROR003'})
	db.rollback()

	try:
		cur.execute("select ID from pathologist"); #select a lab ID
		ptt = cur.fetchall()
	except:
		db.rollback()
		return render(request,'user_home.html',{'ERROR':'UNEXPECTED ERROR004'})
	db.rollback()
    



	mini = datetime.datetime.now()
	max_date = (mini + datetime.timedelta(days=7)).strftime("%Y-%m-%d") #get max time for which leave can be applied
	min_date = mini.strftime("%Y-%m-%d")

	try:
		return render(request,'book_test.html',{'ptts':ptt, 'tts':tt, 'lts':lt,'pat':patients,'city':city,'min':min_date,'max':max_date})
	except:
		return redirect('/user/')

@never_cache
def book_submit(request): # submit form entries for validation and and then insert into database
	if request.method!="POST":
		return redirect('/user/')
	if "user" not in request.session:
		return redirect('/')
	try:
		ltid = request.POST['lt']
		pat = request.POST['pati']
        
		ag = request.POST['ptt']
		ndate = request.POST['ndate']
	except:
		return redirect('/user/')
	uid = request.session['user']
	rand_day = randint(1,5)
	nk = ndate + " 03:30:30"
	nstamp = dateutil.parser.parse(nk)
	aux_date = nstamp + datetime.timedelta(days=rand_day)
	cdate = datetime.datetime.now()
	mdate = cdate + datetime.timedelta(days=7)
	val_date = mdate.strftime("%Y-%m-%d")
	curr_date = cdate.strftime("%Y-%m-%d")
	due_date = aux_date.strftime("%Y-%m-%d")
	reg_date = nstamp.strftime("%Y-%m-%d")
	if reg_date < curr_date or reg_date > val_date: #check date validations for booking test
		return render(request,'user_home.html',{'ERROR':'REG. DATE MUST BE WITHIN 7 DAYS FROM NOW'})
	try:
		cur.execute("select cost from lab_test where ID=%s",(ltid,))
	except Exception as e:
		db.rollback()
		return render(request,'user_home.html',{'ERROR':str(e)})
	db.rollback()
	cost = cur.fetchall()[0][0]
	int(cost)
	
	try:
		cur.execute('insert into reg_tests values(0,%s,%s,%s,%s,%s,%s,%s,0,"NO")',
			(ltid,uid,pat,ag,reg_date,due_date,cost,))
	except Exception as e:
		db.rollback()
		return render(request,'user_home.html',{'ERROR':str(e)})
	db.commit()
	try:
		return render(request,'user_home.html',{'ERROR':'REGISTRATION SUCCESSFUL'})
	except Exception as e:
		return render(request,'user_home.html',{'ERROR':str(e)})

@never_cache
def menu(request):
	return redirect('/user/')

@never_cache
def prev(request): #view previous tests
	if "user" not in request.session:
		return redirect('/')
	records = []
	try:
		ID = request.session["user"]
		cur.execute("select ID,PatientID,AgentID,RegDate,DueDate,Cost from reg_tests where UserID=%s",(ID,));
		records = cur.fetchall()
	except Exception as e:
		db.rollback()
		return render(request,'user_home.html',{'ERROR':str(e)})
	db.rollback()
	if(len(records)==0):
		return render(request,'prev.html',{'ERROR':'NO HISTORY FOUND'})
	else:
		return render(request,'prev.html',{'records':records})


@never_cache
def track(request): # track tests
	if "user" not in request.session:
		return redirect('/')
	records = []
	try:
		ID = request.session["user"]
		cur.execute("select ID,PatientID,AgentID,RegDate,DueDate,Cost,paid,rep_gen from reg_tests where UserID=%s and rep_gen='NO'order by RegDate DESC",(ID,));
		records = cur.fetchall()
	except Exception as e:
		db.rollback()
		return render(request,'user_home.html',{'ERROR':str(e)})
	db.rollback()
	if(len(records)==0):
		return render(request,'track.html',{'ERROR':'NO TESTS TO TRACK'})
	else:
		return render(request,'track.html',{'records':records})


@never_cache
def update(request): # update profile
	if "user" not in request.session:
		return redirect('/')
	try:
		ID = request.session["user"]
		cur.execute("select * from patient where ID=%s",(ID,))
		l = cur.fetchall()
	except:
		db.rollback()
		return redirect('/user/')
	db.rollback()
	d = {}
	d['ID'] = l[0][0]
	d['fname'] = l[0][1]
	d['lname'] = l[0][2]
	d['dob'] = l[0][3]
	d['age'] = l[0][4]
	d['adline'] = l[0][6]
	d['pin'] = l[0][7]
	d['phno'] = l[0][8]
	d['eid'] = l[0][9]
	try:
		return render(request,'update_form.html',d)
	except Exception as e:
		return redirect('/user/')

@never_cache
def update_check(request): # update profile validations
	if request.method!="POST":
		return redirect('/user/');
	if "user" not in request.session:
		return redirect('/')
	try:
		login = request.POST['id']
		fname = request.POST['fname']
		dob = request.POST['dob']
		phno = request.POST['phno']
		eid = request.POST['eid']
	except:
		return render(request,'user_home.html',{'ERROR':'FEILDS MARKED RED ARE NECESSARY'})
	lname = request.POST['lname']
	age = request.POST['age']
	addline = request.POST['addline']
	pincode = request.POST['pin']
	if len(pincode)!=0 and len(pincode)!=6:
		return render(request,'user_home.html',{'ERROR':'INVALID PINCODE'})
	try:
		if(len(pincode)==6):
			pincode = int(pincode)
		if len(age)>0:
			age = int(age)
	except Exception as e:
		return render(request,'user_home.html',{'ERROR':str(e)})
	try:
		cur.execute("update patient set phno=%s,age=%s,Address=%s,zipcode=%s where ID=%s",
		(phno,age,addline,pincode,login))
	except Exception as e:
		db.rollback()
		return render(request,'user_home.html',{'ERROR':str(e)})
	db.commit()
	try:
		return render(request,'user_home.html',{'ERROR':"PROFILE UPDATED"})
	except:
		return redirect('/user/')





# Create your views here.
