"""Main module."""

import string
import random
import ipyleaflet 
import pandas
import geopandas
import openpyxl
import folium 
import os
import geemap
import folium.plugins as plugins
from box import Box 
from geemap import xyz_to_folium
from geemap import vector_to_geojson 

basemaps = Box(xyz_to_folium(), frozen_box=True)

class Map(ipyleaflet.Map):
        def __init__(self, **kwargs):
            # Default map center location and zoom level
            latlon = [20, 0]
            zoom = 2

            # Interchangeable parameters between ipyleaflet and folium
            if "center" in kwargs:
                kwargs["location"] = kwargs["center"]
                kwargs.pop("center")
            if "location" in kwargs:
                latlon = kwargs["location"]
            else:
                kwargs["location"] = latlon

            if "zoom" in kwargs:
                kwargs["zoom_start"] = kwargs["zoom"]
                kwargs.pop("zoom")
            if "zoom_start" in kwargs:
                zoom = kwargs["zoom_start"]
            else:
                kwargs["zoom_start"] = zoom
            if "max_zoom" not in kwargs:
                kwargs["max_zoom"] = 24

            if "scale_control" not in kwargs:
                kwargs["scale_control"] = True

            if kwargs["scale_control"]:
                kwargs["control_scale"] = True
                kwargs.pop("scale_control")

            # if "control_scale" not in kwargs:
            #     kwargs["control_scale"] = True

            if "draw_export" not in kwargs:
                kwargs["draw_export"] = False

            if "height" in kwargs and isinstance(kwargs["height"], str):
                kwargs["height"] = float(kwargs["height"].replace("px", ""))

            if (
                "width" in kwargs
                and isinstance(kwargs["width"], str)
                and ("%" not in kwargs["width"])
            ):
                kwargs["width"] = float(kwargs["width"].replace("px", ""))

            height = None
            width = None

            if "height" in kwargs:
                height = kwargs.pop("height")
            else:
                height = 600

            if "width" in kwargs:
                width = kwargs.pop("width")
            else:
                width = "100%"

            super().__init__(**kwargs)
            self.baseclass = "folium"

            if (height is not None) or (width is not None):
                f = folium.Figure(width=width, height=height)
                self.add_to(f)

            if "fullscreen_control" not in kwargs:
                kwargs["fullscreen_control"] = True
            if kwargs["fullscreen_control"]:
                plugins.Fullscreen().add_to(self)

            if "draw_control" not in kwargs:
                kwargs["draw_control"] = True
            if kwargs["draw_control"]:
                plugins.Draw(export=kwargs.get("draw_export")).add_to(self)

            if "measure_control" not in kwargs:
                kwargs["measure_control"] = True
            if kwargs["measure_control"]:
                plugins.MeasureControl(position="bottomleft").add_to(self)

            if "latlon_control" not in kwargs:
                kwargs["latlon_control"] = False
            if kwargs["latlon_control"]:
                folium.LatLngPopup().add_to(self)

            if "locate_control" not in kwargs:
                kwargs["locate_control"] = False
            if kwargs["locate_control"]:
                plugins.LocateControl().add_to(self)

            if "minimap_control" not in kwargs:
                kwargs["minimap_control"] = False
            if kwargs["minimap_control"]:
                plugins.MiniMap().add_to(self)

            if "search_control" not in kwargs:
                kwargs["search_control"] = True
            if kwargs["search_control"]:
                plugins.Geocoder(collapsed=True, position="topleft").add_to(self)

            if "google_map" not in kwargs:
                pass
            elif kwargs["google_map"] is not None:
                if kwargs["google_map"].upper() == "ROADMAP":
                    layer = basemaps["ROADMAP"]
                elif kwargs["google_map"].upper() == "HYBRID":
                    layer = basemaps["HYBRID"]
                elif kwargs["google_map"].upper() == "TERRAIN":
                    layer = basemaps["TERRAIN"]
                elif kwargs["google_map"].upper() == "SATELLITE":
                    layer = basemaps["SATELLITE"]
                else:
                    print(
                        f'{kwargs["google_map"]} is invalid. google_map must be one of: ["ROADMAP", "HYBRID", "TERRAIN", "SATELLITE"]. Adding the default ROADMAP.'
                    )
                    layer = basemaps["ROADMAP"]
                layer.add_to(self)

            if "layers_control" not in kwargs:
                self.options["layersControl"] = True
            else:
                self.options["layersControl"] = kwargs["layers_control"]

            self.fit_bounds([latlon, latlon], max_zoom=zoom)

        def add_search_control(self, position="topleft", **kwargs):
            """Adds a search control to the map.

            Args:
                self: The map.
                position (str, optional): The position of the search control. Defaults to "topleft".
                kwargs: Keyword arguments to pass to the search control.

            Returns:
                ipyleaflet.SearchControl: The search control.
            """
            if "url" not in kwargs:
                kwargs["url"] = 'https://nominatim.openstreetmap.org/search?format=json&q={s}'
    

            search_control = ipyleaflet.SearchControl(position=position, **kwargs)
            self.add_control(search_control)

        def add_draw_control(self, **kwargs):
            """Adds a draw control to the map.

            Args:
                self: The map.
                kwargs: Keyword arguments to pass to the draw control.

            Returns:
                ipyleaflet.DrawControl: The draw control.
            """
            draw_control = ipyleaflet.DrawControl(**kwargs)

            draw_control.polyline =  {
                "shapeOptions": {
                    "color": "#6bc2e5",
                    "weight": 8,
                    "opacity": 1.0
                }
            }
            draw_control.polygon = {
                "shapeOptions": {
                    "fillColor": "#6be5c3",
                    "color": "#6be5c3",
                    "fillOpacity": 1.0
                },
                "drawError": {
                    "color": "#dd253b",
                    "message": "Oops!"
                },
                "allowIntersection": False
            }
            draw_control.circle = {
                "shapeOptions": {
                    "fillColor": "#efed69",
                    "color": "#efed69",
                    "fillOpacity": 1.0
                }
            }
            draw_control.rectangle = {
                "shapeOptions": {
                    "fillColor": "#fca45d",
                    "color": "#fca45d",
                    "fillOpacity": 1.0
                }
            }

            self.add_control(draw_control)
  
        def add_layers_control(self, position="topright"):
            """Adds a layers control to the map.

            Args:
                self: The map.
                position (str, optional): The position of the layers control. Defaults to "topright".

            Returns:
                ipyleaflet.LayersControl: The layers control.
            """
            layers_control = ipyleaflet.LayersControl(position=position)
            self.add_control(layers_control)

        def add_fullscreen_control(self, position="topleft"):
            """Adds a fullscreen control to the map.

            Args:
                self: The map.
                position (str, optional): The position of the fullscreen control. Defaults to "topleft".

            Returns:
                ipyleaflet.FullScreenControl: The fullscreen control.
            """
            fullscreen_control = ipyleaflet.FullScreenControl(position=position)
            self.add_control(fullscreen_control)

        def add_tile_layer(self, url, name, attribution="", **kwargs):
            """Adds a tile layer to the map.

            Args:
                self: The map.
                url (str): The URL template of the tile layer.
                attribution (str): The attribution of the tile layer.
                name (str, optional): The name of the tile layer. Defaults to "OpenStreetMap".
                kwargs: Keyword arguments to pass to the tile layer.

            Returns:
                ipyleaflet.TileLayer: The tile layer.
            """
            tile_layer = ipyleaflet.TileLayer(url=url, attribution=attribution, name=name, **kwargs)
            self.add_layer(tile_layer)

        def add_basemap(self, basemap="HYBRID", show=True, **kwargs):
            """Adds a basemap to the map.

            Args:
                basemap (str, optional): Can be one of string from ee_basemaps. Defaults to 'HYBRID'.
                show (bool, optional): Whether to show the basemap. Defaults to True.
                **kwargs: Additional keyword arguments to pass to folium.TileLayer.

            Returns:
                ipyleaflet.BasemapLayer: The basemap layer.
            """
            import xyzservices 

            try:
                if isinstance(basemap, xyzservices.TileProvider):
                    name = basemap.name
                    url = basemap.build_url()
                    attribution = basemap.attribution
                    if "max_zoom" in basemap.keys():
                        max_zoom = basemap["max_zoom"]
                    else:
                        max_zoom = 22
                    layer = ipyleaflet.TileLayer(
                        tiles=url,
                        attr=attribution,
                        name=name,
                        max_zoom=max_zoom,
                        overlay=True,
                        control=True,
                        show=show,
                        **kwargs,
                    )

                    self.add_layer(layer)

            except Exception:
                raise Exception(
                    "Invalid basemap."
                )
    
        def add_geojson(self, data, **kwargs):
            """Adds a GeoJSON layer to the map.
            Args:
                self: The map.
                data (dict): The GeoJSON data.
                kwargs: Keyword arguments to pass to the GeoJSON layer.

            Returns:
                ipyleaflet.GeoJSON: The GeoJSON layer.
            """
            import json

            if isinstance(data, str):
                with open(data, "r") as f:
                    data = json.load(f)

            geojson = ipyleaflet.GeoJSON(data=data, **kwargs)
            self.add_layer(geojson)
            
        def add_shp(self, data, name='Shapefile', **kwargs):
            """Adds a shapefile to the map.

            Args:
                self: The map.
                data: The shapefile data.
                name (str, optional): The name of the shapefile layer. Defaults to "Shapefile".
                kwargs: Keyword arguments to pass to the shapefile layer.

            Returns:
                gdf.__geo_interface__: The shapefile layer.
            """
            import geopandas as gpd
        
            gdf = gpd.read_file(data)
            geojson = gdf.__geo_interface__
            self.add_geojson(geojson, name=name, **kwargs)

        def add_vector(
            self,
            filename,
            layer_name="Untitled",
            bbox=None,
            mask=None,
            rows=None,
            info_mode="on_hover",
            **kwargs,
        ):
            """Adds any geopandas-supported vector dataset to the map.

            Args:
                filename (str): Either the absolute or relative path to the file or URL to be opened, or any object with a read() method (such as an open file or StringIO).
                layer_name (str, optional): The layer name to use. Defaults to "Untitled".
                bbox (tuple | GeoDataFrame or GeoSeries | shapely Geometry, optional): Filter features by given bounding box, GeoSeries, GeoDataFrame or a shapely geometry. CRS mis-matches are resolved if given a GeoSeries or GeoDataFrame. Cannot be used with mask. Defaults to None.
                mask (dict | GeoDataFrame or GeoSeries | shapely Geometry, optional): Filter for features that intersect with the given dict-like geojson geometry, GeoSeries, GeoDataFrame or shapely geometry. CRS mis-matches are resolved if given a GeoSeries or GeoDataFrame. Cannot be used with bbox. Defaults to None.
                rows (int or slice, optional): Load in specific rows by passing an integer (first n rows) or a slice() object.. Defaults to None.
                info_mode (str, optional): Displays the attributes by either on_hover or on_click. Any value other than "on_hover" or "on_click" will be treated as None. Defaults to "on_hover".
            
            """
            if not filename.startswith("http"):
                filename = os.path.abspath(filename)

            ext = os.path.splitext(filename)[1].lower()
            if ext == ".shp":
                self.add_shp(filename, layer_name, **kwargs)
            elif ext in [".json", ".geojson"]:
                self.add_geojson(filename, layer_name, **kwargs)
            else:
                geojson = vector_to_geojson(
                    filename,
                    bbox=bbox,
                    mask=mask,
                    rows=rows,
                    epsg="4326",
                    **kwargs,
                )

                self.add_geojson(geojson, layer_name, info_mode=info_mode, **kwargs)

        def add_raster(self, url, name='Raster', fit_bounds=True, **kwargs):
            """Adds a raster layer to the map.

            Args:
                self: The map.
                url (str): The URL to the raster.
                name (str, optional): The name of the raster layer. Defaults to "Raster".
                fit_bounds (bool, optional): Whether to fit the bounds of the map to the raster. Defaults to True.
                kwargs: Keyword arguments to pass to the raster layer.

            Returns:
                ipyleaflet.RasterLayer: The raster layer.
            """
            import httpx

            titiler_endpoint = "https://titiler.xyz"

            r = httpx.get(
                f"{titiler_endpoint}/cog/info",
                params = {
                    "url": url,
                }
            ).json()

            bounds = r["bounds"]

            r = httpx.get(
                f"{titiler_endpoint}/cog/tilejson.json",
                params = {
                    "url": url,
                }
            ).json()

            tile = r["tiles"][0]

            self.add_tile_layer(url=tile, name=name, **kwargs)

            if fit_bounds:
                bbox = [[bounds[0], bounds[1]], [bounds[2], bounds[3]]]
                self.fit_bounds(bbox)


