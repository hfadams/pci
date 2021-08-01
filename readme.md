
# Chlorophyll-*a* growth window dataset
The scripts within this repository were used to standardize and compile a dataset of *in situ* chlorophyll-*a* data and related water quality data and for lakes at or above 40°N across the Northern hemisphere. Original data files are not included, but can be found by following the links listed under "Data sources" below. 

The chlorophyll-*a* growth window dataset contains chlorophyll-*a* rate of increase along with  mean water quality variables (i.e., surface water temperature, nutrients, and solar radiation) during periods of rapid algal growth referred to as the _**growth window**_. Growth windows were defined based on the rate of change in the fluctuating chlorophyll-*a* concentration sampled over the year, and categorized as occurring in the spring, summer, or as a "single" growth window when there was one main period of growth. Additional lake parameters were included from the HydroLAKES and HydroATLAS databases, and trophic status index was calculated from the chlorophyll-*a* data.

This dataset is meant to be used to explore trends between different environmental conditions and algal growth. However, as a compiled dataset, the growth window data is based on lakes samples collected from a variety of organizations with differing methods. Great care was taken to standardize the data and provide all relevant metadata wherever possible. However, it is recommended that the dataset be uniquely subsetted depending on the research question (e.g., for sampling frequency or depth). 

 
## Data sources

