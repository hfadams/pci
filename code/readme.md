# Code for formatting and processing lake and solar radiation data

This folder contains the main scripts for the growth window dataset preparation. The order of use is as follows:

1. Basic formatting of original data files for consistent units and headings (code not provided since not all data is open access)

2. Growth windows are calculated using the *growth\_window\_calculations.py* script, which calls on functions from the *growth\_window\_functions.py* file. The output is the growth window dataset without paired surface solar radiation data.

3. The growth window data file is imported into QGIS as a point vector layer, and the *ssr\_lakes\_pairing\_qgis.py*, *lakes\_dem\_extraction.py*, and *ssr\_dem\_extraction.py* scripts are opened in QGIS under plugins > Python console (usiing the "Show Editor" icon in the Python console to open and edit the scripts). 

	a) **ssr\_lakes\_pairing\_qgis.py** generates a copy of the lake points layer, with the paired SSR point data appended to each lake point along with distance between the lake and SSR stations

	b) **lakes\_dem\_extraction.py** generates a copy of the imported lake points layer, with the lake elevation, area, volume, and depth added

	c) **ssr\_dem\_extraction.py** generates a copy of the input SSR points layer, with the SSR elevation added.


4. SSR growth window and pre-growth window means are calculated using the *paired\_stations\_ssr\_calcs.py* script.

## Software and packages
* [Python version 3.7.6](https://www.python.org/downloads/release/python-376/)
* [QGIS 3.16](https://qgis.org/en/site/forusers/download.html)

##### General
* [pandas](https://pandas.pydata.org/)
* [numpy](https://numpy.org/)
* [dplython](https://pythonhosted.org/dplython/)
* [glob](https://docs.python.org/3.7/library/glob.html)

##### Growth window analysis
* [scipy.signal find_peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html)
* [scipy.signal savgol_filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html)

##### Plotting
* [matplotlib](https://matplotlib.org/)
* [ptitprince](https://pypi.org/project/ptitprince/)
* [RainCloudPlots](https://github.com/RainCloudPlots/RainCloudPlots)
* [seaborn](https://seaborn.pydata.org/)

## Scripts

#### lakes
* growth\_window\_calculations.py
* growth\_window\_functions.py

#### QGIS
* ssr\_lakes\_pairing\_qgis.py
* lakes\_dem\_extraction.py
* ssr\_dem\_extraction.py

#### solar radiation
* paired\_stations\_ssr\_calcs.py


