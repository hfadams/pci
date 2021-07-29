*This readme.md file was generated on 2021-07-26 by Hannah Adams*

# Chlorophyll-*a* growth window dataset

## Authors
**Hannah Adams:** University of Waterloo, hfadams@uwaterloo.ca

**Jane Ye:** University of Waterloo, jane.ye@uwaterloo.ca

**Stephanie Slowinski:** University of Waterloo, seslowinski@uwaterloo.ca

**Bhaleka Persaud:** University of Waterloo, bd2persaud@uwaterloo.ca

**Homa Kheyrollah-Pour:** Wilfrid Laurier University, hpour@wlu.ca

**Philippe van Cappellen:** University of Waterloo, pvc@uwaterloo.ca



## Data sources

In situ chlorophyll-*a* and associated lake physicochemical data were collected from open source international, federal, and regional databases from May 2020 to January 2021.
### Lake data: 
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

### Solar radiation:

### Miscelaneous:
* DEM
* HydroLakes
* HydroATLAS

*full summary available in the database_summary.csv file*


## Methods

Growth windows are defined based on the rate of change in chlorophyll-*a* concentration throughout the year after smoothing the annual time series for each lake using the Savitzky-Golay filter [(Savitzky and Golay, 1964)](https://pubs.acs.org/doi/10.1021/ac60214a047) and flagging optima in the smoothed data using the following functions:

* [scipy.signal savgol_filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html) 
* [scipy.signal find_peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html#scipy.signal.find_peaks)


	
Mean values were calculated for all water quality variables sampled during the growth window.

##### Quality assurance
We removed all data recorded as below the instrument detection limit and selected years where samples were collected a minimum of 8 times over the ice-free season.

Data files from varying sources were formatted to have consistent units and column headers, and were rounded to daily mean values.

## Software and packages 

All data processing and analyses for this project were implemented using Python (ver. 3.7.6) and QGIS/PYQGIS (ver. 3.14; QGIS.org, 2021).
##  Data and file overview


### Folder 1:  Data: 
All data used to create the growth window dataset 

##### subfolder a: processed_data 
Contains the growth window dataset and supporting metadata
		
 * growth\_window\_data.csv: 
  	   	   
 * lake\_summary.csv: 
  	   	    
	
##### subfolder b: supplementary_data
  	   
 Metadata and relevant supplimentary files
		
* daily_mean.csv:
  
	Formatted *in situ* water quality data that has been rounded to daily mean (processed by format_lakes function)

* all\_lake\_coordinates.csv:
  	   	     
* Growth\_window\_variable\_description.csv
  	   	       
* lake\_name\_formatting.csv
  	   	     
* database\_summary.csv:
  	   	     
### Folder 2: code    
      	
Scripts for formatting data and detecting growth windows

* growth\_window\_functions.py
  	   	   
* growth\_window\_calculations.py
  	   	   
* lake\_name\_formatting.csv

* all\_lake\_formatting.py

* gw\_plots.py
  	   	   

## Recommended citation 

Adams, H., Ye, J., Slowinski, S., Persaud, B., Kheyrollah Pour, H., van Cappellen, P. (2021). Chlorophyll-a rate and environmental variables during periods of seasonal algal growth in northern, temperate lakes.

## Sharing and accessing the data
These data are available under a [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

## Funding
This work is funded by the Canada First Research Excellence Fund’s Global Water Futures Programme.











