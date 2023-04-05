"""Main module."""

import string
import random
import ipyleaflet
import pandas

class Map(ipyleaflet.Map):

        def __init__(self, center, zoom, **kwargs) -> None:

            if "scroll_wheel_zoom" not in kwargs:
                kwargs["scroll_wheel_zoom"] = True

            super().__init__(center=center, zoom=zoom, **kwargs)

            if "layers_control" not in kwargs:
                kwargs["layers_control"] = True
            
            if kwargs["layers_control"]:
                self.add_layers_control()

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
