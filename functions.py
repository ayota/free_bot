from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from datetime import datetime
from time import mktime 
import time, urllib2, errno, tweepy, time, sys
from socket import error as SocketError
import folium
import random

def scraper():
	geolocator = Nominatim(country_bias="USA")

	free_things = {}
	links = 'http://washingtondc.craigslist.org/search/zip'

	try:
	    page = urllib2.urlopen(links)
	except SocketError as e:
	    if e.errno != errno.ECONNRESET:
	        raise #Not error we are looking for
	    else:
	    	time.sleep(30)
	    pass 

	soup = BeautifulSoup(page.read())

	for thing in soup.find_all('p','row'):
		now = mktime(datetime.now().timetuple())
		item_time = thing.time['datetime']
		item_2 = time.strptime(item_time, "%Y-%m-%d %H:%M")
		item = mktime(item_2)

		if item > (now - 7200): 
		 	name = thing.find('a', 'hdrlnk').get_text()
			link = 'http://washingtondc.craigslist.org' + thing.a['href']
			loc = thing.find('span', 'pnr').small
			location = str(loc).strip("<small> (").strip(")</small>")
			try:
				coord = geolocator.geocode(location)
				lat = coord.latitude
				lng = coord.longitude
	 		except:
	 			location = "DC"
	 			lat = 38.8951
	 			lng = -77.0367
	 		free_things[name] = {'location': location, 'lat': lat, 'lng': lng, 'link': link}
	 	else:
	 		break
	return free_things

def tweeter(free_things):
	CONSUMER_KEY = 'CONSUMER_KEY'
	CONSUMER_SECRET = 'CONSUMER_SECRET'
	ACCESS_KEY = 'ACCESS_KEY'
	ACCESS_SECRET = 'ACCESS_SECRET'
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
	api = tweepy.API(auth)

	for name,info in free_things.iteritems():
		tweet = "{0}: {1} // more: {2}".format(info['location'], name, info['link'])
		api.update_status(tweet, lat = info['lat'], long= info['lng'])
		time.sleep(900) #tweet every 15 minutes

def mapper(free_things):
	map_osm = folium.Map(location=[38.8951, -77.0367])
	for name, item in free_things.iteritems():
		hexa = hex(random.randint(0, 16777215))[2:].upper()
		color = "#{0}".format(hexa)
		map_osm.circle_marker(location=[item['lat'], item['lng']], radius=300, 
			popup="<h3>{0} [{1}]</h3><a href='http://{2}' target='_blank'>view ad</a>".format(name,item['location'],item['link']), 
			line_color=color, fill_color=color, fill_opacity=0.7)
	map_osm.create_map(path='index.html')




	
