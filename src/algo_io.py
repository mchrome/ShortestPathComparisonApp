from shapely.geometry import Point, LineString
import geopandas as gpd
from math import radians, sin, cos, asin, sqrt
import matplotlib.pyplot as plt


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))


class AlgoIO:

    def __init__(self, algorithm, input_path="input.txt", output_path="output.txt"):
        self.input_path = input_path
        self.output_path = output_path
        self.execution_time = None
        self.preprocessing_time = None
        self.ctov = None
        self.vtoc = None
        self.etols = None
        self.st = None
        self.end = None
        self.algorithm = algorithm

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

        ans = []
        checked = []
        landmarks = []
        print("first")
        with open(self.output_path, 'r') as f:
            ans_size = f.readline()
            for i in range(int(ans_size) - 1):
                edge = tuple(map(int, f.readline().split()))
                ans.append(edge)
            checked_size = f.readline()
            for i in range(int(checked_size)):
                edge = tuple(map(int, f.readline().split()))
                checked.append(edge)
            self.execution_time = float(f.readline())
            if self.algorithm == "alt":
                landmark_size = f.readline()
                #print(landmark_size)
                for i in range(int(landmark_size)):
                    landmarks.append(self.vtoc[int(f.readline())])
                #print(landmarks)
                self.preprocessing_time = float(f.readline())

        print("second")
        geometry_shortest_path = [self.etols[xy] for xy in ans]
        gdf_shortest_path = self.get_mercator_gdf(geometry_shortest_path)
        geometry_checked = [self.etols[xy] for xy in checked]
        gdf_checked = self.get_mercator_gdf(geometry_checked)
        gdf_st = self.get_mercator_gdf([Point(self.st[0], self.st[1])])
        gdf_end = self.get_mercator_gdf([Point(self.end[0], self.end[1])])
        if self.algorithm == "alt":
            gdf_landmarks = self.get_mercator_gdf(geometry=landmarks)

        gdf = self.get_mercator_gdf(base_gdf.geometry)

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        print(len(gdf_checked))
        print(len(gdf_shortest_path))
        base = gdf.plot(ax=ax, linewidth=0.5)
        ax.margins(0)
        ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
        checked = gdf_checked.plot(ax=base, color='black', linewidth=0.5)
        fig = gdf_shortest_path.plot(ax=checked, color='red', linewidth=0.8)
        fig = gdf_st.plot(ax=fig, color='brown')
        fig = gdf_end.plot(ax=fig, color='green')
        print("last")
        if self.algorithm == "alt":
            fig = gdf_landmarks.plot(ax=fig, color='gold')

        return fig.get_figure()

    def get_mercator_gdf(self, geometry):
        gdf = gpd.GeoDataFrame(geometry=geometry)
        gdf.crs = {"init": "epsg:4326"}
        gdf = gdf.to_crs(epsg=3857)
        return gdf