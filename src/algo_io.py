from shapely.geometry import Point, LineString
import geopandas as gpd
from math import radians, sin, cos, asin, sqrt
import matplotlib.pyplot as plt
from output_format import OutputFormatItem

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))


class AlgoIO:

    def __init__(self, out_format: list[OutputFormatItem], input_path, output_path):
        self.out_format = out_format
        self.input_path = input_path
        self.output_path = output_path
        self.execution_time = None
        self.preprocessing_time = None
        self.ctov = None
        self.vtoc = None
        self.etols = None
        self.st = None
        self.end = None

    def gdf_to_input(self, gdf, st, end):
        self.ctov = dict()
        self.vtoc = dict()
        self.etols = dict()
        self.st = st
        self.end = end
        v = []
        e = []

        for i, linestring in enumerate(gdf['geometry']):
            x, y = linestring.coords.xy

            prev = None

            for x, y in zip(x, y):

                if (x, y) not in self.ctov:
                    self.ctov[(x, y)] = len(v)
                    self.vtoc[len(v)] = Point(x, y)
                    v.append((x, y))

                if prev == None:
                    prev = (x, y)

                    continue

                road_length = haversine(prev[0], prev[1], x, y)
                e.append((self.ctov[prev], self.ctov[(x, y)], road_length))

                self.etols[(e[-1][0], e[-1][1])] = LineString([Point(prev[0], prev[1]), Point(x, y)])
                self.etols[(e[-1][1], e[-1][0])] = LineString([Point(prev[0], prev[1]), Point(x, y)])

                prev = (x, y)

        self.write_to_file(v, e, st, end)

    def write_to_file(self, v, e, st, end):
        with open(self.input_path, 'w') as f:
            f.write(f'{len(v)} {len(e)} {st[0]} {st[1]} {end[0]} {end[1]} \n')
            for edge in e:
                f.write(f'{edge[0]} {edge[1]} {edge[2]}\n')
            for vertex in v:
                f.write(f'{vertex[0]} {vertex[1]}\n')

    def get_result_fig(self, base_gdf):

        output = []

        with open(self.output_path, 'r') as f:
            for out_form in self.out_format:
                if out_form.type == "Вершины":
                    vertex_count = int(f.readline())
                    verticies = []
                    for i in range(vertex_count):
                        verticies.append(self.vtoc[int(f.readline())])
                    output.append((verticies, out_form.color))
                if out_form.type == "Дуги":
                    edge_count = int(f.readline())
                    edges = []
                    for i in range(edge_count-1): ###########################################################################################
                        edge = tuple(map(int, f.readline().split()))
                        edges.append(self.etols[edge])
                    output.append((edges, out_form.color))

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        gdf = self.get_mercator_gdf(base_gdf.geometry)
        fig = gdf.plot(ax=ax, linewidth=0.5)
        ax.margins(0)
        ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)

        for out in output:
            gdf = self.get_mercator_gdf(out[0])
            fig = gdf.plot(ax=fig, color=out[1], linewidth=0.8)

        gdf_st = self.get_mercator_gdf([Point(self.st[0], self.st[1])])
        gdf_end = self.get_mercator_gdf([Point(self.end[0], self.end[1])])

        fig = gdf_st.plot(ax=fig, color='brown')
        fig = gdf_end.plot(ax=fig, color='green')


        return fig.get_figure()

    def get_mercator_gdf(self, geometry):
        gdf = gpd.GeoDataFrame(geometry=geometry)
        gdf.crs = {"init": "epsg:4326"}
        gdf = gdf.to_crs(epsg=3857)
        return gdf