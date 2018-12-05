	


def SendtoApi():
	"""
	Used tp sne ddata to api gateway
	"""


	req = urllib.request.Request(endpoint)
	req.add_header('Content-Type', 'application/json; charset=utf-8')
	jsondata = json.dumps(str(data))
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
		Send data to API
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, data)
	print(response.getcode())

	if response.getcode() == 200:
		print("sent")
	else:
    	print("Error send back to que")