from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.views.decorators.cache import never_cache


import matplotlib.pyplot as plt
from io import StringIO
import numpy as np

import MySQLdb as mdb

import hashlib
import datetime

from random import randint

db = mdb.connect('localhost','root','','path_lab')
cur = db.cursor()


#this page mainly contains the functions that are being used to implement
# the functionality of the green bar that appears on every page
# each button has its own uniue feature 


@never_cache
def index(request):
	try:
		return render(request,"start.html")
	except:
		return HttpResponse("Page Not Found")


@never_cache
def showGraph(request):
    context = {}
    context['graph'] = return_graph()
    return render(request, 'showGraph.html', context)
       
def return_graph():
    
    x= []
    y = []
    try:
        cur.execute('select distinct PatientID from reg_tests')
        PID = cur.fetchall()
        
        for i, ID in enumerate(PID):
            x.append(ID[0])
            try:
                cur.execute('select SUM(cost) FROM reg_tests WHERE PatientID = %s',(ID,))
                TCost = cur.fetchall()
                for i, cost in enumerate(TCost):
                    y.append(cost)
            except Exception as e:
                db.rollback()
                print(str(e))
                return redirect('/')
                
    except Exception as e:
        db.rollback()
        print(str(e))
        return redirect('/')
        
    print(x)
    db.rollback()
    
    
    fig = plt.figure()
    plt.plot(x,y)
    
    plt.xlabel("Patient's ID")
    plt.ylabel("Total lab test's cost in USD")
    
    fig.suptitle('Total lab test`s cost per patient', fontsize=12)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data


@never_cache
def menuhom(request):
	return redirect('/')

@never_cache
def lab(request):
	try:
		cur.execute('select distinct TestId from lab_test')
		ID = cur.fetchall()
	except Exception as e:
		db.rollback()
		print(str(e))
		return redirect('/')
	db.rollback()
	print('we')
	try:
		return render(request,'lab.html',{'records':ID})
	except:
		return redirect('/')


@never_cache
def tid_sub(request):
	if request.method!="POST":
		redirect('/')
	try:
		ID = request.POST['tid']
	except:
		redirect('/')
	try:
		print(ID)
		cur.execute('select * from lab_test where TestID=%s',(ID,))
		records = cur.fetchall()
	except:
		return redirect('/')
	try:
		return render(request,'showlt.html',{'records':records})
	except:
		return redirect('/')



@never_cache
def tetnam(request):
	try:
		cur.execute('select distinct Type from tests')
		records = cur.fetchall()
	except:
		db.rollback()
		return redirect('/')
	db.rollback()
	try:
		return render(request,'seltype.html',{'records':records})
	except:
		return redirect('/')
@never_cache
def testty(request):
	if request.method!="POST":
		redirect('/')
	try:
		ID = request.POST['tid']
		cur.execute('select * from tests where Type=%s',(ID,))
		records = cur.fetchall()
	except:
		return redirect('/')
	try:
		return render(request,'seltype1.html',{'records':records})
	except:
		return redirect('/')

@never_cache
def pathologistInfo(request):
	try:
		cur.execute('select ID from pathologist where working="YES" or working="L"')
		ag = cur.fetchall()
	except:
		db.rollback()
		return redirect('/')
	db.rollback()
	try:
		return render(request,'selag.html',{'records':ag})
	except:
		return redirect('/')
        
@never_cache
def agent_show(request):
	if request.method!="POST":
		redirect('/')
	try:
		ID = request.POST['aid']
		cur.execute('select ID,FName,LName,emailid,phno,Address,zipcode from pathologist where ID=%s',(ID,))
		records = cur.fetchall()
	except Exception as e:
		print(str(e))
		return redirect('/')
	try:
		return render(request,'showag.html',{'records':records})
	except:
		return redirect('/')



@never_cache
def getBills(request):
	try:
		cur.execute('select reg_tests.PatientID, patient.fname, patient.lname, reg_tests.RegDate, reg_tests.DueDate, reg_tests.cost, reg_tests.paid, tests.name  from reg_tests INNER JOIN patient ON reg_tests.PatientID = patient.id INNER JOIN lab_test ON reg_tests.LTID = lab_test.ID INNER JOIN tests ON lab_test.TestID = tests.ID')
		bills = cur.fetchall()
	except:
		db.rollback()
		return redirect('/')
	db.rollback()
	try:
		return render(request,'getBills.html',{'bills':bills})
	except:
		return redirect('/') 


def getPatients(request):
	try:
		cur.execute('select * FROM patient')
		patients = cur.fetchall()
	except:
		db.rollback()
		return redirect('/')
	db.rollback()
	try:
		return render(request,'patients.html',{'patients':patients})
	except:
		return redirect('/') 
