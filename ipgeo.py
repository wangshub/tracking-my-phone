# -*- coding:utf-8 -*-
from ip2Region import Ip2Region
import socket
import time


def domain_to_ip(domain):
    # print('parsing {}'.format(domain))
    return socket.gethostbyname(domain)


class IpGeo:
    def __init__(self, db_file):
        self.searcher = Ip2Region(db_file)

    def find(self, ip):
        result = {}
        try:
            if not self.searcher.isip(ip):
                ip = domain_to_ip(ip)

            data = self.searcher.btreeSearch(ip)
            loc = data["region"].decode('utf-8').split('|')
            result['ip'] = ip
            result['city_id'] = data["city_id"]
            result['country'] = loc[0]
            result['province'] = loc[2]
            result['city'] = loc[3]
            result['operator'] = loc[4]
        except Exception as err:
            print(err, ip)
        return result

    def close(self):
        self.searcher.close()


if __name__ == '__main__':
    ipgeo = IpGeo('./geo/ip2region.db')
    result = ipgeo.find('www.baidu.com')
    print(result)
    ipgeo.close()
