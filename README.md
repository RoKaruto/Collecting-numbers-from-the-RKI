# Daily published numbers by the Robert Koch Institut

## First data mining project

#### DATA MINING
This is my first _data mining_ project collecting the (then) daily published numbers by the RKI, influenced by the pandemid and my "free" time connected to it and the fact, that I wanted an own assembled data set to manipulate in python. Using **python** and the **beautiful soup** module (bs4) the [RKI webiste](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html "numbers published") is read in, the data of the relevant tags is extracted and cleaned up to be put into a dictionary, which will be strored in **json** format. These tags were found by going through the source code of the website using the inspect tool. These needed to be adjusted, as the webiste content was updated several times, but lacking specific identifiers (e.g. a "published date tag").

![Demo json data](https://github.com/RoKaruto/Collecting-numbers-from-the-RKI/blob/main/rki%20json%20example.png "json data")

---

#### DATA VISUALIZATION
Using the **matplotlib.pyplot** module in **python**, a collection of simple line plots of the numbers in the json file will be created, the timeframe is choosable and a list of dates with no publication by the RKI will be attached to the plot.

![Demo RKI plots](https://github.com/RoKaruto/Collecting-numbers-from-the-RKI/blob/main/RKI%20plots%20example.png "RKI plots")
                  
