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

data = [('谷歌', 84301),
        ('电信', 76497),
        ('阿里巴巴', 6031),
        ('联通', 4318),
        ('未知', 1408),
        ('阿里云', 1003),
        ('移动', 606),
        ('脸书', 323),
        ('亚马逊', 222),
        ('内网IP', 210),
        ('阿卡迈', 22),
        ('教育网', 18),
        ('层峰网络', 7),
        ('香港宽频', 7),
        ('沃达丰', 2),
        ('Hurricane-Electric', 1)]


@C.funcs
def pie_base() -> Pie:
    c = (
        Pie(init_opts=opts.InitOpts(width="800px", height="1200px"))
            .add("", data)
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", font_size=16))
    )
    return c


Page().add(*[fn() for fn, _ in C.charts]).render('./output/map_pie_operator.html')
