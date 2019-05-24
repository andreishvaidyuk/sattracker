from SatTracker import helpers
import SatTracker.default as defaults


def print_sat_coordinates(sat_coord_info):
    """
    Print satellite information
    :param sat_coord_info:
    :return:
    """
    print("Time: " + str(sat_coord_info[0]))
    print("Latitude: " + str(sat_coord_info[1].sublat),
          "\nLongitude: " + str(sat_coord_info[1].sublong),
          "\nAltitude: " + str(sat_coord_info[1].alt * defaults.degrees_per_radian),
          "\nAzimuth: " + str(sat_coord_info[1].az * defaults.degrees_per_radian),
          "\nGeocentric height above sea level (km): " + str(sat_coord_info[1].elevation/1000),
          "\nDistance from observer to satellite (km): " + str(sat_coord_info[1].range/1000),
          "\nRange rate of change (m/s): " + str(sat_coord_info[1].range_velocity),
          "\nWhether satellite is in Earth’s shadow: " + str(sat_coord_info[1].eclipsed),
          "\n"
          )


def print_next_passes(next_pass):
    """
    Print satellite next_passes
    :param next_pass: info about next pass
    It returns a six-element tuple giving:
            0  Rise time
            1  Rise azimuth
            2  Maximum altitude time
            3  Maximum altitude
            4  Set time
            5  Set azimuth
    :param count: count of next passes
    :return:
    """
    print("Next pass time: " + str(next_pass[0][4]) +
          "\nMaximum altitude: " + str(next_pass[0][3]) +
          "\nMaximum altitude time: " + str(next_pass[0][2]) + "\n"
          )


def print_gs_location(gs_location):
    print("Ground segment Location: " +
          "\nLatitude: " + str(helpers.dms_to_deg(gs_location.lat)) + '; ' +
          "\nLongitude: " + str(helpers.dms_to_deg(gs_location.lon)) + '; ' +
          "\nElevation: " + str(gs_location.elevation) + ' meters')
