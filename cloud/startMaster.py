from create_instance import main
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery


credentials = GoogleCredentials.get_application_default()
compute = discovery.build('compute', 'v1', credentials=credentials)
projectName = 'xenon-marker-147522' #need to modify 
bucketName = projectName + 'appspot.com'
region = 'us-east1-b'
instanceName = 'master'

main(projectName, bucketName, region, instanceName)


