from firebase import firebase
import json
import datetime
import os


firebase = firebase.FirebaseApplication(os.environ['FIREBASE'], None)

def adddataFirebase(data):
	'''
	Add the email to the database
	'''
	now = datetime.datetime.now()
	jsondata = json.loads(data.decode('utf-8'))
	jsondata['timestamp']= now
	print(jsondata)
	airport = str(jsondata['airport'])
	run = str(jsondata['run'])
	


	result = firebase.post('/run/'+airport+'/'+run+'/', jsondata, params={'print': 'pretty'})
	print(result)