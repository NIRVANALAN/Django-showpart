import json
from django.core.files.storage import DefaultStorage
from visuService.dataUtil.visu import exportVisuData
from visuService.dataUtil.readinfo import readinfo
from visuService.dataUtil.assomining import getNormalizedBoolData, getTimeRelatedData, apriori_algo, exportCSV, mine, \
	read_sequences, getAssoResult
import pprint as pp
from visuService.dataUtil.anoDetection import cluster
import argparse
import requests


class dataHandler():
	traceTXTpath = '/media/visuService/txt/swdata.txt'
	infoJSONpath = '/media/visuService/json/datainfo.json'
	allJSONpath = '/media/visuService/json/all.json'
	visuJSONpath = '/media/visuService/json/visudata.json'
	assoCSVpath = '/media/visuService/csv/sequenceData.csv'
	anoJPGpath = '/media/visuService/jpg/anoDetection.jpg'
	dotJSONpath = '/media/visuService/json/dotbook.json'
	pathJSONpath = '/media/visuService/json/pathbook.json'
	Base = "http://172.20.10.3:8081/person_search/api"
	
	defaultStorage = DefaultStorage()
	
	def __init__(self):
		# if self.defaultStorage.exists(self.traceTXTpath) and self.defaultStorage.exists(self.infoJSONpath):
		#   print("base data exist")
		# else:
		self.getBaseData()
		print("load base data")
	
	# save base data to the path
	
	def getVisuData(self):
		if self.defaultStorage.exists(self.traceTXTpath) and self.defaultStorage.exists(self.infoJSONpath):
			print("base data exist")
			exportVisuData(self)
		else:
			print("uable to do this for base data not exists")
	
	def getAssoData(self):
		self.support_threshold = 10
		paths = getAssoResult(self)
		return paths
	
	def getAnoResult(self):
		cluster(self)
	
	def getBaseData(self):
		self.get_traces()
		self.get_videos()
	
	def get_traces(self):
		url = self.Base + "/traces"
		request = requests.get(url)
		print(request.content)
		with open(self.traceTXTpath, 'wb') as f:
			f.write(request.content)
		return request.content
	
	def get_videos(self):
		url = self.Base + "/videos"
		request = requests.get(url)
		with open(self.infoJSONpath, 'w') as f:
			f.write(json.dumps(request.json()))
		
		return request.json()
