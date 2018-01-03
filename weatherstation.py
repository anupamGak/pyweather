import requests
from lxml import html
import csv
import time

class WeatherStation:
	def __init__(self):
		self.wind_speed = 0
		self.wind_dir = 0
		self.wind_gust = 0
		self.temp = 0
		self.humidity = 0
		self.node = 0
		self.data = []
		self.payload = {}
		self.data_time = 0

		self.datafile = 0
		self.datawriter = 0

		self.uploader = 0

		self.response = requests.get("http://192.168.137.99/livedata.htm")
		self.tree = html.fromstring(self.response.text)

	def get_data(self):
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
		print self.uploader.text

	def save_data(self):
		self.data = [self.data_time, self.wind_speed, self.wind_dir, self.temp]

		with open('data2.csv', 'ab') as self.datafile:
			self.datawriter = csv.writer(self.datafile)
			self.datawriter.writerow(self.data)


station = WeatherStation()
tick = 0

while True:
	starttime = time.time()

	station.get_data()

	tick = tick + 1
	print "Tick ", tick, " ",
	
	station.upload_data()

	time.sleep(60 - (time.time() - starttime))