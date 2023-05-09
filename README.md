# maplab


[![image](https://img.shields.io/pypi/v/maplab.svg)](https://pypi.python.org/pypi/maplab)


**A Python package for visualizing and manipulating geospatial data.**


-   Free software: MIT license
-   Documentation: [https://hwilli72.github.io/maplab](https://hwilli72.github.io/maplab)
-   GitHub: [https://github.com/hwilli72/maplab](https://github.com/hwilli72/maplab) 
-   PyPI: [https://pypi.org/project/maplab/](https://pypi.org/project/maplab/)
-   YouTube tutorial: [https://www.youtube.com/watch?v=9N_v5G9j6LE](https://www.youtube.com/watch?v=9N_v5G9j6LE)
    

## Introduction

MapLab is a Python package for visualizing and manipulating geospatial data. It is built on top of [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) and [folium](https://python-visualization.github.io/folium/), both of which are used for interactive mapping. MapLab provides a set of tools for creating interactive maps and preparing data for spatial analysis. It also provides a set of tools for adding geospatial data from the web to the interactive map. This package is designed for both beginners and advanced users. It is easy to use and can be applied to teaching and research purposes. I find a lot of the existing geospatial packages are very complicated in practice for beginners, and with this project I aimed to reach those who are not advanced in their GIS skills but simply want to display data with a spatial component on a map. MapLab has various functions that allow users to load shapefiles, basemaps, raster data, and other types of vector data onto an interactive map with minimal coding. Furthermore, MapLab includes functions that automate data cleaning operations that would otherwise be performed in excel to prepare geospatial data for mapping applications. I hope this package can fill the gap and make geospatial data analysis more accessible to a wider audience. 

## Key Features

-   Create a map in a jupyter notebook with one line of code
-   Load shapefiles, basemaps, raster data, and other types of vector data onto an interactive map
-   Download geospatial data from the web
-   Automate data cleaning operations that would otherwise be performed in excel to prepare geospatial data for mapping applications
-   Create a split map with different layers on each side to compare change over time
-   Add WMS National Land Cover Database layers to a map   

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
