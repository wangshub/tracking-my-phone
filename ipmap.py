from pyecharts import options as opts
from pyecharts.charts import Geo, Page, Map
from pyecharts.globals import ChartType, SymbolType


class Collector:
    charts = []

    @staticmethod
    def funcs(fn):
        Collector.charts.append((fn, fn.__name__))


C = Collector()


@C.funcs
def geo_lines() -> Geo:
    c = (
        Geo()
            .add_schema(maptype="china")
            .add(
            "",
            [("广州", 55), ("北京", 66), ("杭州", 77), ("重庆", 88), ("成都", 99)],
            type_=ChartType.EFFECT_SCATTER,
            color="blue",
        )
            .add(
            "geo",
            [("广州", "上海市"), ("广州", "北京"), ("广州", "杭州"), ("广州", "重庆"), ("广州", "成都")],
            type_=ChartType.LINES,
            effect_opts=opts.EffectOpts(
                symbol=SymbolType.ARROW, symbol_size=6, color="blue"
            ),
            linestyle_opts=opts.LineStyleOpts(curve=0.2, opacity=0.2, width=0.5),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Lines"))
    )
    return c


@C.funcs
def map_visualmap() -> Map:
    c = (
        Map()
        .add("商家A", [list(z) for z in zip(['四川'], [80])], "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-VisualMap（分段型）"),
            visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True),
        )
    )
    return c


Page().add(*[fn() for fn, _ in C.charts]).render('./output/render.html')
