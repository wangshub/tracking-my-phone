# -*- coding: utf-8 -*-
import geoip2.database


class IpGeo:
    def __init__(self, db_file):
        self.reader = geoip2.database.Reader(db_file)

    def find(self, ip):
        result = {}
        try:
            data = self.reader.city(ip)
            result['country'] = data.country.name
            result['city'] = data.city.name
            result['longitude'] = data.location.longitude
            result['latitude'] = data.location.latitude
        except Exception as err:
            print('no ip info, '+str(err))
        return result


if __name__ == '__main__':
    ipgeo = IpGeo('./geo/GeoLite2-City.mmdb')
    result = ipgeo.find('121.35.100.100')
    print(result)



