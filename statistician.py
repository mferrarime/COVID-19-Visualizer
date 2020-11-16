import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import pandas as pd
import requests

class Stats:
    def __init__(self, region, query):
        self.region = region
        self.query = query

    def update(self):
        url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"
        req = requests.get(url, allow_redirects=True)
        open("data.csv", "wb").write(req.content)

    def set(self, region, query):
        self.region = region
        self.query = query

    def plot(self):
        df = pd.read_csv("data.csv")

        df.drop("stato", axis=1, inplace=True)
        df.drop("codice_regione", axis=1, inplace=True)
        df.drop("lat", axis=1, inplace=True)
        df.drop("long", axis=1, inplace=True)
        df.drop("note", axis=1, inplace=True)

        df["data"] = df["data"].str[0:10]
        df.sort_values(by=["denominazione_regione", "data"])

        df = df.filter(["data", "denominazione_regione", self.query], axis=1)
        df = df.set_index("denominazione_regione").filter(like=self.region, axis=0)
        df.set_index("data", inplace=True)

        df.plot(grid=True)
        plt.xlabel("timestamp")
        plt.ylabel("values")
        plt.show()
