import pandas as pd
import numpy as np

from pyecharts import options as opts
from pyecharts.charts import Geo, Page, Map, Pie, Bar
from pyecharts.globals import ChartType, SymbolType


class Collector:
    charts = []

    @staticmethod
    def funcs(fn):
        Collector.charts.append((fn, fn.__name__))


C = Collector()

data = [('googleapis.com', 79979),
        ('qq.com', 25716),
        ('bilibili.com', 11771),
        ('qpic.cn', 5735),
        ('google.com', 5207),
        ('amap.com', 3749),
        ('hdslb.com', 3693),
        ('zhihu.com', 2994),
        ('163.com', 2042),
        ('sogou.com', 1952),
        ('alipay.com', 1364),
        ('snssdk.com', 1317),
        ('meituan.com', 1298),
        ('p2cdn.com', 1287),
        ('baidu.com', 1274),
        ('other', 25598)]

data.reverse()


@C.funcs
def pie_base() -> Pie:
    c = (
        Pie()
            .add("", data)
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", font_size=18))
    )
    return c


@C.funcs
def bar_base() -> Bar:
    c = (
        Bar(init_opts=opts.InitOpts(width="100%", height="800%"))
        .add_xaxis(xaxis_data=[x[0] for x in data])
        .add_yaxis(series_name="公司",
                   color='#59a2a7',
                   yaxis_data=[x[1] for x in data])
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))

    )
    return c


Page().add(*[fn() for fn, _ in C.charts]).render('./output/map_bar_company.html')
