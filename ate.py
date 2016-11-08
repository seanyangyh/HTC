



from datetime import datetime
import json, requests

def UpdateMonitorReport(jobid, name, fc_id, result, description):
	url = "http://10.9.160.219:3000/MonitorReport/create"
	data = { "jobid":str(jobid), "item":str(name), "fcid":str(fc_id), "result":str(result), "description":str(description), "time":datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]}
	headers = { "Content-Type" : "application/json"}
	try:
		r = requests.post(url, data=json.dumps(data), headers=headers, timeout=5)
		print("[ate] UpdateMonitorReport: status_code:" + str(r.status_code) + ", content:" + str(r.content))
	except Exception as ex:
		print("[ate] UpdateMonitorReport: exception:" + str(type(ex)) + ", " + str(ex))

