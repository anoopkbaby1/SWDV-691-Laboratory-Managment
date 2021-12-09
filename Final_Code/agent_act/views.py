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

db = mdb.connect('localhost','root','','path_lab')
cur = db.cursor()

@never_cache
def load_home2(request): #loads agent dashboard
	if "pathologist" in request.session:
		return render(request,'agent_home.html',{'text':request.session["pathologist"]})
	else:
		return redirect('/')

@never_cache
def go_home2(request): #go to home
	try:
		del request.session['pathologist']
		return redirect('/')
	except:
		return redirect("/agent/")

@never_cache
def menu(request):
	return redirect('/agent/')

@never_cache
def view_t(request): # view the tests that have been assigned to that user
	if "pathologist" not in request.session:
		return redirect('/')
	records = []
	try:
		ID = request.session["pathologist"]
		cur.execute("select reg_tests.ID,reg_tests.LTID,lab_test.TestID, tests.Name, reg_tests.PatientID, patient.fname, patient.lname, reg_tests.RegDate,reg_tests.DueDate, reg_tests.cost,reg_tests.paid from reg_tests INNER JOIN patient ON reg_tests.PatientID = patient.id INNER JOIN lab_test ON lab_test.ID = reg_tests.LTID INNER JOIN tests ON tests.ID = lab_test.TestID where reg_tests.AgentID=%s and reg_tests.rep_gen='NO' order by reg_tests.RegDate DESC",(ID,));
		records = cur.fetchall()
	except Exception as e:
		db.rollback()
		return render(request,'agent_home.html',{'ERROR':str(e)})
	db.rollback()
	if(len(records)==0):
		return render(request,'view_tests.html',{'ERROR':'NO TESTS AVAILABLE'})
	else:
		return render(request,'view_tests.html',{'records':records})

@never_cache
def track_t(request): # tracking of tests
	if "pathologist" not in request.session:
		return redirect('/')
	records = []
	try:
		ID = request.session["pathologist"]
		cur.execute("select reg_tests.ID,reg_tests.PatientID,patient.fname,patient.lname, reg_tests.AgentID, pathologist.fname, pathologist.lname, reg_tests.RegDate, reg_tests.DueDate, reg_tests.Cost, reg_tests.paid, reg_tests.rep_gen from reg_tests INNER JOIN patient ON reg_tests.PatientID = patient.id INNER JOIN pathologist ON pathologist.id = reg_tests.AgentID where reg_tests.AgentID=%s",(ID,));
		records = cur.fetchall()
	except Exception as e:
		db.rollback()
		return render(request,'agent_home.html',{'ERROR':str(e)})
	db.rollback()
	if(len(records)==0):
		return render(request,'agent_track.html',{'ERROR':'NO TESTS TO TRACK'})
	else:
		return render(request,'agent_track.html',{'records':records})

@never_cache
def sel_test(request): # select test for updation of tracking and payment details
	if "pathologist" not in request.session:
		return redirect('/')
	testid = []
	try:
		ID = request.session["pathologist"]
		cur.execute("select ID from reg_tests where AgentID=%s and rep_gen='NO'",(ID,));
		testid = cur.fetchall()
	except:
		db.rollback()
		return render(request,'agent_home.html',{'ERROR':'UNEXPECTED ERROR'})
	db.rollback()
	if len(testid)==0:
		try:
			return render(request,'agent_home.html',{'ERROR':'NO TESTS TO UPDATE'})
		except:
			print('neymar')
			return redirect('/agent/')
	else:
		try:
			return render(request,'update_test.html',{'records':testid})
		except:
			print('iniesta')
			return redirect('/agent/')

@never_cache
def update_d(request): # select update details for the test
	if request.method!="POST":
		return redirect('/agent/')
	if "pathologist" not in request.session:
		return redirect('/')
	try:
		ID = request.POST['pat']
		repgen = request.POST['repgen']
		paid = request.POST['paid']
	except Exception as e:
		return render(request,'agent_home.html',{'ERROR':str(e)})
	try:
		int(paid)
	except Exception as e:
		return render(request,'agent_home.html',{'ERROR':str(e)})
	try:
		cur.execute("update reg_tests set rep_gen=%s,paid=%s where ID=%s",
			(repgen,paid,ID))
	except Exception as e:
		db.rollback()
		return render(request,'agent_home.html',{'ERROR':str(e)})
	db.commit()
	try:
		return render(request,'agent_home.html',{'ERROR':'Test Data Successfully Updated'})
	except Exception as e:
		return redirect('/agent/')

@never_cache
def patient(request): # select patient and then view its details
	if "pathologist" not in request.session:
		return redirect('/')
	pat = []
	try:
		ID = request.session["pathologist"]
		cur.execute("select distinct PatientID from reg_tests where AgentID=%s",(ID,));
		pat = cur.fetchall()
	except:
		db.rollback()
		return render(request,'agent_home.html',{'ERROR':'UNEXPECTED ERROR'})
	db.rollback()
	if len(pat)==0:
		try:
			return render(request,'agent_home.html',{'ERROR':'NO PATIENT DETAILS'})
		except:
			return redirect('/agent/')
	else:
		try:
			return render(request,'pats.html',{'records':pat})
		except:
			return redirect('/agent/')

@never_cache
def display(request): #display the details of the selected patient
	if request.method!="POST":
		return redirect('/agent/')
	if "pathologist" not in request.session:
		return redirect('/')
	try:
		ID = request.POST['pat']
	except Exception as e:
		return render(request,'agent_home.html',{'ERROR':str(e)})
	try:
		cur.execute("select fname,lname,gender,dob,emailid,phno from patient where id=%s",(ID,))
		user = cur.fetchall()
	except Exception as e:
		db.rollback()
		return render(request,'agent_home.html',{'ERROR':str(e)})
	db.rollback()
	
	if len(user)==0:
		try:
			return render(request,'agent_home.html',{'ERROR':'PATIENT DETAILS NOT FOUND'})
		except:
			return redirect('/agent/')
	if len(user)!=0:
		try:
			return render(request,'dis_det.html',{'records':user})
		except:
			return redirect('/agent/')
	return redirect('/agent/')






