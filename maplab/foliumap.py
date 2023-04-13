"""Foliumap module."""
import string
import random
import folium

class Map(folium.Map):

    """A folium map with additional functionality.
    Args:
        center (list, optional): The center of the map. Defaults to [20,0].
        zoom (int, optional): The zoom level of the map. Defaults to 2.
        **kwargs: Keyword arguments passed to the folium map.
    """

    def __init__(self, center=[20,0], zoom=2, **kwargs) -> None:
        """Adds the ability to use a mouse to zoom in and out.
        
        Args:
            **kwargs: Keyword arguments passed to the scroll wheel zoom.
        """
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(location=center, zoom_start=zoom, **kwargs)

# Add Tile Layer Function
    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Add a tile layer to the map.
        Args:
            url (str): The url of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = folium.TileLayer(
            tiles=url, 
            name=name, 
            attr=attribution,
            **kwargs
        )
        self.add_child(tile_layer)

# Add basemap function
    def add_basemap(self, name, **kwargs):
        """Add a basemap from folium to the map.
        Args:
            name (str): The name of the basemap.
        """
        basemap = folium.basemaps[name](**kwargs)
        self.add_child(basemap)

# Add shapefile function
    def add_shapefile(self, path, name, **kwargs):
        """Add a shapefile to the map.
        Args:
            path (str): The path to the shapefile.
            name (str): The name of the shapefile.
        """
        shapefile = folium.features.GeoJson(
            data=path,
            name=name,
            **kwargs
        )
        self.add_child(shapefile)

# Add GeoJSON function
    def add_geojson(self, path, name, **kwargs):
        """Add a GeoJSON file to the map.
        Args:
            path (str): The path to the GeoJSON file.
            name (str): The name of the GeoJSON file.
        """
        geojson = folium.features.GeoJson(
            data=path,
            name=name,
            **kwargs
        )
        self.add_child(geojson)






