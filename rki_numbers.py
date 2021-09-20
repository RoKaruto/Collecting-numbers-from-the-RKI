# -*- coding: UTF-8 -*-
import bs4
import requests
import json
import datetime as dt
import codecs


if __name__ == "__main__":
    today = dt.date.today().strftime("%Y_%m_%d")        # date format for json file
    response = requests.get(url="https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html")
    response.raise_for_status()
    website = response.text                             # read out the html code as text
    soup = bs4.BeautifulSoup(website, "html.parser")    # make soup
    
    ''' find date of published numbers and transform to YYYY_MM_DD '''
    curr_date = soup.findAll("p")  # the date of publication is in one of the "all p" - list, changes from time to time
    curr_dat1 = []
    for _ in curr_date:                             # filter all <p> tags with "Stand: " (followed by a date)
        if str(_)[0:10] == "<p>Stand: ":
            curr_dat1.append(str(_))
    curr_dat1 = curr_dat1[0].split(" ")[2]          # grab only the date from relevant p string
    curr_dat1 = curr_dat1[:-1]                      # remove last position (",")
    currdate = f'{curr_dat1.split(".")[2]}_{(str(int(curr_dat1.split(".")[1]))).zfill(2)}_' \
               f'{(str(int(curr_dat1.split(".")[0]))).zfill(2)}'
    #            └-> rearrange year, month and date, separate by "_" and fill zeroes if needed (e.g. 2 -> 02)
    
    if currdate != today:
        print(f"Die Zahlen für den {today.split('_')[2] + '.' + today.split('_')[1] + '.' + today.split('_')[0]}"
              f" wurden vom RKI noch nicht veröffentlicht. "
              f"({dt.datetime.strftime(dt.datetime.now().now(), '%H:%M')} Uhr)")
    else:
        # filename = f"./venv/data/{currdate}_data.json"
    
        num_names = ["Anzahl", "Differenz zum Vortag", "Fälle in den letzten 7 Tagen", "7-Tage-Inzidenz", "Todesfälle"]
        #         └-> list of keys needed in the dict, which will be transformed to json
    
        ''' check for latest numbers recorded '''
    
        with open("./venv/data/rki_data.json", "r") as f:
            curr_json = json.load(f)
    
        try:
            last_data = (curr_json[currdate])
        except KeyError:        # if current date is not in the keys of the json dict, data has not been saved yet
            all_data = soup.find_all(name="td", rowspan="1")   # all numbers in the html code are a <td> with rowspan=1
    
            rki_zahlen_heute = {currdate: {}}  # dictionary for the numbers of today with date as 1st key, value - nums)
            for i in range(len(all_data)):
                if i % 6 == 0:   # every row consists out of 6 entries, meaning, after 6 iterations, a new county starts
                    county = {}  # the county, which will be a key of its on own (e.g. Berlin)
                    county_nums = {}  # the numbers of this county
                    for j in range(1, 6):    # the first one can be skipped (it's the county name), so 1 to excluding 6
                        county_nums[num_names[j - 1]] = float(all_data[i + j].text.replace(".", "").replace("*", "").
                                                              replace(",", "."))  # since 2021_07_21 7d inci dType float
                        #               └-> iterate through the <td>'s of this line, keys - see list, values - the entry
                    county[str(all_data[i].text.replace("­", ""))] = county_nums  # remove weird strings from html
                    rki_zahlen_heute[currdate].update(county)       # "add" completed county to the dictionary
            # print(rki_zahlen_heute)  # for testing purposes
    
            '''write rkidata.json file'''
    
            with codecs.open("./venv/data/rki_data.json", "a", encoding="utf-8") as f:
                json.dump(rki_zahlen_heute, f, indent=2, ensure_ascii=False)
    
            with open("./venv/data/rki_data.json", "r") as f:
                incorr_json = f.read()  # instead of a ",", the content is added as a new dict, which will be...
    
            corr_json = incorr_json.replace("}{", ",")    # ... the only "}{" in the file, so simply replace it ...
            with open("./venv/data/rki_data.json", "w") as f:
                f.write(corr_json)                        # ... and rewrite the file in correct json format
            print(f"Die vom RKI veröffenlichten Zahlen für den {dt.date.today().strftime('%d.%m.%Y')} wurden ausgelesen"
                  f" und gespeichert.")
        else:
            print(f"Die vom RKI veröffenlichten Zahlen für den {dt.date.today().strftime('%d.%m.%Y')} wurden bereits "
                  f"ausgelesen und gespeichert.")
