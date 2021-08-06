# Code for formatting and processing lake and solar radiation data

This folder contains the main scripts for the growth window dataset preparation. Order of use is as follows:

1. Basic formatting of original data files for consistent units and headings (code not provided since not all data is openly accessible)

2. Growth windows are calculated using the *growth\_window\_calculations.py* script, which calls on functions from the *growth\_window\_functions.py* file. The output is the growth window dataset without paired surface solar radiation data.

3. The growth window data file is imported into QGIS as a point vector layer, and the *ssr\_lakes\_pairing\_qgis.py*, *lakes\_dem\_extraction.py*, and *ssr\_dem\_extraction.py* scripts are opened in QGIS under plugins > Python console (usiing the "Show Editor" icon in the Python console to open and edit the scripts). 

	a) **ssr\_lakes\_pairing\_qgis.py** generates a copy of the lake points layer, with the paired SSR point data appended to each lake point along with distance between the lake and SSR stations

	b) **lakes\_dem\_extraction.py** generates a copy of the imported lake points layer, with the lake elevation, area, volume, and depth added

	c) **ssr\_dem\_extraction.py** generates a copy of the input SSR points layer, with the SSR elevation added.

	Attributes from these generated layers are then merged with the growth window dataset.


4. SSR growth window and pre-growth window means are calculated using the *paired\_stations\_ssr\_calcs.py* script.

## Scripts

### Lakes
* growth\_window\_calculations.py
* growth\_window\_functions.py

### QGIS
* ssr\_lakes\_pairing\_qgis.py
* lakes\_dem\_extraction.py
* ssr\_dem\_extraction.py

### Solar radiation
* paired\_stations\_ssr\_calcs.py


## Software and packages
* [Python (version 3.7.6)](https://www.python.org/downloads/release/python-376/)
* [QGIS (version 3.16)](https://qgis.org/en/site/forusers/download.html)

#### General
* [Pandas library](https://pandas.pydata.org/)
* [NumPy library](https://numpy.org/)
* [Dplython library](https://pythonhosted.org/dplython/)
* [glob module](https://docs.python.org/3.7/library/glob.html)

#### Growth window analysis
* [scipy.signal find_peaks function](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html)
* [scipy.signal savgol_filter function](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html)

#### Plotting
* [Matplotlib library](https://matplotlib.org/)
* [Ptitprince package](https://pypi.org/project/ptitprince/)
* [RainCloudPlots package](https://github.com/RainCloudPlots/RainCloudPlots)
* [Seaborn library](https://seaborn.pydata.org/)


## References

Allen M, Poggiali D, Whitaker K et al. (2021). Raincloud plots: a multi-platform tool for robust data visualization [version 2.0.5; peer review: 2 approved]. *Wellcome Open Res*. 4:63. DOI:[10.12688/wellcomeopenres.15191.2](https://wellcomeopenresearch.org/articles/4-63/v1)

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., … Oliphant, T. E. (2020, September). Array programming with NumPy. Nature, Vol. 585, pp. 357–362. [https://doi.org/10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)

Hunter, J.D. (2007). Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*. 9:3, 90-95. DOI: [10.1109/MCSE.2007.55](https://ieeexplore.ieee.org/document/4160265)

Poggiali, Davide. (2018). Ptitprince python package. GitHub repository:[https://github.com/pog87/PtitPrince](https://github.com/pog87/PtitPrince)

Python Software Foundation. (2021). Python Language. [https://www.python.org/](https://www.python.org/)

QGIS Development Team. (2021). QGIS Geographic information system. [http://qgis.osgeo.org](http://qgis.osgeo.org)

Riederer, C. (2015). Dplython. Retrieved from GitHub repository website: [https://github.com/dodger487/dplython](https://github.com/dodger487/dplython)

Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., … Vázquez-Baeza, Y. (2020). SciPy 1.0: fundamental algorithms for scientific computing in Python. Nature Methods, 17(3), 261–272. [https://doi.org/10.1038/s41592-019-0686-2](https://doi.org/10.1038/s41592-019-0686-2)

Waskom, M. L., (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021, [https://doi.org/10.21105/joss.03021](https://joss.theoj.org/papers/10.21105/joss.03021)





