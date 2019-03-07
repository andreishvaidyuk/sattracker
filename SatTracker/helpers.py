

import ephem
import requests
import re

base_N2YO_URL = 'http://www.n2yo.com/satellite/?s='
base_CELESTRAK_URL = 'http://www.celestrak.com/NORAD/elements/'
CELESTRAK_paths = ('stations.txt', 'weather.txt', 'noaa.txt', 'goes.txt', 'resource.txt', 'sarsat.txt.', 'dmc.txt', 'tdrss.txt', 'argos.txt',
                                'geo.txt', 'intelsat.txt', 'gorizont.txt', 'raduga.txt', 'molniya.txt', 'iridium.txt', 'orbcomm.txt', 'globalstar.txt',
                                'amateur.txt', 'x-comm.txt', 'other-comm.txt', 'gps-ops.txt', 'glo-ops.txt', 'galileo.txt', 'beidou.txt',
                                'sbas.txt', 'nnss.txt', 'musson.txt', 'science.txt', 'geodetic.txt', 'engineering.txt', 'education.txt', 'military.txt',
                                'radat.txt', 'cubesat.txt', 'other.txt', 'tle-new.txt')


def parse_text_tle(target, baseURL, extensions=('',)):
    """
    Parse text files containing TLE data to identify satellite name and elements.
    :param target: Name of Satellite
    :param baseURL: base_CELESTRAK_URL
    :param extensions: CELESTRAK_paths
    :return:
    """
    # pattern = target + r'[\s)(]*?.*?[\n\r](.+?)[\n\r](.+?)[\n\r]'
    pattern = r'[\s]*?.*?' + str(target) + r'[\t )(]*?.*?[\n\r\f\v]+?(.+?)[\n\r\f\v]+?(.+?)[\n\r\f\v]'
    for path in extensions:
        url = baseURL + path
        data = requests.get(url)
        match = re.search(pattern, data.text)
        if match:
            tle1 = match.group(1).strip()
            tle2 = match.group(2).strip()
            return (target, str(tle1), str(tle2))
        else:
            continue


def dms_to_deg(dms):
    """
    Calculate degrees using degrees, minutes, seconds
    :param dms: Satellite coordinates in format 'degrees:minutes:seconds'
    :return: Satellite coordinates in format 'degrees'
    """
    string = str(dms)                           # convert to str, because 'dms' has format 'ephem.Angle'
    degrees = string.split(":")
    degrees = abs(float(degrees[0])) + float(degrees[1]) / 60.0 + float(degrees[2]) / 3600.0
    degrees = round(degrees,3)
    if dms < 0:
        degrees *= -1
    return degrees
