# coding=utf8

import plotly.plotly as plt
import plotly.graph_objs as graphobjs
import argparse
from caicweather import CAICWeather

parser = argparse.ArgumentParser(description="Find inversions across a pair of weather stations. By default chooses highest and lowest stations in given region unless otherwise supplied.")
parser.add_argument('start_date', help="Data Start Time (MM/DD/YYYY-HH)")
parser.add_argument('end_date', help="Data End Date (MM/DD/YYYY-HH)")
parser.add_argument('region', help="Name of CAIC region.")
parser.add_argument('--stations', help="Stations to plot. See --station_list for available stations in region", nargs='+')
parser.add_argument('--station_list', action='store_true', help="List known station names and quit.")
parser.add_argument('--data', action="store_true", help="output csv file with requested data.")
parser.add_argument('--image', help="Download image of plot. Provide filename (.png, .jpg, or .pdf only)")
arguments = parser.parse_args()


## download weather
weather = CAICWeather(arguments.region, arguments.start_date, arguments.end_date)

if arguments.station_list:
	print weather.station_list
	exit(0)

## choose pertinent stations
wx_stations = arguments.stations
if arguments.stations:
	weather_data = weather.selected_stations(wx_stations)
else:
	## sort known sttations by elevation 
	stations_sorted = sorted(weather.stations, key=lambda x: int(x[1]), reverse=True)
	high_station = stations_sorted[0]
	low_station  = stations_sorted[-1]
	high_station_name = high_station[0]
	low_station_name  = low_station[0]
	wx_stations.append(high_station_name)
	wx_stations.append(low_station_name)
	weather_data = weather.selected_stations([high_station_name, low_station_name]	)


## get traces together for all stations
traces = []
for station in wx_stations:
	station_data = []
	for hour in weather_data.keys(): ## pull apart weather data. TODO: Bettter way to do this
		station_temp = [row["Temp"] for row in weather_data[hour] if row["Station"] == station]

		if not station_temp:
			station_data.append((hour, 'n/a'))
		else:
			station_data.append((hour, station_temp[0]))

	station_data.sort(key=lambda x: x[0])
	station_times, station_temps = zip(*station_data)

	trace = graphobjs.Scatter(x = station_times,
							  y = station_temps,
							  name = station)
	traces.append(trace)



graphtitle = "Inversion: {0} to {1}".format(str(arguments.start_date), str(arguments.end_date))
layout = graphobjs.Layout(title = graphtitle,
						  yaxis = graphobjs.YAxis(title="Temperature (°F)"),
						  xaxis = graphobjs.XAxis(title="Time"))
figure = graphobjs.Figure(data=traces, layout=layout)
plot = plt.iplot(figure, filename=graphtitle)

print plot.resource

if arguments.image:
	plt.image.save_as(figure, arguments.image)

