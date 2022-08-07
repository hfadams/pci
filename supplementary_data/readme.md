# PCI dataset: supplementary files
This folder contains source files used to generate the PCI dataset. *lake\_name\_formatting.csv* and *all_lake_coordinates.csv* files are used for generating the PCI dataset, in addition to the daily mean *in situ* water quality data, which can be found in the [FRDR repository]() along with the PCI dataset.

## Folder directory
* [lake_name_formatting.csv](https://github.com/hfadams/pci/blob/662c87faba3d5bd954d160357da87cf4741a9d4c/data/supplementary%20_data/lake_name_formatting.csv): conversion of lake names from original sampling location ID to name in the PCI dataset
* [all\_lake\_coords.csv](https://github.com/hfadams/pci/blob/ac46b91a203430bf76440d42d7880bbb072b425e/supplementary_data/all_lake_coordinates.csv): list of coordinates for all lakes in the dataset, used in the PCI calculation scripts. Coordinates were collected from the original data files or searched within the database where possible, otherwise they were estimated based on sampling location name.

## Dataset summary
The PCI dataset consists of 3077 rows of unique growth windows with 48 variables/ lake and SSR station parameters. There are 343 lake sampling locations and paired SSR stations ≥ 40°N, monitored between 1964-2019.

## Variable descriptions

| Variable                          | Units                                                | Description                                                                                                                                                                                                                                                                                    |
|-----------------------------------|------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| lake                              | NA                                                   | lake name, reformatted from original file                                                                                                                                                                                                     						    |
| lake_lat                          | decimal degrees                                      | lake latitude, collected from original data files and HydroLakes data  																											    |
| lake_long                         | decimal degrees                                      | lake longitude, collected from original data files and HydroLakes data 																											    |
| tsi                               | Range from 0-100                                     | calculated from mean chlorophyll-*a* concentration across all years the lake was sampled, based on guidelines from the [North American Lake Management Society](https://www.nalms.org/secchidipin/monitoring-methods/trophic-state-equations/)  						    |
| trophic_status                    | oligotrophic, mesotrophic, eutrophic, hypereutrophic | assigned using lake trophic status index															    																    |
| climate_zone                      | integer                                              | climate zone of the region where the lake is sampled, assigned using the HydroATLAS database 																								    |
| lake_elev                         | m above sea level                                    | elevation of the lake, extracted from the [Global Multi-resolution Terrain Elevation Data (GMTED2010)](https://www.usgs.gov/core-science-systems/eros/coastal-changes-and-impacts/gmted2010?qt-science_support_page_related_con=0#qt-science_support_page_related_con) model                   |
| lake_area                         | km<sup>2                                             | total lake surface area, extracted from the HydroLAKES database       																											    |
| lake_volume                       | m<sup>3                                              | total lake volume, extracted from the HydroLAKES database                  																										    |
| mean_lake_depth                   | m                                                    | mean lake depth, extracted from the HydroLAKES database                 																											    |
| year                              | integer                                              | year the PCI occurred            																														  		    |
| season                            | spring, summer, single                               | time of year when the PCI is detected 																															    |
| start_day                         | days (range from 1-365)                              | day of year that the PCI begins  																														   		    |
| end_day                           | days (range from 1-365)                              | day of year that the PCI ends   																																    |
| pci_length           		    | days                                                 | duration of the PCI, including the start and end dates       																												    |
| chla_rate                         | µgL<sup>-1</sup>day<sup>-1                           | rate of increase in chlorophyll-*a* concentration during the PCI   																											    |
| normalized chla rate		    | day<sup>-1					   | first derivative of the smoothed chlorophyll-a concentration over time divided by the original chlorophyll-a concentration																					    |
| max_chla                          | µgL<sup>-1                                           | maximum chlorophyll-*a* concentration reached during the PCI  																												    |
| acc_chla                          | µgL<sup>-1                                           | accumulated chlorophyll-*a* over the PCI, calculated using the numpy.trapz function   																									    |
| specific_chla_rate                | day<sup>-1                                           | chla_rate rate divided by initial concentration																														    |
| temp_corrected_specific_chla_rate | day<sup>-1                                           | specific chlorophyll-*a* rate corrected for the influence of temperature using the equation from [Rosso et al (1995)](https://journals.asm.org/doi/abs/10.1128/aem.61.2.610-616.1995)*    													    |
| poc_rate                          | mgL<sup>-1                                           | rate of increase or decrease in particulate organic carbon  from the start to the end of the PCI   																							    |
| chla_to_poc                       | mg chl-a : mg POC                                    | rate of change in chlorophyll-*a* in proportion to particulate organic carbon during the PCI           																							    |
| pci_temp                          | °C                                                   | mean surface water temperature during the PCI                     																										    		    |
| pci_tp                            | mgL<sup>-1                                           | mean total phosphorus during the PCI																															    |
| pci_secchi                        | m                                                    | mean Secchi depth during the PCI    																															    |
| pci_ph                            | pH units                                             | mean pH during the PCI            																														 		    |
| pci_srp                           | mgL<sup>-1                                           | mean soluble reactive phosphorus during the PCI             																												    |
| pci_tkn                           | mgL<sup>-1                                           | mean total Kjeldahl nitrogen during the PCI                     																												    |
| pre_pci_temp                      | °C                                                   | mean surface water temperature during the 14 days leading up to the PCI  																											    |
| pre_pci_tp                        | mgL<sup>-1                                           | mean total phosphorus during the 14 days leading up to the PCI    																												    |
| pre_pci_tkn                       | mgL<sup>-1                                           | mean total Kjeldahl nitrogen during the 14 days leading up to the PCI																											    |
| first_day_sampled		    | day of year					   | day of first sample collected that year (start of sampling season)																												    |
| last_day_sampled		    | day of year					   | day of last sample collected that year (end of sampling season)																												    |
| num_samples                       | integer                                              | number of days sampled that year; can be used to filter the dataset        																										    |
| sampling_frequency		    | samples per day					   | number of samples collected that year, divided by the number of days in the sampling season																								    |
| mean_time_between_samples	    | days  					           | average number of days between sample collection (sampling resolution)																										            |
| ssr_station                       | NA                                                   | station name as assigned in original database                                                                                                                                                                                                                                                  |
| ssr_id                            | NA                                                   | id number in original database (where available)                                                                                                                                                                                                                                               |
| ssr_id_type                       | NA                                                   | type of ID number (i.e., GEBA, Internal)  																															    |
| ssr_lat                           | decimal degrees                                      | SSR station latitude                                                                                                                                                                                                                                                    |
| ssr_long                          | decimal degrees                                      | SSR station longitude																														    |
| geo_dist_km                       | km                                                   | geodic distance between the paired lake and SSR station                    																										    |
| ssr_elev                          | m above sea level                                    | elevation of the SSR station, extracted from the [Global Multi-resolution Terrain Elevation Data (GMTED2010)](https://www.usgs.gov/core-science-systems/eros/coastal-changes-and-impacts/gmted2010?qt-science_support_page_related_con=0#qt-science_support_page_related_con) model            |
| ssr_lake_elev_diff                | m                                                    | difference in elevation between the paired lake ans SSR station (positive when ssr station is at a higher elevation)            																				    |
| pci_ssr                           | Wm<sup>-2                                            | mean solar radiation during the PCI 																															    |
| pre_pci_ssr                       | Wm<sup>-2                                            | mean solar radiation during the 14 days leading up to the PCI																									        		    |
                                                                                               

*calculation used for temperature correction:

		group.loc[:, 'f_temp'] = (mean_temp - t_max) * (mean_temp - t_min) ** 2 / ((t_opt - t_min) * ((t_opt - t_min) * (mean_temp - t_opt) - (t_opt - t_max) * (t_opt + t_min - 2 * mean_temp)))

        # divide specific growth rate by f_temp
        group.loc[:, 'temp_corrected_specific_chla_rate'] = group.loc[:, 'specific_chla_rate'] / group.loc[:, 'f_temp']

** see ssr\_data\_sources.csv in the associated FRDR repository for more information

## Additional documentation
HydroATLAS technical document and shapefile download is available through the [Hydrosheds HydroATLAS webpage](https://hydrosheds.org/page/hydroatlas).

HydroLAKES technical document and shapefile download is available through the [Hydrosheds HydroLAKES webpage](https://hydrosheds.org/page/hydrolakes) (includes more information regarding climate zone codes)

## References

Linke, S., Lehner, B., Ouellet Dallaire, C., Ariwi, J., Grill, G., Anand, M., … Thieme, M. (2019). Global hydro-environmental sub-basin and river reach characteristics at high spatial resolution. Scientific Data, 6(1), 1–15. [https://doi.org/10.1038/s41597-019-0300-6](https://doi.org/10.1038/s41597-019-0300-6)

Messager, M. L., Lehner, B., Grill, G., Nedeva, I., & Schmitt, O. (2016). Estimating the volume and age of water stored in global lakes using a geo-statistical approach. Nature Communications, 7, 1–11. [https://doi.org/10.1038/ncomms13603](https://doi.org/10.1038/ncomms13603)

