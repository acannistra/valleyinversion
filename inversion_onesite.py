# coding=utf8

import plotly.plotly as plt
import plotly.graph_objs as graphobjs
import argparse
from caicweather import CAICWeather

parser = argparse.ArgumentParser(description="Find inversions across a pair of weather stations. By default chooses highest and lowest stations in given region unless otherwise supplied.")
parser.add_argument('start_date', help="Data Start Time (MM/DD/YYYY-HH)")
parser.add_argument('end_date', help="Data End Date (MM/DD/YYYY-HH)")
parser.add_argument('region', help="Name of CAIC region.")
parser.add_argument('--high_station', help="Name of high-altitude station.")
parser.add_argument('--low_station', help="Name of low-altitude station.")
parser.add_argument('--stations', action='store_true', help="List known station names and quit.")
parser.add_argument('--data', action="store_true", help="output csv file with requested data.")
parser.add_argument('--image', help="Download image of plot. Provide filename (.png, .jpg, or .pdf only)")
arguments = parser.parse_args()


## download weather
weather = CAICWeather(arguments.region, arguments.start_date, arguments.end_date)

if arguments.stations:
	print weather.stations
	exit(0)

## choose pertinent stations
if arguments.high_station and arguments.low_station:
	high_station_name = arguments.high_station
	low_station_name  = arguments.low_station

	weather_data = weather.selected_stations([arguments.high_station, arguments.low_station])
else:
	## sort known sttations by elevation 
	stations_sorted = sorted(weather.stations, key=lambda x: int(x[1]), reverse=True)
	high_station = stations_sorted[0]
	low_station  = stations_sorted[-1]
	high_station_name = high_station[0]
	low_station_name  = low_station[0]
	weather_data = weather.selected_stations([high_station[0], low_station[0]])


## get two traces together for the plot -- high and low. 
high_station_wx, low_station_wx = [], []
for hour in weather_data.keys(): ## pull apart weather data. TODO: Bettter way to do this
	hs_wx_temp = [row["Temp"] for row in weather_data[hour] if row["Station"] == high_station_name]
	ls_wx_temp = [row["Temp"] for row in weather_data[hour] if row["Station"] == low_station_name]
	high_station_wx.append((hour, hs_wx_temp[0]))
	low_station_wx.append((hour, ls_wx_temp[0]))

high_station_wx.sort(key=lambda x: x[0])
low_station_wx.sort(key=lambda x: x[0])

hs_time, hs_temps = zip(*high_station_wx)
ls_time, ls_temps = zip(*low_station_wx)

## plot

high_trace = graphobjs.Scatter(x = hs_time, 
							   y = hs_temps,
							   name = high_station_name)
low_trace  = graphobjs.Scatter(x = ls_time,
							   y = ls_temps, 
							   name = low_station_name)

data = [high_trace, low_trace]

graphtitle = "Inversion: {0} to {1}".format(str(hs_time[0]), str(hs_time[-1]))
layout = graphobjs.Layout(title = graphtitle,
						  yaxis = graphobjs.YAxis(title="Temperature (°F)"),
						  xaxis = graphobjs.XAxis(title="Time"))
figure = graphobjs.Figure(data=data, layout=layout)
plot = plt.iplot(figure, filename="valley_inversion_twosites")

print plot.resource

if arguments.image:
	plt.image.save_as(figure, arguments.image)

