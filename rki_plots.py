import json
import codecs
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


def date_to_ddmmyyyy(dat="1981_01_24", separator="."):
    """Takes the date in string format YYYY_MM_DD from csv and transforms it into DD.MM.YYYY, separator default can
       be reset to different symbol, leading zeroes will be filled (1 -> 01)"""
    return f'{dat.split("_")[2]}{separator}{(str(int(dat.split("_")[1]))).zfill(2)}{separator}' \
           f'{(str(int(dat.split("_")[0]))).zfill(2)}'


if __name__ == "__main__":

    date_from = "2021_04_08"
    date_to = dt.date.today().strftime("%Y_%m_%d")

    # date_from = "2021_05_01"
    # date_to = "2021_08_02"

    date_from_dt = dt.datetime.strptime(date_from, "%Y_%m_%d")
    date_to_dt = dt.datetime.strptime(date_to, "%Y_%m_%d")
    dates_in_timeframe_dt = [date_from_dt + dt.timedelta(days=x) for x in range((date_to_dt - date_from_dt).days)]

    with codecs.open("./data/rki_data.json", "r", encoding="utf-8") as f:
        rki_data = json.load(f)

    all_dates = list(rki_data.keys())

    dates = []
    if date_from and date_to:
        for d in all_dates:
            if date_from <= d <= date_to:
                dates.append(d)
    else:
        dates = all_dates

    dates_missing = [dt.datetime.strftime(d, "%Y_%m_%d") for d in dates_in_timeframe_dt
                     if dt.datetime.strftime(d, "%Y_%m_%d") not in all_dates]
    dates_missing_fmted = [date_to_ddmmyyyy(d) for d in dates_missing]      # dates missing formatted to DD.MM.YYYY

    info_line = "Keine Daten veröffentlicht: "     # attached to plot to list all dates, where no data was provided
    lb_c = 0   # linebreak counter
    for d in dates_missing_fmted[:-1]:
        lb_c += 1
        this_d = d.split('.')[:-1]
        info_line += f"{this_d[0]}.{this_d[1]}., "
        if lb_c % 12 == 0:
            info_line += "\n"
    info_line = info_line[:-3]
    info_line += f" und {dates_missing_fmted[-1]}."

    ###################################
    # PLOTS FOR ALL COUNTIES, ALL NUMBERS

    num_names = ["Anzahl", "Differenz zum Vortag", "Fälle in den letzten 7 Tagen", "7-Tage-Inzidenz", "Todesfälle"]
    colors = ["black", "dimgray", "yellow", "lightcoral", "maroon", "crimson", "goldenrod", "silver", "darkgreen",
              "lime", "aquamarine", "steelblue", "dodgerblue", "navy", "mediumorchid", "purple", "deeppink"]

    counties = list(rki_data[dates[0]].keys())

    counties_raw = counties[:-1]    # "Gesamt" in last position will be left out (as it's the median of all counties)
    counties = [c[:-1] if c[-1:] == "*" else c for c in counties_raw]   # remove *, if county names contain these

    dats = list(dates)          # list of dates as strings

    dates_plot = []             # rewrite the dates for plots to DD.MM.YYYY format
    for _ in dats:
        if _ in dats:
            dates_plot.append(f'{_.split("_")[2]}.{(_.split("_")[1]).zfill(2)}.{(_.split("_")[0]).zfill(2)}')

    for num in num_names:       # loop through all five categories of numbers from RKI website
        these_numbers = {}      # create a new dictionary for respectice number
        for county in counties:     # loop through counties and create a key value pair -> county : numbers (as list)
            if county[:-1] != "*" and county not in these_numbers.keys():   # add key only, if not already added
                these_numbers[county] = []

        for date in dates:              # loop through all keys in rki json -> date with YYYY_MM_DD format
            for county in counties:     # loop through all counties

                try:                    # catch the entries with * attached (annotation on website of that day)
                    these_numbers[county].append(rki_data[date][county][num])
                except KeyError:
                    this_data = rki_data[date][county+"*"][num]
                    these_numbers[county].append(this_data)

        plt.figure(figsize=(10, 7), dpi=100)   # new plot
        plt.grid()
        plt.subplots_adjust(bottom=0.15, right=.75)  # leave space for x-ticks at bottom and legend on the right
        plt.title(f"{num}\n{dates_plot[0]} - {dates_plot[-1]}")  # title = the description of the respective num-entry

        col = 0   # color counter to go through list with colors (automatic only 8 -> repetitive)
        lines = []
        for county in counties:
            plt.plot(dates_plot, these_numbers[county], label=county, color=colors[col])
            col += 1

        plt.xticks(rotation=90)

        if len(dates_plot) > 30:    # limit the number of x-ticks if timeframe > month (readability of x-axis)
            plt.xticks(np.arange(0, len(dates_plot), int(len(dates_plot) / 30)))

        plt.legend(bbox_to_anchor=[1.05, 1.0])
        plt.subplots_adjust(bottom=0.18)
        plt.figtext(0.5, 0.01, info_line, ha="center", fontsize=7)
        filename = f"../plots/all_{num}-{dats[0]}-{dats[-1]}"
        plt.savefig(filename)

    plt.show()