##  Practice with functions


def random_string(length, upper=False, digits=False):
    """Generates a random string of a given length.

    Args:
        length (_type_): The length of the string to generate.
        upper (bool, optional): Whether to include uppercase letters. Defaults to False.
        digits (bool, optional): Whether to include digits. Defaults to False.

    Returns:
        str: random string
    """    
    letters = string.ascii_lowercase
    if upper:
        letters += string.ascii_uppercase
    if digits:
        letters += string.digits
    return ''.join(random.choice(letters) for i in range(length))

#####  Converting Census Data formatting to a format that will join with the city socioeconomic database

def excel_to_dataframe(excel_file, sheet_name, index_col=None):
    """Converts an excel file to a dataframe.

    Args:
        excel_file (str): The excel file to convert.
        sheet_name (str): The name of the sheet to convert.
        index_col (str, optional): The column to use as the index. Defaults to None.

    Returns:
        pandas.DataFrame: The dataframe.
    """
    return pandas.read_excel(excel_file, sheet_name=sheet_name, index_col=index_col)

def copy_columns_to_index(df, columns):
    """Copies the values of the given columns to the index.

    Args:
        df (pandas.DataFrame): The dataframe to copy the columns from.
        columns (list): The columns to copy to the index.

    Returns:
        pandas.DataFrame: The dataframe with the columns copied to the index.
    """
    for column in columns:
        df[column] = df.index
    return df

def edit_city_names(df, phrase):
    """Edits the dataframe values by entering a string to remove from the right side of the city name.

    Args:
        df (pandas.DataFrame): The dataframe to edit.
        phrase (str): The string to remove from the right side of the county name.

    Returns:
        pandas.DataFrame: The dataframe with the city names edited.
    """
    df = df.str.replace(phrase, "")
    return df

def aggregate_by_county(df, county_column, agg_column, agg_func):
    """Aggregates the values of a column by county.

    Args:
        df (pandas.DataFrame): The dataframe to aggregate.
        county_column (str): The name of the county column.
        agg_column (str): The name of the column to aggregate.
        agg_func (str): The aggregation function to use.

    Returns:
        pandas.DataFrame: The aggregated dataframe.
    """
    return df.groupby(county_column)[agg_column].agg(agg_func)
