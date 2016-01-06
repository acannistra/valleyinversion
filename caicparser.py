import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

CAIC_WEATHER_BASEURL = "http://avalanche.state.co.us/caic/obs_stns/zones.php?date=%s&stnlink=hourly&unit=e&flag=on&area=caic&flag=on&span=6"

class CAICWeather(object):
	def generate_urls(start_date, end_date):
		""" generate CAIC weather urls based on start date and end date. 
		one URL per date"""
		## {start/end}_date are MM/DD/YYYY HH
		input_format = "%m/%d/%Y %H"

		start_date = datetime.strptime(start_date, input_format)
		end_date   = datetime.strptime(end_date, input_format)

		required_format = "%Y-%m-%d-%H"
		current = start_date
		urls = []
		while current not end_date + timedelta(hours=1):
			url_date = current.strftime(required_format)
			url = CAIC_WEATHER_BASEURL % url_date
			print url
			urls.append(url)
			current = current + timedelta(hours=1)

		return urls



	def __init__(self, region, start_date, end_date):
		super(CAICParser, self).__init__()
		print generate_urls(start_date, end_date)
				

		