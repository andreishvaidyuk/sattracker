
import ephem
import SatTracker.default as defaults
from datetime import datetime
import math
import time
import SatTracker.helpers as helpers
from SatTracker.helpers import *
import folium
import pandas as pd


class SatTracker:
    def __init__(self):
        self.id = None                              # name of satellite
        self.observer = ephem.Observer()            # observer class representing current location
        self.satellite = None                       # satellite object created by pyephem
        self.isActive = False                       # flag to see if satellite is computing
        self.tle = None                             # list of 2 line elements read
        self.location = {'latitude': defaults.gs_lat, 'longitude': defaults.gs_lon, 'elevation': defaults.gs_elev}

    def set_location(self, lat=None, lon=None, elevation=None):
        """
        Sets location of observer using coordinates (+N and +E).
        :param lat: Observer's latitude (positive north from the equator)
        :param lon: Observer's longitude (positive east from the prime meridian)
        :param elevation: Observer's elevation (meters above see level)
        :return Observer object
        """

        if lat:
            lat = lat
        else:
            lat = self.location['latitude']
        if lon:
            lon = lon
        else:
            lon = self.location['longitude']
        if elevation:
            elevation = elevation
        else:
            elevation = self.location['elevation']

        self.observer.lat = lat
        self.observer.lon = lon
        self.observer.elevation = elevation
        self.observer.epoch = ephem.Date(str(datetime.utcnow()))
        self.observer.date = ephem.Date(str(datetime.utcnow()))

        return self.observer

    def get_tle(self, sat_id, destination=None):
        """
        parses CELESTRAK for satellite's TLE data using its NORAD id.
        :param sat_id: Satellite's designation
        :param destination: Place to save the data for later use (optional).
        :return:
        """
        data = helpers.parse_text_tle(sat_id, base_CELESTRAK_URL, CELESTRAK_paths)
        print(data)
        if not data:
            return False
        try:
            if destination is not None:
                with open(destination, 'w') as file_object:
                    w_data = [data[0] + "\n"] + [data[1] + "\n"] + [data[2] + "\n"]
                    file_object.writelines(w_data)
            return True
        except:
            pass

    def load_tle(self, filename):
        """
        loads satellite TLE data from a text file
        :param filename: path of file
        """

        with open(filename) as file_object:
            data = file_object.readlines()
            for line in data:
                print(line.rstrip())
            self.satellite = ephem.readtle(data[0], data[1], data[2])
            self.tle = data
            self.id = data[0]

    def find_sat_coordinates_for_date(self, date):
        """
        Find Ground longitude/latitude under that satellite at a given time
        :param date: example - datetime.datetime(2019, 3, 1, 9, 48, 00) it means "2019, 1 march, 9:48:00"
        :return: list of satellite information
        """
        self.satellite.compute(self.observer, date)
        sat_coord_info = [date, self.satellite]
        return sat_coord_info

    def find_sat_coordinates_for_now(self):
        """
        Find Ground longitude/latitude under that satellite now
        :return: list of satellite information
        """
        self.satellite.compute(self.observer)
        date = datetime.utcnow()
        sat_coord_info = [date, self.satellite]
        return sat_coord_info

    def find_satellite_alt_az(self):
        """
        Find satellite altitude and azimuth for current time
        :return:
        """
        degrees_per_radian = 180.0 / math.pi
        print("\nSatellite: " + self.id)
        while True:
            self.observer.date = datetime.utcnow()
            self.satellite.compute(self.observer)
            print("altitude: %4.2f deg, azimuth: %5.2f deg" %
                  (self.satellite.alt*degrees_per_radian, self.satellite.az*degrees_per_radian))
            time.sleep(1.0)

    def next_pass(self):
        """
        The next_pass() method takes an EarthSatellite body and determines when it will next cross above the horizon.
        It returns a six-element tuple giving:
            0  Rise time
            1  Rise azimuth
            2  Maximum altitude time
            3  Maximum altitude
            4  Set time
            5  Set azimuth
        :return:
        """
        n = self.observer.next_pass(self.satellite)
        self.observer.date = ephem.Date(n[4] + ephem.minute)
        next_pass_info = [n, self.observer.date]
        return next_pass_info

    def visualization(self):
        map_simu = folium.Map(location=defaults.gs_location,
                              zoom_start=2, tiles="Mapbox Bright",
                              control_scale=True,
                              prefer_canvas=True,
                              )

        data = pd.read_csv("SatTracker\\text_files\Sat_pass_stat.txt")
        lat = data['LAT']
        lon = data['LON']

        for lat, lon in zip(lat, lon):
            folium.CircleMarker(location=[lat, lon], radius=5, fill_color='red', color='gray').add_to(map_simu)
            map_simu.save("map.html")

    def write_statistic(self):
        with open("SatTracker\\text_files\Sat_pass_stat.txt", 'a') as file_object:
            data = str(datetime.utcnow()) + "," + \
                   str(helpers.dms_to_deg(self.satellite.sublat)) + "," + \
                   str(helpers.dms_to_deg(self.satellite.sublong)) + "\n"
            file_object.writelines(data)
