import json
from pathlib import Path
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
    default_map_extent = [-111.677812, 40.244400,-110.892191, 40.712003]
    max_zoom = 16
    min_zoom = 8

    def compose_layers(self, request, map_view, *args, **kwargs):
        """
        Add layers to the MapLayout and create associated layer group objects.
        """
        # Load GeoJSON from files
        data_directory = Path(__file__).parent / 'data'
        config_dir = data_directory / 'AWI_001' / 'config'
        
        # Nexus Points
        nexus_path = config_dir / 'nexus_reprojected.geojson'
        with open(nexus_path) as nf:
            nexus_geojson = json.loads(nf.read())

        nexus_layer = self.build_geojson_layer(
            geojson=nexus_geojson,
            layer_name='nexus',
            layer_title='Nexus',
            layer_variable='nexus',
            visible=True,
        )

        # Catchments
        catchments_path = config_dir / 'catchments_reprojected.geojson'
        with open (catchments_path) as cf:
            catchments_geojson = json.loads(cf.read())

        catchments_layer = self.build_geojson_layer(
            geojson=catchments_geojson,
            layer_name='catchments',
            layer_title='Catchments',
            layer_variable='catchments',
            visible=True,
        )

        # Create layer groups
        layer_groups = [
            self.build_layer_group(
                id='ngen-features',
                display_name='NGen Features',
                layer_control='checkbox',  #  'checkbox' or 'radio'
                layers=[
                    nexus_layer,
                    catchments_layer,
                ]
            )
        ]

        return layer_groups

    @classmethod
    def get_vector_style_map(cls):
        return {
            'Point': {'ol.style.Style': {
                'image': {'ol.style.Circle': {
                    'radius': 5,
                    'fill': {'ol.style.Fill': {
                        'color': 'white',
                    }},
                    'stroke': {'ol.style.Stroke': {
                        'color': 'red',
                        'width': 3
                    }}
                }}
            }},
            'MultiPolygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'navy',
                    'width': 3
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 25, 128, 0.1)'
                }}
            }},
        }
