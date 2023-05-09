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
        elif basemap.lower() == "terrain_only":
            url = 'http://mt0.google.com/vt/lyrs=t&hl=en&x={x}&y={y}&z={z}'
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "terrain":
            url = 'http://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}'
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
    

    def add_image(self, path, w=250, h=250):
        """Adds a small image (like your logo) to the bottom right of the map
        Args:
        file (str): the filepath of the image
        w (int) : width of the image (defaults 250 px)
        h (int) : height of the image (defaults 250 px)
        """
        import ipywidgets as widgets

        file = open(path, "rb")
        image = file.read()
        i = widgets.Image(
            value=image,
            format='png',
            width=w,
            height=h,
        )
                
        output_widget = widgets.Output()
        output_control = ipyleaflet.WidgetControl(widget=output_widget, position='bottomright')
        self.add_control(output_control)
        with output_widget:
            self.add_control(ipyleaflet.WidgetControl(widget=i, position='bottomright'))

    def add_toolbar(self, position="topright"):
        """Adds a dropdown widget to select a basemap.
        Args:
            self: The map.
            position (str, optional): The position of the toolbar. Defaults to "topright".
        """
        import ipywidgets as widgets

        widget_width = "250px"
        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar",
            icon="wrench",
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )

        toolbar = widgets.HBox([toolbar_button, close_button])

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()
                basemap.close()
                
        close_button.observe(close_click, "value")

        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px"))

        icons = ["folder-open", "map", "bluetooth", "area-chart"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(description="", button_style="primary", icon=icons[i*rows+j], 
                                            layout=widgets.Layout(width="28px", padding="0px"))
                
        toolbar = widgets.VBox([toolbar_button])

### Basemap info

        basemap = widgets.Dropdown(
            options=['OpenStreetMap', 'ROADMAP', 'SATELLITE','TERRAIN','TERRAIN WITH LABELS'],
            value=None,
            description='Basemap:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='250px')
        )

        basemap_ctrl = ipyleaflet.WidgetControl(widget=basemap, position='topright')

        def change_basemap(change):
            if change['new']:
                self.add_basemap(basemap.value)

        basemap.observe(change_basemap, names='value')

### Dropdown

        output = widgets.Output()
        output_ctrl = ipyleaflet.WidgetControl(widget=output, position="bottomright")
        self.add_control(output_ctrl)

        def tool_click(b):
            with output:
                output.clear_output()
                print(f"You clicked the {b.icon} button.")
                if b.icon == 'map':
                    if basemap_ctrl not in self.controls:
                        self.add_control(basemap_ctrl)
        
        for i in range(rows):
            for j in range(cols):
                tool = grid[i, j]
                tool.on_click(tool_click)

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]
                
        toolbar_button.observe(toolbar_click, "value")

        toolbar_ctrl = ipyleaflet.WidgetControl(widget=toolbar, position=position)

        self.add_control(toolbar_ctrl)

    def add_wms_layer(self, url, name, layers, format='image/png', transparent=True, attribution='', **kwargs):
        """Adds a WMS layer to the map.
        Args:
            url (str): The URL of the WMS service.
            name (str): The name of the layer.
            layers (str): The layers of the WMS service.
            format (str, optional): The format of the image. Defaults to 'image/png'.
            transparent (bool, optional): Whether the image is transparent. Defaults to True.
            attribution (str, optional): The attribution of the data. Defaults to ''.
        """
        import ipyleaflet
        import requests
        from ipyleaflet import WMSLayer

        wms = ipyleaflet.WMSLayer(
            url=url,
            layers=layers,
            format=format,
            transparent=transparent,
            attribution=attribution,
            name=name, **kwargs
        )
        self.add_layer(wms)

    def add_landcover(self, NLCD, **kwargs):
        """Adds the NLCD to the map.
        
        Args:
            self: The map.
            NLCD (str): The NLCD to add.
            kwargs: Keyword arguments to pass to the NLCD.
        """
        if NLCD.lower() == "2001 land cover":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2001_Land_Cover_L48/wms?'
            layers = 'NLCD_2001_Land_Cover'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2001 impervious":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2001_Impervious/wms'
            layers = 'NLCD_2001_Impervious'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2001 tree canopy":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2001_Tree_Canopy/wms'
            layers = 'NLCD_2001_Tree_Canopy'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2004 land cover":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2004_Land_Cover_L48/wms?'
            layers = 'NLCD_2004_Land_Cover'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2004 impervious":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2004_Impervious/wms'
            layers = 'NLCD_2004_Impervious'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2004 tree canopy":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2004_Tree_Canopy/wms'
            layers = 'NLCD_2004_Tree_Canopy'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2006 land cover":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2006_Land_Cover_L48/wms?'
            layers = 'NLCD_2006_Land_Cover'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2006 impervious":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2006_Impervious/wms'
            layers = 'NLCD_2006_Impervious'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2006 tree canopy":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2006_Tree_Canopy/wms'
            layers = 'NLCD_2006_Tree_Canopy'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2008 land cover":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2008_Land_Cover_L48/wms?'
            layers = 'NLCD_2008_Land_Cover'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2008 impervious":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2008_Impervious/wms'
            layers = 'NLCD_2008_Impervious'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2008 tree canopy":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2008_Tree_Canopy/wms'
            layers = 'NLCD_2008_Tree_Canopy'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2019 land cover":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2019_Land_Cover_L48/wms?'
            layers = 'NLCD_2019_Land_Cover_L48'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2019 impervious":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2019_Impervious/wms'
            layers = 'NLCD_2019_Impervious'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        elif NLCD.lower() == "2019 tree canopy":
            url = 'https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2019_Tree_Canopy/wms'
            layers = 'NLCD_2019_Tree_Canopy'
            self.add_wms_layer(url, layers=layers, name=NLCD, **kwargs)
        else:
            print("Please enter a valid NLCD year.")


    def add_swipe_control(self, layer1_url, layer2_url, swipe_position):
        '''Adds a swipe control to the map.
        Args:
            layer1_url (str): The URL of the first tile layer to swipe between.
            layer2_url (str): The URL of the second tile layer to swipe between.
            swipe_position (str): The position of the swipe control. Valid values are 'bottomleft', 'bottomright', 'topleft', and 'topright'.'''	        
        # Create the two layers to swipe between
        layer1 = ipyleaflet.TileLayer(url=layer1_url, name="Layer 1")
        layer2 = ipyleaflet.TileLayer(url=layer2_url, name="Layer 2")

        # Create a layer group to hold the two layers
        layer_group = ipyleaflet.LayerGroup(layers=(layer1, layer2))

        # Add the layer group to the map
        self.add_layer(layer_group)

        # Create the swipe control and add it to the map
        swipe_control = ipyleaflet.SplitMapControl(left_layer=layer1, right_layer=layer2, position=swipe_position)
        self.add_control(swipe_control)

        # make the swipe control draggable
        def on_mouse_down(event):
            swipe_control.dragging = True
            swipe_control.start_x = event['containerPoint'][0]

        def on_mouse_move(event):
            if swipe_control.dragging:
                delta = event['containerPoint'][0] - swipe_control.start_x
                swipe_control.split_position += delta / self.width * 100
                swipe_control.start_x = event['containerPoint'][0]

        def on_mouse_up(event):
            swipe_control.dragging = False

        self.on_interaction(on_mouse_down, 'mousedown')
        self.on_interaction(on_mouse_move, 'mousemove')
        self.on_interaction(on_mouse_up, 'mouseup')

        print("Swipe tool added to map")


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

def join_shapefile_to_dataframe(df, shapefile, index_column, join_column):
    """Joins a shapefile to a dataframe.

    Args:
        df (pandas.DataFrame): The dataframe to join.
        shapefile (str): The shapefile to join.
        index_column (str): The column to use as the index.
        join_column (str): The column to join on.

    Returns:
        geopandas.GeoDataFrame: The joined dataframe.
    """
    gdf = geopandas.read_file(shapefile)
    gdf = gdf.set_index(index_column)
    gdf[join_column] = gdf.index
    gdf = gdf.join(df, on=join_column)
    return gdf

def columns_to_list(df, columns):
    """Converts the values of the given columns to a list.

    Args:
        df (pandas.DataFrame): The dataframe to convert.
        columns (list): The columns to convert.

    Returns:
        pandas.DataFrame: The dataframe with the columns converted to lists.
    """
    for column in columns:
        df[column] = df[column].str.split(", ")
    return df
