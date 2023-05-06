import argparse
import geojson
import pyproj


def main(args):
    # Load geojson
    with open(args.in_filename) as f:
        gj = geojson.load(f)

    if gj.type == 'FeatureCollection':
        print(f'Loaded "{gj.type}" with {len(gj.features)} features.')
    else:
        raise ValueError(f'Only GeoJSON containing a "FeatureCollection" is supported at this time: {gj.type} given.')

    # Load source CRS from GeoJSON
    source_crs = pyproj.CRS.from_string(gj.crs['properties']['name'])
    print(f'Found source projection definition in given GeoJSON: {source_crs}')

    # Validate given target CRS
    try:
        target_crs = pyproj.CRS.from_user_input(args.projection)
    except pyproj.exceptions.CRSError as e:
        raise ValueError(f'Invalid value for argument "projection": {e}')
    print(f'Target projection given: {target_crs}')

    # Prepare transformer
    print(f'Reprojecting {len(gj.features)} features {source_crs.to_string()} -> {target_crs.to_string()}...')
    tf = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)

    new_features = []
    for feature in gj.features:
        if feature.geometry.type == 'Point':
            # Transform coordinates
            new_coordinates = tf.transform(*feature.geometry.coordinates)

            # Define new Point Feature
            new_point = geojson.Point(new_coordinates)
            new_feature = geojson.Feature(
                geometry=new_point,
                properties=feature.properties
            )
            new_features.append(new_feature)

        elif feature.geometry.type == 'MultiPolygon':
            # Transform coordinates
            new_polygons = []
            for polygon in feature.geometry.coordinates:
                new_linear_rings = []
                for linear_ring in polygon:
                    new_coordinates = []
                    for coordinate_pair in linear_ring:
                        new_coordinate_pair = tf.transform(*coordinate_pair)
                        new_coordinates.append(new_coordinate_pair)
                    new_linear_rings.append(new_coordinates)
                new_polygons.append(new_linear_rings)

            # Define new MultiPolygon Feature
            new_multipolygon = geojson.MultiPolygon(new_polygons)
            new_feature = geojson.Feature(
                geometry=new_multipolygon,
                properties=feature.properties,
            )
            new_features.append(new_feature)

        else:
            # TODO: implement support for more Geometry types
            print(f'Warning: This tool currently does not support "{feature.geometry.type}s".')
            continue

    # Create new feature collection
    new_feature_collection = geojson.FeatureCollection(
        features=new_features,
        crs={
            'type': 'name',
            'properties': {
                'name': f'urn:ogc:def:crs:{"::".join(target_crs.to_authority())}'
            }
        }
    )

    print(f'Successfully reprojected {len(new_features)} features. Writing to file...')

    # Write output to file with filename given
    with open(args.out_filename, 'w') as o:
        geojson.dump(new_feature_collection, o)

    print(f'Reprojected FeatureCollection written to "{args.out_filename}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='reproject',
        description='Reproject GeoJSON files.'
    )

    parser.add_argument('in_filename', help='Name of the GeoJSON file to read features from and reproject.')
    parser.add_argument('out_filename', help='Name of the GeoJSON file to write the repojrect features to.')
    parser.add_argument('projection', help='EPSG code of target projection.')

    args = parser.parse_args()
    main(args)
