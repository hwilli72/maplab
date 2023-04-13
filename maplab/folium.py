"""Folium module."""

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

        super().__init__(center=center, zoom=zoom, **kwargs)
        
        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True

        if kwargs["layers_control"]:
            self.add_layers_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True

        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()

# Add Search Control Function
    def add_search_control(self, position="topleft", **kwargs):
        """Add a search control to the map.
        Args:
            **kwargs: Keyword arguments passed to the search control.
        """
        if "url" not in kwargs:
            kwargs["url"] = "https://nominatim.openstreetmap.org/search?format=json&q={s}"

        search_control = folium.SearchControl(position=position, **kwargs)
        self.add_control(search_control)

# Add Draw Control Function
    def add_draw_control(self, **kwargs):
        """Add a draw control to the map.
        
        Args:
            **kwargs: Keyword arguments passed to the draw control.
        """
        draw_control = folium.DrawControl(**kwargs)
        self.add_control(draw_control)

# Add Layers Control Function
    def add_layers_control(self, position='topright'):
        """Add a layers control to the map.
        Args:
            **kwargs: Keyword arguments passed to the layers control.
        """
        layers_control = folium.LayersControl(position=position)
        self.add_child(layers_control)

# Add Fullscreen Control Function
    def add_fullscreen_control(self, position='topright'):
        """Add a fullscreen control to the map.
        Args:
            **kwargs: Keyword arguments passed to the fullscreen control.
        """
        fullscreen_control = folium.FullscreenControl(position=position)
        self.add_child(fullscreen_control)

# Add Tile Layer Function
    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Add a tile layer to the map.
        Args:
            url (str): The url of the tile layer.
            name (str): The name of the tile layer.
            attribution (str, optional): The attribution of the tile layer. Defaults to "".
        """
        tile_layer = folium.TileLayer(
            url=url, 
            name=name, 
            attribution=attribution,
            **kwargs
        )
        self.add_layer(tile_layer)

# Basemap Function
    def add_basemap(self, basemap, **kwargs):
        """Add a basemap to the map.
        
        Args:
            basemap (str): The name of the basemap.
            **kwargs: Keyword arguments passed to the basemap.
        """
        
        import xyzservices.providers as xyz

        if basemap.lower() == "roadmap":
            url = 'http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "satellite":
            url = 'http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError(f"{basemap} is not a valid basemap.")
            
# Add GeoJSON Function
    def add_geojson(self, data, name='GeoJSON', **kwargs):
        """Add a GeoJSON layer to the map.
        Args:
            data (dict): The GeoJSON data.
            name (str, optional): The name of the GeoJSON. Defaults to 'GeoJSON'.
        """
       
        if isinstance(data, str):
            import json
            with open(data, 'r') as f:
                data = json.load(f)

        geojson = folium.GeoJson(data=data, name=name, **kwargs)
        self.add_geojson(geojson)

# Add Shapefile Function
    def add_shp(self, data, name='Shapefile', **kwargs):
        """Add a shapefile layer to the map.
        Args:
            data (str): The path to the shapefile.
            name (str, optional): The name of the shapefile. Defaults to 'Shapefile'.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.to_json()
        self.add_geojson(geojson, name=name, **kwargs)

# Add a Vector Function
    def add_vector(self, data, name='Vector', **kwargs):
        """Add a vector layer to the map.
        Args:
            data (str): The path to the vector file.
            name (str, optional): The name of the vector file. Defaults to 'Vector'.
        """
        import geopandas as gpd
        gdf = gpd.read_file(data)
        geojson = gdf.to_json()
        self.add_geojson(geojson, name=name, **kwargs)

# Add a Raster Function
    def add_raster(self, url, name='Raster', fit_bounds=True, **kwargs):
        """Add a raster layer to the map.
        
        Args:
            url (str): The URl of the raster layer.
            name (str, optional): The name of the raster layer. Defaults to 'Raster'.
            fit_bounds (bool, optional): Whether to fit the bounds of the raster layer. Defaults to True.
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
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)