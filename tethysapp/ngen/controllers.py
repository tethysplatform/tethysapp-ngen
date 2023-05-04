from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import Ngen as app

@controller(name="home")
class NgenMap(MapLayout):
    app = app
    base_template = 'ngen/base.html'
    map_title = 'Next Generation'
    map_subtitle = 'Water Model'
    basemaps = [
        'OpenStreetMap',
        'ESRI',
        'Stamen',
    ]
    default_map_extent = [-65.69, 23.81, -129.17, 49.38]  # CONUS bbox
    max_zoom = 16
    min_zoom = 2
