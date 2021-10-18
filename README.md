# Daily published numbers by the Robert Koch Institut

## First data mining project

#### DATA MINING
This is my first _data mining_ project collecting the (then) daily published numbers by the RKI, as I wanted a data set created by myself for further usage. Using **python** and the **beautiful soup** module (bs4) the [RKI webiste](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html "numbers published") is read in, the data of the relevant tags is extracted and cleaned up to be put into a dictionary, which will be strored in **json** format. These tags were found by going through the source code of the website using the inspect tool and need to be updated occasionally, as the webiste content (more specific its order) is updated from time to time, but lacking specific identifiers (e.g. a "published date" tag).

![Demo json data](https://github.com/RoKaruto/Collecting-numbers-from-the-RKI/blob/main/rki%20json%20example.png "json data")

---

#### DATA VISUALIZATION
Using the **matplotlib.pyplot** module in **python**, several line plots of the json data will be created, the option of choosing the timeframe, counties and specific plots is given, moreover a list of dates with no publication by the RKI will can be attached to the plot.

![Demo RKI plots](https://github.com/RoKaruto/Collecting-numbers-from-the-RKI/blob/main/rki_plot1.png "RKI plots")
![Demo RKI plots](https://github.com/RoKaruto/Collecting-numbers-from-the-RKI/blob/main/rki_plot2.png "RKI plots")
                  
