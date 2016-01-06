import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

CAIC_WEATHER_BASEURL = "http://avalanche.state.co.us/caic/obs_stns/zones.php?date=%s&stnlink=hourly&unit=e&flag=on&area=caic&flag=on&span=6"

class CAICWeather(object):
	def generate_urls(self, start_date, end_date):
		""" generate CAIC weather urls based on start date and end date. 
		one URL per date. returns tuple of (datetime, url)"""
		## {start/end}_date are MM/DD/YYYY-HH
		input_format = "%m/%d/%Y-%H"

		start_date = datetime.strptime(start_date, input_format)
		end_date   = datetime.strptime(end_date, input_format)

		required_format = "%Y-%m-%d-%H"
		current = start_date
		urls = []
		while current != end_date + timedelta(hours=1):
			url_date = current.strftime(required_format)
			url = CAIC_WEATHER_BASEURL % url_date
			urls.append((current, url))
			current = current + timedelta(hours=1)

		return urls

	def is_row_valid(self, row):
		""" ensures temperature value is present """
		try: 
			int(row["Temp"])
			return True
		except ValueError:
			return False


	def get_stations(self, url, region):
		raw_page = requests.get(url)
		parser = BeautifulSoup(raw_page.text, "html.parser")

		## Parse CAIC data
		weather_table_raw = parser.find("h4", text=region).find_next("table").find_all("tr")
		table_header      = [head.text for head in weather_table_raw[0].find_all("th")]
		weather_stations  = [dict(zip(table_header, [cell.text for cell in row.find_all("td")])) for row in weather_table_raw[1:-1]]
		weather_stations  = [row for row in weather_stations if self.is_row_valid(row)]
		return weather_stations

	def get_station_info(self, wxtable):
		return [(row["Station"], row["Elev"], row["Provider"]) for row in wxtable]

	def selected_stations(self, stations):
		new_weather = []
		for hour, data in self.hourly_weather.iteritems():
			new_data = [row for row in data if row["Station"] in stations ]
			new_weather.append((hour, new_data))
		return dict(new_weather)

	def __init__(self, region, start_date, end_date):
		super(CAICWeather, self).__init__()
		urls = self.generate_urls(start_date, end_date)
		self.hourly_weather = { date[0] : self.get_stations(date[1], region) for date in urls } 
		self.stations       = self.get_station_info(self.hourly_weather.values()[0])
		

		