*In situ* lake physiochemical data and solar radiation data were collected from open source international, federal, and regional databases between May 2020 and January 2021 from the following sources: 
### Lake data 
 * [Open Canada](https://open.canada.ca/data/en/dataset/d155effe-048d-45cf-8683-d827dadc428b)
 * [Lake Winnipeg DataStream](https://lakewinnipegdatastream.ca/)
 * [University of Winnipeg](http://lwbin-datahub.ad.umanitoba.ca/dataset/lwpg-namao-chem/resource/931532fe-1785-4a9f-a857-f5d6ddab43e9?view_id=61484de8-2fe6-46df-abd3-37ac9ca9f4f1)
 * [IISD-ELA private database](https://www.iisd.org/ela/science-data/our-data/data-requests/)
 * [Alberta Environment and Parks data repository](http://environment.alberta.ca/apps/EdwReportViewer/LakeWaterQuality.aspx)
 * [LUBW data and map service](https://udo.lubw.baden-wuerttemberg.de/public/index.xhtml)
 * [GEMS](http://db.cger.nies.go.jp/gem/inter/GEMS/database/kasumi/contents/datalist.html)
 * [VISS](https://viss.lansstyrelsen.se/)
 * [UK Environment Agency](https://environment.data.gov.uk/water-quality/view/download)
 * [KNB](https://knb.ecoinformatics.org/view/kgordon.35.96)
 * [University of Wisconsin NLTER](https://lter.limnology.wisc.edu/node/55078)
 * [DataONe](https://search.dataone.org/view/https%3A%2F%2Fpasta.lternet.edu%2Fpackage%2Fmetadata%2Feml%2Fedi%2F186%2F3)
 * [USGS and USEPA water quality portal](https://www.waterqualitydata.us/#:~:text=The%20Water%20Quality%20Portal%20WQP,%2C%20tribal%2C%20and%20local%20agencies)

### Solar radiation
* [Baseline Solar Radiation Network](https://bsrn.awi.de/)
* [ETH Zürich Global Energy Balance](https://geba.ethz.ch/)
* [IISD-ELA private database](https://www.iisd.org/ela/science-data/our-data/data-requests/)
* [Agriculture Alberta Station Data](https://agriculture.alberta.ca/acis/weather-data-viewer.jsp)
* [Environment and Climate Change Canada](https://drive.google.com/drive/folders/1VhYUoVhKyL7TnyLQ9ApiLmpS0XlTkv0s)

### Additional parameters:
* [Global Multi-resolution Terrain Elevation Data (GMTED2010)](https://www.usgs.gov/core-science-systems/eros/coastal-changes-and-impacts/gmted2010?qt-science_support_page_related_con=0#qt-science_support_page_related_con)
* [HydroLAKES](https://hydrosheds.org/page/hydrolakes)
* [HydroATLAS](https://hydrosheds.org/page/hydroatlas)

*A full summary of data sources is available in the [lake_database.csv]() and [ssr_database.csv]() files*


## Methods

Growth windows are defined based on the rate of change in chlorophyll-*a* concentration throughout the year after smoothing the annual time series for each lake using the Savitzky-Golay filter [(Savitzky and Golay, 1964)](https://pubs.acs.org/doi/10.1021/ac60214a047) and flagging optima in the smoothed data using the following functions:

* [scipy.signal savgol_filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html) 
* [scipy.signal find_peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html#scipy.signal.find_peaks)

Mean values were calculated for all water quality variables sampled during the growth window and are provided in the [daily_mean.csv]() file.

##### Quality assurance

Data files from varying sources were formatted to have consistent units and column headers; we removed all data recorded as below the instrument detection limit and selected years where samples were collected a minimum of 8 times over the ice-free season.

## Software and packages 

All data processing and analyses for this project were implemented using Python (ver. 3.7.6) and QGIS/PYQGIS (ver. 3.14).

##  Data and file overview


### Folder 1:  Data: 
Contains the growth window dataset, metadata, and relevant supplementary information.

#### subfolder a: processed_data 
Growth window dataset and summary of parameters for all lake sampling locations.
		
 * [growth\_window\_data.csv](https://github.com/hfadams/growth_window/blob/3354fa0c2aea2bd1af4f02e528693c68157a8335/data/processed_data/growth_window_data.csv): Compiled growth window dataset
  	   	   
 * [lake\_summary.csv](https://github.com/hfadams/growth_window/blob/3354fa0c2aea2bd1af4f02e528693c68157a8335/data/processed_data/lake_summary.csv): Summary of growth window data

* [daily\_mean.csv](https://github.com/hfadams/growth_window/blob/3354fa0c2aea2bd1af4f02e528693c68157a8335/data/processed_data/daily_mean.csv): formatted *in situ* water quality data that has been rounded to daily mean (processed by format_lakes function)
  	   	    
	
#### subfolder b: supplementary_data
  	   
 Metadata and relevant supplementary files
  	   	     
* [Growth_window_variable_description.csv](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/data/supplementary%20_data/growth_window_variable_description.csv): Units and description of each variable in the growth window dataset
  	   	       
* [lake_name_formatting.csv](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/data/supplementary%20_data/lake_name_formatting.csv): conversion of lake names from original sampling location ID to name in the growth window dataset
  	   	     
* [lake_database\_summary.csv](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/data/supplementary%20_data/lake_database_summary.csv): summary of all databases used for *in situ* water quality data collection

* [HydroATLASclimatezones.csv](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/data/supplementary%20_data/HydroATLASclimatezones.csv): legend for HydroATLAS climate zone values
  	   	     
### Folder 2: code    
      	
Scripts for formatting data and detecting growth windows

* [growth_window_functions.py](https://github.com/hfadams/growth_window/blob/862bc82edc4b0be763f729d8ec3e078828750e47/code/growth_window_functions.py): all functions used to generate the growth window dataset
  	   	   
* [growth_window_calculations.py](https://github.com/hfadams/growth_window/blob/862bc82edc4b0be763f729d8ec3e078828750e47/code/growth_window_calculations.py): script used to call on the growth window functions

* [ssr\_lakes\_pairing\_qgis.py](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/code/ssr_lakes_pairing_qgis.py): pairs lakes and SSR stations using PYQGIS

* [lake\_dem\_extraction.py](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/code/lake_dem_extraction.py): uses DEM in PYQGIS to extract lake elevation

* [ssr\_dem\_extraction.py](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/code/ssr_dem_extraction.py): uses DEM in PYQGIS to extract SSR station elevation

* [paired\_stations\_ssr\_calcs.py](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/code/paired_stations_ssr_calcs.py): calculates mean SSR during the growth window and pre-growth window period
  	   	   

## Sharing and accessing the data
This project is licensed under the Creative Commons Attribution 4.0 International license, please see [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) for details.

## Funding
This work is funded by the Canada First Research Excellence Fund’s Global Water Futures Programme.

## Recommended citation 

Adams, H., Ye, J., Slowinski, S., Persaud, B., Kheyrollah Pour, H., van Cappellen, P. (2021). Chlorophyll-a rate and environmental variables during periods of seasonal algal growth in northern, temperate lakes.

## Authors
**Hannah Adams:** University of Waterloo, hfadams@uwaterloo.ca

**Jane Ye:** University of Waterloo, jane.ye@uwaterloo.ca

**Stephanie Slowinski:** University of Waterloo, seslowinski@uwaterloo.ca

**Bhaleka Persaud:** University of Waterloo, bd2persaud@uwaterloo.ca

**Homa Kheyrollah-Pour:** Wilfrid Laurier University, hpour@wlu.ca

**Philippe van Cappellen:** University of Waterloo, pvc@uwaterloo.ca











