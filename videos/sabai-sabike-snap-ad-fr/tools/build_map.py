"""Build the Phuket map SVG paths from the GSHHG full-resolution shoreline (LGPL).

Input: polygons extracted from basemap-data-hires (gshhs_f.dat) around Phuket,
as [{"level": 1, "pts": [[lon, lat], ...]}, ...].
Usage: python3 tools/build_map.py <gshhs_phuket.json> <out.json>
Coordinates are projected into "card space" (CARD_W x CARD_H) at the full-island view.
"""
import json, math, sys
from shapely.geometry import Polygon, box
from shapely.ops import transform, unary_union

CARD_W, CARD_H = 940, 1240
N, S = 8.215, 7.745                     # full-island latitude window
LAT0 = (N + S) / 2
PX_LAT = CARD_H / (N - S)
PX_LON = PX_LAT * math.cos(math.radians(LAT0))
LON_C = 98.335
W = LON_C - CARD_W / 2 / PX_LON
E = LON_C + CARD_W / 2 / PX_LON

def proj(lon, lat):
    return ((lon - W) * PX_LON, (N - lat) * PX_LAT)

frame = box(W - 0.02, S - 0.02, E + 0.02, N + 0.02)
parts = []
for rec in json.load(open(sys.argv[1])):
    poly = Polygon(rec["pts"])
    if not poly.is_valid:
        poly = poly.buffer(0)
    parts.append(poly.intersection(frame))
# GSHHG full resolution is a ~200m grid: drop the staircase, then round the corners
land = unary_union(parts).simplify(0.0012)
land = transform(lambda x, y, z=None: proj(x, y), land)

def chaikin(pts, n=3):
    for _ in range(n):
        out = []
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            out += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        pts = out
    return pts

def ring_d(coords):
    pts = chaikin(list(coords)[:-1])
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"

d = []
polys = [land] if land.geom_type == "Polygon" else list(land.geoms)
for p in polys:
    if p.area < 6:  # drop specks under ~2x2 px at full view
        continue
    d.append(ring_d(p.exterior.coords))
    for hole in p.interiors:
        d.append(ring_d(hole.coords))

places = {
    "patong": (98.2990, 7.8930),
    "karon": (98.2985, 7.8465),
    "kata": (98.3000, 7.8200),
    "town": (98.3880, 7.8850),
    "airport": (98.3090, 8.1120),
}
# indicative Patong -> Karon road (Route 4233 over the hill), not survey data
route = [(98.2990, 7.8930), (98.2972, 7.8860), (98.2958, 7.8800), (98.2975, 7.8745),
         (98.3005, 7.8690), (98.3010, 7.8625), (98.2990, 7.8560), (98.2985, 7.8465)]

out = {
    "card": [CARD_W, CARD_H],
    "land": " ".join(d),
    "places": {k: proj(*v) for k, v in places.items()},
    "route": [proj(*p) for p in route],
}
json.dump(out, open(sys.argv[2], "w"))
print(len(d), "rings,", sum(len(x) for x in d) // 1000, "KB path")
