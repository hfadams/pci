# Chlorophyll-*a* growth window dataset and associated files
This folder contains the growth window dataset along with the *in situ* data that has been converted to a daily mean and a summary file for all lakes and ssr stations that make up the dataset.

## Folder directory
* growth\_window\_data.csv: Containing water quality and other associated environmental data for 3137 growth windows
* daily_mean.csv: *in situ* water quality data where each variable has been rounded to daily mean (see growth_window_functions.py). Chlorophyll-*a* concentrations within the file are used to generate the growth window dataset
* lake_summary.csv: summary file for all lakes in the growth window dataset; each row provides the lake parameters, monitoring period, data source, and paired SSR station where relevant.

#### Subfolder A: supplementary_data
Data and metadata associated with the growth window dataset (see supplementary data readme.md for more information). 

* growth_window_variable_description.csv
* lake_name_formatting.csv
* database\_summary.csv
* HydroATLASclimatezones.csv

	**Subfolder i: shapefiles**

## Dataset summary
The growth window dataset consists of 3137 rows of unique growth windows with 42 variables/ lake and SSR station parameters. There are 357 lake sampling locations and 30 paired SSR stations ≥ 40°N, monitored between 1964-2019.

## Variable descriptions

* **lake:** Lake name, reformatted from original data file

* **lat, long:** coordinates in decimal degrees, collected from original data files and HydroLakes data

* **tsi, trophic status:**
      Trophic status index is calculated from mean chlorophyll-a concentration in the lake across all years sampled, and is used to assign a trophic status to each lake, based on guidelines from the [North American Lake Management Society](https://www.nalms.org/secchidipin/monitoring-methods/trophic-state-equations/).

	TSI ranges:
 	* < 30 = oligotrophic
 	* 30-50 = mesotrophic
 	* 50-60 = eutrophic
 	* > 60 = hypereutrophic
 

* **lake\_elev, area, mean\_depth, climate\_zone:** parameters collected from HydroLakes and HydroATLAS database. Climate zone is extracted from the [Global Environmental Stratification (GEnS) database](https://datashare.ed.ac.uk/handle/10283/3089). 
	

	**Climate zones:**
	
	* 6 = Extremely cold and mesic
	* 7 = Cold and mesic
	* 8 = Cool temperate and dry
	* 9 = Cool temperate and xeric
	* 10 = Warm temperate and mesic

	*full climate zone documentation available in the HydroATLASclimatezone.csv file*

* **year:** Year the growth period occurred

* **season:** indicates the timing of the growth period (spring, summer, or single_bloom)

* **num_samples:** Number of days sampled that year, can be used to filter the dataset for quality

* **start_day, end_day, gw_length:** year the growth period occurred

* **chla_rate:** rate of increase in chlorophyll-*a* concentration (ug/L) during the growth window

* **specific\_chla\_rate:** chlorophyll-a rate divided by the initial concentration at the start of the growth window (day^-1)

* **temp\_corrected\_specific\_chla\_rate:** specific chlorophyll-a rate corrected for the influence of temperature using the equation from [Rosso et al (1995)](https://journals.asm.org/doi/abs/10.1128/aem.61.2.610-616.1995):


		group.loc[:, 'f_temp'] = (mean_temp - t_max) * (mean_temp - t_min) ** 2 / ((t_opt - t_min) * ((t_opt - t_min) * (mean_temp - t_opt) - (t_opt - t_max) * (t_opt + t_min - 2 * mean_temp)))

        # divide specific growth rate by f_temp
        group.loc[:, 'temp_corrected_specific_chla_rate'] = group.loc[:, 'specific_chla_rate'] / group.loc[:, 'f_temp']


* **max\_chla:** Maximum chlorophyll-a concentration reached during the growth window (ug/L)

* **acc_chla:** accumulated chlorophyll-a over the growth window (ug/L), calculated using the numpy.trapz function

* **poc_rate:** Rate of change in particulate organic carbon (mg/L/day) during the growth window

* **chla\_to\_poc:** Rate of change in chlorophyll-a (ug/L/day) in proportion to particulate organic carbon (mg/L/day) during the growth window

* **mean\_temp, prev\_7days\_mean\_temp, prev\_14days\_mean\_temp:** mean surface water temperature (degrees Celsius) during the growth window and pre-growth window periods

* **mean\_tp, mean\_secchi, mean\_ph, mean\_srp, mean\_tkn:** mean total phosphorus (mg/L). Secchi depth (m), pH, soluble reactive phosphorus (mg/L), and mean total Kjeldahl nitrogen (mg/L) during the growth window

* **ssr\_station, ssr\_id, ssr\_lat, ssr\_long:** name and location of the surface solar radiation sampling station.

* **geo\_dist\_km:** geodic distance (m) between the paired lake ans SSR station

* **ssr\_elev, ssr\_lake\_elev\_diff:** elevation (m above sea level) of the SSR station and the difference in elevation between the paired lake ans SSR station

* **mean\_ssr, prev\_7days\_mean\_ssr, prev\_14days\_mean\_ssr:** mean surface solar radiation (W/m^2) during the growth window and pre growth window periods. Experimental Lakes Area (ELA) data was converted from photosynthetically active radiation (PAR) to SSR, where the PAR wavelength range (400-700 nm) was averaged as 550 nm for conversion calculations.

***NaN cells indicate no available data***

Complete summary is available in the *growth\_window\_variable\_description.csv* file in the supplementary data folder
