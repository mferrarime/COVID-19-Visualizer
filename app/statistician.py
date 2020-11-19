import math
import matplotlib.dates as dates
from matplotlib.dates import MO
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import requests

class Stats:
    def __init__(self, region, query):
        # setting region and query
        self.region = region
        self.query = query

    def update(self):
        url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"
        req = requests.get(url, allow_redirects=True)
        open("data/data.csv", "wb").write(req.content)

    def set(self, region, query):
        self.region = region
        self.query = query

    def plot(self):
        # clearing from unused data
        df = pd.read_csv("data/data.csv")

        df.drop("stato", axis=1, inplace=True)
        df.drop("codice_regione", axis=1, inplace=True)
        df.drop("lat", axis=1, inplace=True)
        df.drop("long", axis=1, inplace=True)
        df.drop("note", axis=1, inplace=True)

        df["data"] = df["data"].str[0:10]
        df.sort_values(by=["denominazione_regione", "data"])

        # take only timestamp, region and query
        df = df.filter(["data", "denominazione_regione", self.query], axis=1)

        # take data only from the selected region
        df = df.set_index("denominazione_regione").filter(like=self.region, axis=0)

        # set last_value_y, used to print text of the last value
        last_value_y = df.iloc[-1][self.query]

        # set start and end data retrival date, create a new index and drop 'data'
        start = df.iloc[0]["data"]
        end = df.iloc[-1]["data"]
        df.set_index(pd.date_range(start=start, end=end, freq="D"), inplace=True)
        df.drop("data", axis=1, inplace=True)

        # separate positive values from negative values
        pos = df.clip(lower=0)
        neg = df.clip(upper=0.01)

        # plot everything, throw exception when there are no negative values
        fig, ax = plt.subplots()
        max, min = 0, 0
        try:
            pos.plot.area(ax=ax, stacked=False, linewidth=1.1)
            max = pos.sum(axis=1).max()

            neg.plot.area(ax=ax, stacked=False, linewidth=1.1)
            min = neg.sum(axis=1).min()
        except:
            pass

        # set x axis
        ax.set_xlabel("week")
        plt.axhline(0, color="k")
        ax.xaxis.set_major_locator(dates.WeekdayLocator(byweekday=MO, interval=1))
        ax.xaxis.set_major_formatter(dates.DateFormatter("%m-%d"))

        # set y axis
        ax.set_ylabel("value")

        # plot other details
        ax.set_ylim([min + math.ceil(min/10), max + math.ceil(max/10)])
        ax.grid(color="gray", linestyle="-", linewidth=0.07)
        ax.set_title(label=self.region, loc="center")
        ax.legend([self.query], loc="upper center")
        plt.gcf().autofmt_xdate()
        plt.get_current_fig_manager().resize(1500, 700)
        plt.text(x=ax.get_xlim()[1] + 1.7,
            y=last_value_y,
            s=int(last_value_y),
            color="gray",
            fontsize=9,
            fontweight="demi",
            fontstyle="italic")

        plt.show()
