from flask import Flask, render_template
import SatTracker
from SatTracker.sattracker import *
from SatTracker.printer import *
import datetime
from datetime import datetime
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('welcome.html')


@app.route('/mymap')
def map():
    tracker = SatTracker()

    print("Setting ground segment Location.")
    gs_location = tracker.set_location()
    print_gs_location(gs_location)

    print("\nGetting TLE.")
    tracker.get_tle('KAZSTSAT', '../SatTracker/text_files/tle.txt')

    print("\nLoading TLE data.")
    tracker.load_tle('../SatTracker/text_files/tle.txt')

    print("\nGround longitude/latitude under that satellite now: ")
    for i in range(5):
        sat_info = tracker.find_sat_coordinates_for_now()
        print_sat_coordinates(sat_info)
        tracker.write_statistic()
        tracker.write_sat_coordinates()
        tracker.find_realtime_coord()
        time.sleep(5.0)
        tracker.observer.date = datetime.utcnow()
        return render_template('mymap.html')



if __name__ == '__main__':
    app.run(debug=True)
