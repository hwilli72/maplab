"""Main module."""

import string
import random
import ipyleaflet 
import pandas
import geopandas 
import openpyxl
import folium 

class Map(ipyleaflet.Map):
    
    """A class to create a map with ipyleaflet.
    Args:
        center (list, optional): The center of the map. Defaults to [20, 0].
        zoom (int, optional): The zoom level of the map. Defaults to 2.
        kwargs: Keyword arguments to pass to the map.
    """

    def __init__(self, center=[20, 0], zoom=2, **kwargs) -> None:

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(center=center, zoom=zoom, **kwargs)

        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True

        if kwargs["layers_control"]:
            self.add_layers_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True
        
        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()

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

    def add_basemap(self, basemap, **kwargs):
        """Adds a basemap to the map.
        Args:
            self: The map.
            basemap (str): The basemap to add.
            kwargs: Keyword arguments to pass to the basemap.
        """
        import xyzservices.providers as xyz

        if basemap.lower() == "roadmap":
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "satellite":
            url = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError(f"Basemap '{basemap}' not found.")

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

    def add_gdf(self, gdf, name='GeoDataFrame', **kwargs):
        """Adds a geopandas GeoDataFrame to the map.

        Args:
            self: The map.
            gdf: The geopandas GeoDataFrame.
            name (str, optional): The name of the GeoDataFrame layer. Defaults to "GeoDataFrame".
            kwargs: Keyword arguments to pass to the GeoDataFrame layer.

        Returns:
            gdf.__geo_interface__: The GeoDataFrame layer.
        """
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)

    def add_vector(self, data, name='Vector', **kwargs):
        """ Adds any geopandas supported vector data to the map.
        Args:
            self: The map.
            data: The vector data.
            name (str, optional): The name of the vector layer. Defaults to "Vector".
            kwargs: Keyword arguments to pass to the vector layer."""
        import geopandas as gpd
        if data.endswith(".shp"):
            self.add_shp(data, name=name, **kwargs)
        if data.endswith(".geojson"):
            self.add_geojson(data, name=name, **kwargs)
        else:
            gdf = gpd.read_file(data) 
            self.add_gdf(gdf, name=name, **kwargs)

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
