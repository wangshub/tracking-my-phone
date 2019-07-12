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

data = [(443, 145842),
        (53, 37725),
        (80, 47873),
        (53, 12649),
        (8080, 11255),
        (5228, 5581),
        (8081, 1881),
        (9900, 1576),
        (39620, 1321),
        (9800, 1068),
        (7006, 959),
        ('other', 12329)]


@C.funcs
def pie_base() -> Pie:
    c = (
        Pie()
            .add("", data)
            .set_global_opts(title_opts=opts.TitleOpts(title=""))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%", font_size=16))
    )
    return c


Page().add(*[fn() for fn, _ in C.charts]).render('./output/map_pie_ports.html')
