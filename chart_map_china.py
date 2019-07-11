import pandas as pd
import numpy as np

from pyecharts import options as opts
from pyecharts.charts import Geo, Page, Map, Pie
from pyecharts.globals import ChartType, SymbolType


data = [('广东', 54558),
        ('台湾', 49564),
        ('上海', 37677),
        ('北京', 14690),
        ('浙江', 9062),
        ('江苏', 4226),
        ('河北', 4216),
        ('天津', 4017),
        ('福建', 2358),
        ('香港', 1667),
        ('山东', 1427),
        ('江西', 1119),
        ('湖南', 863),
        ('河南', 847),
        ('湖北', 377),
        ('黑龙江', 341),
        ('海南', 226),
        ('四川', 101),
        ('山西', 38),
        ('安徽', 36),
        ('辽宁', 34),
        ('陕西', 32),
        ('贵州', 28),
        ('吉林', 27),
        ('重庆', 1)]


class Collector:
    charts = []

    @staticmethod
    def funcs(fn):
        Collector.charts.append((fn, fn.__name__))


C = Collector()


@C.funcs
def map_world() -> Map:
    c = (
        Map()
            .add("中国省份分布", data, "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-VisualMap（连续型）"),
            visualmap_opts=opts.VisualMapOpts(max_=54558),
        )
    )
    return c


Page().add(*[fn() for fn, _ in C.charts]).render('./output/map_china_province.html')

