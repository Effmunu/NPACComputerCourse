#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import numpy as np
from astropy import wcs

def dms(angle):
    """
    Convert a floating point angle into textual representation Degree:Minute:Second (-> DEC coordinate)
    :param angle: floating point value
    :return: Degree:Minute:Second
    """
    d = int(angle)
    m = (angle - d) * 60.0
    s = (m - int(m)) * 60.0
    return '[%d:%d:%f]' % (int(d), int(m), s)


def hms(angle):
    """
    Convert a floating point angle into textual representation Hour:Minute:Second (-> RA coordinate)
    :param angle: floating point value
    :return: Hour:Minute:Second
    """
    """  """
    hour = angle*24.0/360.0
    h = int(hour)
    m = (hour - h) * 60.0
    s = (m - int(m)) * 60.0
    return '[%d:%d:%f]' % (int(h), int(m), s)


def radec(coord):
    """
    Convert a floating point array of coordinates into textual representation Hour:Minute:Second (-> RA/DEC coordinates)
    :param coord: array of coordinates [RA, DEC]
    :return: text
    """
    return 'RA=%s DEC=%s' % (hms(coord[0]), dms(coord[1]))


class WCS:
    def __init__(self, header):
        """ Parse the WCS keywords from the primary HDU of an FITS image """

        # header = read_header(image)
        self.wcs = wcs.WCS(header)

    def convert_to_radec(self, x, y):
        pixel = np.array([[x, y],], np.float_)
        sky = self.wcs.wcs_pix2world(pixel, 0)
        ra, dec = sky[0]
        return ra, dec

    def convert_to_xy(self, ra, dec):
        pixel = np.array([[ra, dec],], np.float_)
        sky = self.wcs.wcs_world2pix(pixel, 0)
        x, y = sky[0]
        return x, y


def get_objects(ra, dec, radius):
    """
    Request from the Simbad server a list of astro objects at the RA DEC position, within the specified acceptance cone
    :param ra: the RA floating point coordinate
    :param dec: the DEC floating point coordinate
    :param radius: the acceptance angle in degree
    :return: a dictionary of identified objects {objectname: objecttype}
    """

    def make_req(ra, dec, radius):
        """
        Build a request tu the Simbad server
        :param ra: floating point value of the RA coordinate
        :param dec: floating point value of the DEC coordinate
        :param radius: floting value of the acceptance radius (degrees)
        :return: request text
        """
        def crep (s, c):
            s = s.replace(c, '%%%02X' % ord(c))
            return s

        host_simbad = 'simbad.u-strasbg.fr'
        port = 80

        # WGET with the "request" string built as below :

        script = ''
        # output format (for what comes from SIMBAD)
        script += 'format object f1 "'
        script += '%COO(A)'            # hour:minute:second
        script += '\t%COO(D)'          # degree:arcmin:arcsec
        script += '\t%OTYPE(S)'
        script += '\t%IDLIST(1)'
        script += '"\n'

        script += 'query coo '
        script += '%f' % ra           # append "a_ra" (decimal degree)
        script += ' '
        script += '%f' % dec          # append "a_dec" (decimal degree)
        script += ' radius='
        script += '%f' % radius       # append "a_radius" (decimal degree)
        script += 'd'                  # d,m,s
        script += ' frame=FK5 epoch=J2000 equinox=2000' # fk5
        script += '\n'

        # "special characters" converted to "%02X" format :
        script = crep(script, '%')
        script = crep(script, '+')
        script = crep(script, '=')
        script = crep(script, ';')
        script = crep(script, '"')
        script = crep(script, ' ')                # same as upper line.

        script = script.replace('\n','%0D%0A')    # CR+LF
        script = crep(script, '\t')

        request = 'http://' + host_simbad + '/simbad/sim-script?'
        request += 'script=' + script + '&'

        return request

    def wget(req):

        def send(url):
            retry = 0
            while retry < 10:
                try:
                    req = urllib2.urlopen(url)

                    try:
                        # resp = opener.open(req)
                        s = req.read()
                        lines = s.split('<BR>\n')
                        return lines[0]
                    except Exception, e:
                        print 'cannot read'
                    except:
                        raise

                except urllib2.HTTPError as e:

                    retry += 1
                    sleep(0.2)
                    # print 'url=[%s]' % url
                    # print e.fp.read()
                except:
                    raise
            print retry

        out = send(req)

        return out

    req = make_req(ra, dec, radius)
    out = wget(req)
    out = out.split('\n')
    in_data = False

    objects = dict()

    for line in out:
        line = line.strip()
        if line == '': continue
        if not in_data:
            if line == '::data::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::':
                in_data = True
            continue

        data = line.split('\t')

        objects[data[3].strip()] = data[2].strip()

    return objects

