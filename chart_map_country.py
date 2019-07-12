import pandas as pd
import numpy as np

from pyecharts import options as opts
from pyecharts.charts import Geo, Page, Map, Pie

data = [('China', 188080),
        ('United States', 86471),
        ('Others', 4041),
        ('Ireland', 366),
        ('Sweden', 262),
        ('Chile', 253),
        ('Belgium', 243),
        ('Singapore', 101),
        ('Canada', 72),
        ('Germany', 68),
        ('India', 54),
        ('Japan', 44),
        ('New Zealand', 2),
        ('Poland', 2)]

data_zh = [('中国', 188080),
           ('美国', 86471),
           ('未知', 4041),
           ('爱尔兰', 366),
           ('瑞典', 262),
           ('智利', 253),
           ('比利时', 243),
           ('新加坡', 101),
           ('加拿大', 72),
           ('德国', 68),
           ('印度', 54),
           ('日本', 44),
           ('新西兰', 2),
           ('波兰', 2)]


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
            .add("全球分布", data, "world")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-世界地图"),
            visualmap_opts=opts.VisualMapOpts(max_=200000),
        )
    )
    return c


@C.funcs
def bar_base() -> Pie:
    c = (
        Pie(init_opts=opts.InitOpts(width="1000px", height="900px"))
            .add(
            series_name="国家分布",
            data_pair=data_zh,
            radius=["50%", "70%"],
            label_opts=opts.LabelOpts(is_show=True, position="layoutCenter"),
            )
            .set_global_opts(legend_opts=opts.LegendOpts(pos_left="legft", orient="vertical"))
            .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(formatter="{b}: {c}", font_size=18)
            )
    )

    return c


Page().add(*[fn() for fn, _ in C.charts]).render('./output/global_country.html')
