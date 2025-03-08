import numpy as np
import cv2
from tqdm import tqdm

from shapely.geometry import shape
import geopandas as gpd

def get_name_and_color(id):
    """
        Get name and color for GeoJSON based on predicted id

        :param id: Specific id of predicted class
        :return: Return name and color of class based on id
    """
    classes_to_idx = [
        "positive",
        "negative",
        "other"
    ]
    colors_to_idx = [
        [235, 64, 52],
        [235, 223, 52],
        [52, 235, 61]
    ]
    return classes_to_idx[id], colors_to_idx[id]


def from_npy_to_geojson(npy_mask):
    
    mask = npy_mask
    mask = mask.astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    geojson_cells_classes = []

    for contour in tqdm(contours):

        if len(contour) < 3:
            continue

        # Get class of cell
        cell_class = mask[contour[0][0][1], contour[0][0][0]]

        # Save class to GeoJSON structure
        contour = np.squeeze(contour)
        polygon_coords = [contour.tolist()]
        polygon = shape({'type': 'Polygon', 'coordinates': polygon_coords})

        name, color = get_name_and_color(cell_class-1)
        meta_data_cell_img = {'name': name, 'color': color}

        # Create GeoJSON feature with properties
        predicted_cell_class = {'type': 'Feature',
                                'geometry': polygon,
                                'properties': {'objectType': 'annotation', 'classification': meta_data_cell_img}}

        # Check cell validation TODO

        geojson_cells_classes.append(predicted_cell_class)

    gdf_classes = gpd.GeoDataFrame.from_features(geojson_cells_classes)
    # gdf_classes.to_file(f'{output_path}', driver='GeoJSON')
    return gdf_classes


