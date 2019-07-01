import pandas as pd


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
    df = pd.DataFrame({
        'day': list_day,
        'time': list_time,
        'domain': list_domain,
        'port': list_port
    })
    df.to_csv(out_csv)
    print('saved to {}'.format(out_csv))


if __name__ == '__main__':
    log_file = './data/logs.txt'
    out_csv = './data/logs.csv'
    read_log_file(log_file, out_csv)

