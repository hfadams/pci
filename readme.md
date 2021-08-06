# Chlorophyll-*a* growth window dataset
The scripts within this repository were used to standardize and compile a dataset of *in situ* chlorophyll-*a* data and related water quality data for lakes at or above 40° N across the Northern hemisphere. Original data files are not included, but can be found by following the links listed under "Data sources" below. 

The chlorophyll-*a* growth window dataset contains chlorophyll-*a* rate of increase along with  mean water quality variables (i.e., surface water temperature, nutrients, and solar radiation) during periods of rapid algal growth referred to as the _**growth window**_. Growth windows were defined based on the rate of change in the fluctuating chlorophyll-*a* concentration sampled over the year, and categorized as occurring in the spring, summer, or as a "single" growth window when there was one main period of growth. Additional lake parameters were included from the [HydroLAKES](https://hydrosheds./page/hydrolakes) and [HydroATLAS](https://hydrosheds.org/page/hydroatlas) databases, and trophic status index (TSI) was calculated from chlorophyll-*a* concentrations.

This dataset is intended to be used to explore trends between changing environmental conditions and lake productivity. However, as a compiled dataset, the growth window data is based on lakes samples collected from a variety of organizations with differing methods. Great care was taken to standardize the data and provide all relevant metadata wherever possible. However, it is recommended that the dataset be uniquely subsetted depending on the research question (e.g., for sampling frequency). 

 
## Data sources

*In situ* lake physiochemical data and solar radiation data were collected from open source international, federal, and regional databases between May 2020 and January 2021. A summary of the sources are listed below:
 
### Lake data 
 | Database                                                                                                                                                                   | Region    | Lakes in dataset                                                                                                                   | Start | End  | Variables                                                                |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|--------------------------------------------------------------------------------------------------------------------------------------|-------|------|---------------------------------------------------------------------------|
| [Open Canada](https://open.canada.ca/en)                                                                                                                                   | Canada    | Laurentian Great Lakes, Hamilton Harbour, Moon lake, South Lake, Whirlpool lake                                                      | 1991  | 2017 | Depth and chlorophyll                                                     |
| [Lake Winnipeg DataStream](https://lakewinnipegdatastream.ca/)                                                                                                             | Manitoba  | Lake Winnipeg                                                                                                                        | 2002  | 2020 | Chlorophyll, Secchi depth, TP, water temperature, SRP, miscellaneous ions |
| [CanWIN Data HUB](http://lwbin-datahub.ad.umanitoba.ca/dataset/lwpg-namao-chem/resource/931532fe-1785-4a9f-a857-f5d6ddab43e9?view_id=61484de8-2fe6-46df-abd3-37ac9ca9f4f1) | Manitoba  | Lake Winnipeg                                                                                                                        | 1996  | 2009 | Chlorophyll, Secchi depth, TP, water temperature, SRP, miscellaneous ions |
| [IISD-ELA private database](https://www.iisd.org/ela/science-data/our-data/data-requests/)                                                                                 | Ontario   | Experimental lakes 114, 224, 239, and 442                                                                                            | 1968  | 2019 | Chlorophyll, Secchi depth, TP, DOC, water temperature, PAR                |
| [Alberta Environment and Parks data repository](http://environment.alberta.ca/apps/EdwReportViewer/LakeWaterQuality.aspx)                                                  | Alberta   | Many lakes sampled by Alberta Environment and Parks                                                                                  | 1978  | 2018 | Chlorophyll, Secchi depth, TP, TKN, DOC, miscellaneous ions               |
| [LUBW data and map service](https://udo.lubw.baden-wuerttemberg.de/public/index.xhtml)                                                                                     | Germany   | Constance Untersee                                                                                                                   | 1998  | 2019 | Chlorophyll                                                               |
| [GEMS](http://db.cger.nies.go.jp/gem/inter/GEMS/database/kasumi/contents/datalist.html)                                                                                    | Japan     | Kasumigaura                                                                                                                          | 1977  | 2018 | Chlorophyll, depth, POC                                                   |
| [Water Information System Sweden (VISS)](https://viss.lansstyrelsen.se/)                                                                                                   | Sweden    | Many lakes sampled across Sweden                                                                                                     | 1945  | 2020 | Chlorophyll, depth                                                        |
| [UK Environment Agency](https://environment.data.gov.uk/water-quality/view/download)                                                                                       | UK        | Bassenthwaite, Belhalm tarn, Derwent water, Esthwaite water, Grasmere, Loch leven, Lake Windermere (north and south basin)           | 2000  | 2020 | Chloprophyll, Secchi depth, TP, pH, water temperature, miscellaneous ions |
| [UK Centre for Ecology and Hydrology](https://catalogue.ceh.ac.uk/documents/f385b60a-2a6b-432e-aadd-a9690415a0ca)                                                          | UK        | Many lakes sampled across the UK                                                                                                     | 1965  | 2013 | Chlorophyll, TP, Water temperature                                        |
| [Environmental Data Initiative portal](https://portal.edirepository.org/nis/home.jsp)                                                                                      | Global    | Central long lake, East long lake, Giles lake, Lacawac, May lake, Paul lake, Peter lake, Tuesday lake, Waynwood lake, West long lake | 2020  | 2020 | Chlorophyll, depth                                                        |
| [KNB](https://knb.ecoinformatics.org/view/kgordon.35.96)                                                                                                                   | Colerado  | Green Valley Lake, Oneida Lake                                                                                                       | 2000  | 2019 | Chlorophyll, Secchi depth, TP, water temperature, SRP,                    |
| [University of Wisconsin NLTER](https://lter.limnology.wisc.edu/node/55078)                                                                                                | Wisconsin | 10 lakes in the Long Term Environmental Research area                                                                                | 1981  | 2018 | Chlorophyll, depth                                                        |
| [USGS and USEPA water quality](https://www.waterqualitydata.us/)                    | USA       |                                                                                                                                      | 2010  | 2010 | chlorophyll, Secchi depth, TP, pH, water temperature                      |

### Solar radiation
| Database                                                                                     | Region  | Start | End  | Variable                                  |
|----------------------------------------------------------------------------------------------|---------|-------|------|-------------------------------------------|
| [ETH Zurich GEBA](https://geba.ethz.ch)                                                      | Global  | 1922  | 2017 | surface solar radiation (SSR)             |
| [Agriculture AB Station Data](https://agriculture.alberta.ca/acis/weather-data-viewer.jsp)   | Alberta | 2005  | 2020 | surface solar radiation (SSR)             |
| [Baseline Solar Radiation Network](https://bsrn.awi.de/)                                     | Global  | 1992  | 2017 | surface solar radiation (SSR)             |
| [ECCC](https://drive.google.com/drive/folders/1VhYUoVhKyL7TnyLQ9ApiLmpS0XlTkv0s?usp=sharing) | Canada  | 1956  | 2008 | surface solar radiation (SSR)             |
| [ELA](https://www.iisd.org/ela/science-data/our-data/data-requests/)                         | Ontario | 1968  | 2019 | photosynthetically active radiation (PAR) |
### Additional parameters:
* [Global Multi-resolution Terrain Elevation Data (GMTED2010)](https://www.usgs.gov/core-science-systems/eros/coastal-changes-and-impacts/gmted2010?qt-science_support_page_related_con=0#qt-science_support_page_related_con)
* [HydroLAKES](https://hydrosheds.org/page/hydrolakes)
* [HydroATLAS](https://hydrosheds.org/page/hydroatlas)

## Methods

Growth windows are defined based on the rate of change in chlorophyll-*a* concentration throughout the year after smoothing the annual time series for each lake using the Savitzky-Golay filter [(Savitzky and Golay, 1964)](https://pubs.acs.org/doi/10.1021/ac60214a047) and flagging optima in the smoothed data using the following functions:

* [scipy.signal savgol_filter](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html) 
* [scipy.signal find_peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html#scipy.signal.find_peaks)

Mean values were calculated for all water quality variables sampled during the growth window and are provided in the [daily_mean.csv]() file.

#### Quality assurance

Data files from varying sources were formatted to have consistent units and column headers; we removed all data recorded as below the instrument detection limit and selected years where samples were collected a minimum of 8 times over the ice-free season.

## Software and packages 

All data processing and analyses for this project were implemented using Python (ver. 3.7.6) and QGIS/PYQGIS (ver. 3.14).

##  Data and file overview


### Folder 1:  Data: 
Contains the growth window dataset, metadata, and relevant supplementary information.
		
 * [growth\_window\_data.csv](https://github.com/hfadams/growth_window/blob/3354fa0c2aea2bd1af4f02e528693c68157a8335/data/processed_data/growth_window_data.csv): Compiled growth window dataset
 * [lake\_summary.csv](https://github.com/hfadams/growth_window/blob/3354fa0c2aea2bd1af4f02e528693c68157a8335/data/processed_data/lake_summary.csv): Summary of growth window data
* [daily\_mean.csv](https://github.com/hfadams/growth_window/blob/3354fa0c2aea2bd1af4f02e528693c68157a8335/data/processed_data/daily_mean.csv): formatted *in situ* water quality data that has been rounded to daily mean (processed by format_lakes function)	   	    
	
#### subfolder a: supplementary_data
  	   
 Metadata and relevant supplementary files
  	   	     
* [Growth_window_variable_description.csv](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/data/supplementary%20_data/growth_window_variable_description.csv): Units and description of each variable in the growth window dataset
* [lake_name_formatting.csv](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/data/supplementary%20_data/lake_name_formatting.csv): conversion of lake names from original sampling location ID to name in the growth window dataset
* [lake_database\_summary.csv](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/data/supplementary%20_data/lake_database_summary.csv): summary of all databases used for *in situ* water quality data collection
* [HydroATLASclimatezones.csv](https://github.com/hfadams/growth_window/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/data/supplementary%20_data/HydroATLASclimatezones.csv): legend for HydroATLAS climate zone values

	**subfolder i: shapefiles**

	Lake and SSR shapefiles can be used to link with HydroATLAS and HydroSHEDS shapefiles. Style files can be used to format the points as seen in figure 1 of the manuscript.

	* lakes.zip: shapefile (and associated files) showing the lake locations and relevant attributes
	* ssr_stations.zip: shapefile (and associated files) showing the SSR station locations and relevant attributes
	* lake_coords.style: QGIS style file that can be used to format the lakes shapefile
	* ssr_coords.style: QGIS style file that can be used to format the SSR station shapefile
  	   	     
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

Adams, H., Ye, J., Slowinski, S., Persaud, B., Kheyrollah Pour, H., van Cappellen, P. (2021). Chlorophyll-a rate and environmental variables during periods of seasonal algal growth in northern, temperate lakes. DOI: ___

## Authors
### Scripts
**Hannah Adams** - *Author* - [LinkedIn](https://www.linkedin.com/in/hannah-adams-624122219/), [GitHub](https://github.com/hfadams)

**Jane Ye:** - *Co-author* - [LinkedIn](https://www.linkedin.com/in/janeye98/), [GitHub](https://github.com/jane801)

### Manuscript
**Hannah Adams** - *Author* - [LinkedIn](https://www.linkedin.com/in/hannah-adams-624122219/), [GitHub](https://github.com/hfadams)

**Jane Ye:** - *Co-author* - [LinkedIn](https://www.linkedin.com/in/janeye98/), [GitHub](https://github.com/jane801)

**Stephanie Slowinski:** -*Co-author* - [LinkedIn](https://www.linkedin.com/in/steph-slowinski/), [GitHub](https://github.com/s-slowinski)

**Bhaleka Persaud:** -*Co-author* - [GitHub]()

**Homa Kheyrollah-Pour:** -*Principle Investigator* - [Google Scholar](https://scholar.google.ca/citations?hl=en&user=0gMCo6wAAAAJ), [ReSEC lab](https://www.wlu.ca/academics/faculties/faculty-of-science/faculty-profiles/homa-kheyrollah-pour/index.html?ref=academics%2Ffaculties%2Ffaculty-of-arts%2Ffaculty-profiles%2Fhoma-kheyrollah-pour%2Findex.html)

**Philippe van Cappellen:** -*Principle Investigator*- [Google Scholar](https://scholar.google.ca/citations?user=E0Vw3FwAAAAJ&hl=en), [Ecohydrology Research Group](https://uwaterloo.ca/ecohydrology/people-profiles/philippe-van-cappellen) 











