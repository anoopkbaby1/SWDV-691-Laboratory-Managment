from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse

from django.views.decorators.cache import never_cache

import MySQLdb as mdb

import hashlib
import smtplib


db = mdb.connect('localhost','root','','path_lab')
cur = db.cursor()

error = "Some Issue Experienced !!!!"
host = '127.0.0.1'

@never_cache
def log_in(request): #reuest for login page
	if(len(request.session.keys())!=0):
		if "user" in request.session:
			return redirect('/user/')
		elif "pathologist" in request.session:
			return redirect('/agent/')
		elif "admin" in request.session:
			return redirect('/admin_act/')
		else:
			return redirect('/')
	try:
		return render(request,"login_form.html")
	except:
		return HttpResponse("Page Not Found !!!!")

@never_cache
def signup(request): #request for signup page
	if(len(request.session.keys())!=0):
		if "user" in request.session:
			return redirect('/user/')
		elif "pathologist" in request.session:
			return redirect('/agent/')
		elif "admin" in request.session:
			return redirect('/admin_act/')
		else:
			return redirect('/')
	try:
		return render(request,"sign_up.html")
	except:
		return HttpResponse("Page Not Found !!!")

@never_cache
def login_auth(request): #authorization of login
	if(request.method!='POST'):
		return render(request,'login_form.html')
	if(len(request.session.keys())!=0):
		if "user" in request.session:
			return redirect('/user/')
		elif "pathologist" in request.session:
			return redirect('/agent/')
		elif "admin" in request.session:
			return redirect('/admin_act/')
		else:
			return redirect('/')
	try:
		login = ''
		pswd = ''
		role = ''
		emailid = ''
		login = request.POST['id']
		emailid = request.POST['emailid']
		pswd = request.POST['paswd']
		role = request.POST['role']
	except:
		return render(request,'login_form.html')
	hashfunc = hashlib.md5()
	hashfunc.update(pswd.encode('utf-8'))
	pswd = hashfunc.hexdigest()
	print(pswd)
	try:
		if login=='' or pswd=='' or role=='':
			return render(request,'login_form.html',{'ERROR':'FILL IN ALL VALUES'}) #look for credentials based on the type of user
		if role == 'user':
			cur.execute('select count(*) from patient where ID=%s and password=%s and emailid=%s',(login,pswd,emailid))
		elif role == 'pathologist':
			cur.execute('select count(*) from pathologist where ID=%s and password=%s and emailid=%s and working="YES" or working="L"',(login,pswd,emailid))
		else:
			cur.execute('select count(*) from admin where ID=%s and password=%s and emailid=%s',(login,pswd,emailid))
		count = cur.fetchall()[0][0]
		print(count)
	except:
		db.rollback()
		return render(request,'login_form.html',{'ERROR':'UNEXPECTED ERROR'})
	db.rollback()
	print('@#$')
	try:
		if count == 1:
			request.session[role] = login
			print('asd')
		else:
			return render(request,'login_form.html',{'ERROR':'MISMATCH IN LOGIN CREDENTIALS'})		
		if role == 'user':
			print('jfk')
			return redirect('/user/')
		elif role == 'pathologist':
			return redirect('/agent/')
		elif role == 'admin':
			return redirect('/admin_act/')
		else:
			return redirect('/')
	except:
		return render(request,'login_form.html',{'ERROR':'UNEXPECTED ERROR'})
		print('finish')

@never_cache
def reg(request): # sign up form for users
	if request.method!="POST":
		return render(request,'sign_up.html');
	if(len(request.session.keys())!=0):
		if "user" in request.session:
			return redirect('/user/')
		elif "pathologist" in request.session:
			return redirect('/agent/')
		elif "admin" in request.session:
			return redirect('/admin_act/')
		else:
			return redirect('/')
	try:
		login = request.POST['id']
		fname = request.POST['fname']
		dob = request.POST['dob']
		gender = request.POST['gender']
		phno = request.POST['phno']
		eid = request.POST['eid']
		passwd = request.POST['passwd']
		repwd = request.POST['repwd']
	except:
		return render(request,'sign_up.html',{'ERROR':'FEILDS MARKED RED ARE NECESSARY'})
	lname = request.POST['lname']
	age = request.POST['age']
	addline = request.POST['addline']
	pincode = request.POST['pin']
	if len(login.split(' '))>1:
		return render(request,'sign_up.html',{'ERROR':'SPACE NOT ALLOWED IN USER ID'})
	if repwd!=passwd:
		return render(request,'sign_up.html',{'ERROR':'PASSWORDS DO NOT MATCH'})
	if len(passwd)<8 or len(passwd)>20:
		return render(request,'sign_up.html',{'ERROR':'PASSWORD LENGTH MUST BE >=8 and <=20'})
	if len(pincode)!=0 and len(pincode)!=6:
		return render(request,'sign_up.html',{'ERROR':'INVALID PINCODE'})
	try:
		int(pincode)
		int(age)
	except Exception as e:
		return render(request,'sign_up.html',{'ERROR':str(e)})
	hashfunc = hashlib.md5()
	hashfunc.update(passwd.encode('utf-8'))
	passwd = hashfunc.hexdigest()
	gender.lower()
	try:
		cur.execute('insert into patient values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(login,fname,lname,dob,age,gender,addline,pincode,phno,eid,passwd))
	except Exception as e:
		print(e)
		db.rollback()
		s = str(e)	
		return render(request,'sign_up.html',{'ERROR':s})
	db.commit()
	return render(request,'login_form.html',{'ERROR':'Registration Successful'})

@never_cache
def red(request):
	return redirect('/')

