import gc
import math
import matplotlib.dates as dates
from matplotlib.dates import MO
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import requests

class Stats:
    __shared_state = {}

    def __init__(self, region, query):
        self.__dict__ = self.__shared_state
        
        # setting region and query
        self.region = region
        self.query = query

    def set(self, region, query):
        self.region = region
        self.query = query

    def update(self):
        self.region_update()
        self.nation_update()

    def nation_update(self):
        url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
        req = requests.get(url, allow_redirects=True)
        open("data/nation_data.csv", "wb").write(req.content)

    def region_update(self):
        url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"
        req = requests.get(url, allow_redirects=True)
        open("data/region_data.csv", "wb").write(req.content)

    def df_selector(self, region):
        if self.region == "Italia":
            #reading csv
            try:
                df = pd.read_csv("data/nation_data.csv")
            except:
                self.nation_update()
                df = pd.read_csv("data/nation_data.csv")

            # check if the dataframe is cleared
            df = self.dropper(df)
        else:
            try:
                df = pd.read_csv("data/region_data.csv")
            except:
                self.region_update()
                df = pd.read_csv("data/region_data.csv")

            df = self.dropper(df)

        return df

    def dropper(self, df):
        if self.region == "Italia":
            return self.nation_dropper(df)
        else:
            return self.region_dropper(df)

    def nation_dropper(self, df):
        # clearing from unused data, pass if already dropped
        try:
            df.drop("note", axis=1, inplace=True)

            df["data"] = df["data"].str[0:10]
            df.sort_values(by=["stato", "data"])

            # take only timestamp and query
            df = df.filter(["data", "stato", self.query], axis=1)

            # index by 'stato'
            df = df.set_index("stato")
        except:
            pass

        return df

    def region_dropper(self, df):
        # clearing from unused data, pass if already dropped
        try:
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
        except:
            pass

        return df

    def plot(self):
        # save for the legend_label, then reformat for query
        legend_label = self.query
        self.query = legend_label.lower().replace(" ", "_")

        # select the right dataframe
        dropped_df = self.df_selector(self.region)

        # set last_value_y, used to print text of the last value
        last_value_y = dropped_df.iloc[-1][self.query]

        # set start and end data retrival date, create a new index and drop 'data'
        start = dropped_df.iloc[0]["data"]
        end = dropped_df.iloc[-1]["data"]
        dropped_df.set_index(pd.date_range(start=start, end=end, freq="D"), inplace=True)
        dropped_df.drop("data", axis=1, inplace=True)

        # separate positive values from negative values
        pos = dropped_df.clip(lower=0)
        neg = dropped_df.clip(upper=0.01)

        # plot everything, throw exception when there are no negative values
        fig, ax = plt.subplots()
        max, min = 0, 0
        try:
            pos.plot.area(ax=ax, color="firebrick", linewidth=1.1, stacked=False)
            max = pos.sum(axis=1).max()

            neg.plot.area(ax=ax, color="royalblue", linewidth=1.1, stacked=False)
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
        ax.set_ylim([min + math.ceil(min/5), max + math.ceil(max/5)])
        ax.grid(color="gray", linestyle="-", linewidth=0.07)
        ax.set_title(label=self.region, loc="center")
        ax.legend([legend_label], loc="upper center")
        fig.autofmt_xdate()
        fig.set_size_inches(20.0, 10.0)
        plt.text(x=ax.get_xlim()[1] + 1.7,
            y=last_value_y,
            s=int(last_value_y),
            color="gray",
            fontsize=9,
            fontweight="demi",
            fontstyle="italic")

        plt.savefig("data/fig.png", dpi=100, facecolor="snow", format="PNG")
        plt.close("all")
        gc.collect()
