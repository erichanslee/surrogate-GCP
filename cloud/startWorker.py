# To be executed by the master sitting on top of the cloud
from create_instance import main
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

def startWorker(workerid):
	credentials = GoogleCredentials.get_application_default()
	compute = discovery.build('compute', 'v1', credentials=credentials)
	projectName = 'xenon-marker-147522' #need to modify 
	bucketName = projectName + 'appspot.com'
	region = 'us-east1-b'
	instanceName = 'worker' + str(workerid)

	create_instance(projectName, bucketName, region, instanceName)
