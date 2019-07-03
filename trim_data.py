import pandas as pd
from ipgeo import IpGeo


def read_log_file(fname, out_csv):
    str_flag = 'connect to'
    print('reading raw text {}'.format(fname))
    with open(fname, 'r') as fp:
        text = fp.readlines()

    content = [x.strip() for x in text]
    filterd_lines = list(filter(lambda x: str_flag in x, content))
    print('found {} connect to requests in total'.format(len(filterd_lines)))
    filterd_lines = list(map(lambda x: x.split(' '), filterd_lines))

    list_day = list(map(lambda x: x[1], filterd_lines))
    list_time = list(map(lambda x: x[2], filterd_lines))
    list_url = list(map(lambda x: x[7], filterd_lines))
    list_domain = list(map(lambda x: x.split(':')[0], list_url))
    list_port = list(map(lambda x: x.split(':')[1], list_url))

    ipgeo = IpGeo('./geo/ip2region.db')

    list_ipgeo = list(map(lambda x: ipgeo.find(x), list_domain))
    list_ip4 = list(map(lambda x: x.get('ip'), list_ipgeo))
    list_city_id = list(map(lambda x: x.get('city_id'), list_ipgeo))
    list_country = list(map(lambda x: x.get('country'), list_ipgeo))
    list_province = list(map(lambda x: x.get('province'), list_ipgeo))
    list_city = list(map(lambda x: x.get('city'), list_ipgeo))
    list_operator = list(map(lambda x: x.get('operator'), list_ipgeo))

    df = pd.DataFrame({
        'day': list_day,
        'time': list_time,
        'domain': list_domain,
        'ip': list_ip4,
        'port': list_port,
        'city_id': list_city_id,
        'country': list_country,
        'province': list_province,
        'city': list_city,
        'operator': list_operator
    })
    df.to_csv(out_csv, index=False)
    print('saved to {}'.format(out_csv))


if __name__ == '__main__':
    log_file = './data/logs.txt'
    out_csv = './data/logs.csv'
    read_log_file(log_file, out_csv)

