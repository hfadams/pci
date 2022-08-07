# Code for formatting and processing lake and solar radiation data

This folder contains the main scripts for the growth window dataset preparation. Order of use is as follows:

1. Basic formatting of original data files for consistent units and headings (code not provided since not all data is openly accessible)

2. PCIs are calculated using the *pci_calculations.py* script, which calls on functions from the *pci_functions.py* file. The output is the PCI dataset without paired surface solar radiation data.

3. The PCI data file is imported into QGIS as a point vector layer, and the *ssr\_lakes\_pairing\_qgis.py*, *lakes\_dem\_extraction.py*, and *ssr\_dem\_extraction.py* alongside the [Global Multi-resolution Terrain Elevation Data (GMTED2010)](https://www.usgs.gov/core-science-systems/eros/coastal-changes-and-impacts/gmted2010?qt-science_support_page_related_con=0#qt-science_support_page_related_con) model.

	a) **ssr\_lakes\_pairing\_qgis.py** generates a copy of the lake points layer, with the paired SSR point data appended to each lake point along with distance between the lake and SSR stations

	b) **lakes\_dem\_extraction.py** generates a copy of the imported lake points layer, with the lake elevation, area, volume, and depth added

	c) **ssr\_dem\_extraction.py** generates a copy of the input SSR points layer, with the SSR elevation added.

	Attributes from these generated layers are then merged with the PCI dataset.


4. SSR PCI and pre-PCI means are calculated using the *paired\_stations\_ssr\_calcs.py* script.

## Scripts

### Lakes
* pci_calculations.py
* pci_functions.py

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
* [Pandas library (version 1.3.1)](https://pandas.pydata.org/)
* [NumPy library (version 1.21.1)](https://numpy.org/)
* [Dplython library (version 0.0.4)](https://pythonhosted.org/dplython/)
* [glob module](https://docs.python.org/3.7/library/glob.html)

#### PCI detection
* [scipy.signal find_peaks function (SciPy version 1.4.1)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html)
* [scipy.signal savgol_filter function (SciPy version 1.4.1)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html)

#### Plotting
* [Matplotlib library (version 3.4.2)](https://matplotlib.org/)
* [Ptitprince package (version 0.2.5)](https://pypi.org/project/ptitprince/)
* [RainCloudPlots package (version 2)](https://github.com/RainCloudPlots/RainCloudPlots)
* [Seaborn library (version 0.11.1)](https://seaborn.pydata.org/)


## References

Allen M, Poggiali D, Whitaker K et al. (2021). Raincloud plots: a multi-platform tool for robust data visualization [version 2.0.5; peer review: 2 approved]. *Wellcome Open Res*. 4:63. DOI:[10.12688/wellcomeopenres.15191.2](https://wellcomeopenresearch.org/articles/4-63/v1)

Danielson, J., and Gesch, D. (2010). Global Multi-resolution Terrain Elevation Data (GMTED2010). *US Geological Survey* [https://pubs.usgs.gov/of/2011/1073/pdf/of2011-1073.pdf](https://pubs.usgs.gov/of/2011/1073/pdf/of2011-1073.pdf).

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., … Oliphant, T. E. (2020, September). Array programming with NumPy. Nature, Vol. 585, pp. 357–362. [https://doi.org/10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)

Hunter, J.D. (2007). Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*. 9:3, 90-95. DOI: [10.1109/MCSE.2007.55](https://ieeexplore.ieee.org/document/4160265)

Poggiali, Davide. (2018). Ptitprince python package. GitHub repository:[https://github.com/pog87/PtitPrince](https://github.com/pog87/PtitPrince)

Python Software Foundation. (2021). Python Language. [https://www.python.org/](https://www.python.org/)

QGIS Development Team. (2021). QGIS Geographic information system. [http://qgis.osgeo.org](http://qgis.osgeo.org)

Riederer, C. (2015). Dplython. Retrieved from GitHub repository website: [https://github.com/dodger487/dplython](https://github.com/dodger487/dplython)

Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., … Vázquez-Baeza, Y. (2020). SciPy 1.0: fundamental algorithms for scientific computing in Python. Nature Methods, 17(3), 261–272. [https://doi.org/10.1038/s41592-019-0686-2](https://doi.org/10.1038/s41592-019-0686-2)

Waskom, M. L., (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021, [https://doi.org/10.21105/joss.03021](https://joss.theoj.org/papers/10.21105/joss.03021)





