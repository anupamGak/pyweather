import requests
from lxml import html
import csv
import time
import argparse

class WeatherStation:
	def __init__(self, filename):
		self.wind_speed = 0
		self.wind_dir = 0
		self.wind_gust = 0
		self.temp = 0
		self.humidity = 0
		self.node = 0
		self.data = []
		self.payload = {}
		self.data_time = 0

		self.net_address = "http://192.168.137.99/livedata.htm"

		self.datafile = 0
		self.datawriter = 0
		self.file_time = time.localtime()
		self.filename = filename

		self.uploader = 0

	def get_data(self):
		self.response = requests.get(self.net_address)
		self.tree = html.fromstring(self.response.text)

		self.node = self.tree.xpath("//input[@name='CurrTime']")[0]
		self.data_time = self.node.get("value")

		self.node = self.tree.xpath("//input[@name='CurrTime']")[0]
		self.data_time = self.node.get("value")

		self.node = self.tree.xpath("//input[@name='avgwind']")[0]
		self.wind_speed = self.node.get("value")

		self.node = self.tree.xpath("//input[@name='windir']")[0]
		self.wind_dir = self.node.get("value")

		self.node = self.tree.xpath("//input[@name='gustspeed']")[0]
		self.wind_gust = self.node.get("value")

		self.node = self.tree.xpath("//input[@name='outTemp']")[0]
		self.temp = self.node.get("value")

		self.node = self.tree.xpath("//input[@name='outHumi']")[0]
		self.humidity = self.node.get("value")

	def upload_data(self):
		self.payload = {
		"action" : "updateraw",
		"ID" : "KCOBOULD381",
		"PASSWORD" : "bv4te8rq",
		"dateutc" : "now",
		"winddir" : self.wind_dir,
		"windspeedmph" : self.wind_speed,
		"windgustmph" : self.wind_gust,
		"tempf" : self.temp,
		"humidity" : self.humidity
		}

		self.uploader = requests.get("https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php", params=self.payload)
#		print self.uploader.text

	def save_data(self):
		self.data = [self.data_time, self.wind_speed, self.wind_dir, self.temp]

		with open(self.filename + ".csv", 'ab') as self.datafile:
			self.datawriter = csv.writer(self.datafile)
			self.datawriter.writerow(self.data)

	def display(self):
		print self.data_time, " || ", self.temp, " || ", self.wind_speed



parser = argparse.ArgumentParser()
parser.add_argument("-d", "--duration", help="Duration of data collection in min", type=int)
parser.add_argument("-f", "--filename", help="File name for the resulting csv data file")
args = parser.parse_args()

if not args.filename:
	file_time = time.localtime()
	args.filename = 'winddata_(%d-%d-%d).csv' % (file_time.tm_year, file_time.tm_mon, file_time.tm_mday)

station = WeatherStation(args.filename)
tick = 0

while tick < args.duration:
	starttime = time.time()

	station.get_data()

	tick = tick + 1
	
	station.upload_data()
	station.display()
	station.save_data()

	time.sleep(60 - (time.time() - starttime))

#	'winddata_(%d-%d-%d).csv' % (self.file_time.tm_year, self.file_time.tm_mon, self.file_time.tm_mday)