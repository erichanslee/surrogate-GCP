from create_instance import create_instance
from create_instance import delete_instance
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from random import random

# cloudUnit is a logical grouping of a Master Instance and Worker Instances, to be used for surrogate optimization.
# cloudUnits may be initalized completely on one's local machine. Alternatively, one may instead initalize the master locally
# and have the master initalize its own workers remotely. 

class cloudUnit:

	def __init__(self, projectName):
		# Names of Instances
		self.masterId = None
		self.region = None
		self.workerIds = []
		credentials = GoogleCredentials.get_application_default()
		compute = discovery.build('compute', 'v1', credentials=credentials)
		self.credentials = credentials
		self.compute = compute
		self.projectName = projectName
		self.bucketName = projectName + '.appspot.com'
		self.numWorkers = 0;

	def startMaster(self, region = 'us-east1-b'):
		instanceName = 'master'
		self.region = region
		# Makes sure master has not been allocated already
		if(self.masterId == None):
			self.masterId = instanceName
			create_instance(self.compute, self.projectName, region, instanceName, self.bucketName)
			print 'Master Started in region: ', region
		else:
			print 'Master already exists, instance initialization failed'

	def startWorker(self):
		# worker given a unique 10 digit ID and initialized in the same region as master
		fp = str(rand())
		instanceName = 'worker' + fp[2:12]
		self.workerIDs.append(instanceName)

		# Use create_instance from GCP Python API
		create_instance(self.compute, self.projectName, self.region, instanceName, self.bucketName)		
		self.numWorkers = self.numWorkers + 1
		print 'Worker ', instanceName, ' Started in region: ', region

	def startWorkers(self, n):
		for i in range(0,n):
			self.startWorker()

	def deleteInstance(self, instanceId):
		try:
			operation = delete_instance(self.compute, self.projectName, self.region, instanceId)
			wait_for_operation(compute, project, zone, operation['name'])
			# If master isn't deleted, decrement numWorkers
			if(instanceId != 'master'):
				self.numWorkers = self.numWorkers - 1
				print 'Deleting instance ', instanceId
			else:
				print 'Deleting master'

		except:
			print 'Unexpected Error'

	def cleanup(self):
		print 'Cleaning up cloud unit'
		# Delete Workers first
		if(self.workerIds != []):
			for workerId in self.workerIds:
				self.deleteWorker(workerId)

		# Delete Master last
		self.deleteInstance('master')
		print 'Cleanup Done'
