import gc
import PySimpleGUI as gui
from statistician import Stats

# needed for Tkinter
import matplotlib
matplotlib.use("TkAgg")

def data_check(stats):
    try:
        file = open("data/region_data.csv")
        file = open("data/nation_data.csv")
        del file
    except IOError:
        stats.update()

def main():
    # setting
    gui.theme("DarkTeal6")
    layout = [  [gui.Text("Remember to 'Download data' if you want more recent data")],
                [gui.Text("Which region?", size=(25, 1)), gui.InputCombo((
                    "Italia",
                    "Abruzzo",
                    "Basilicata",
                    "Calabria",
                    "Campania",
                    "Emilia-Romagna",
                    "Friuli Venezia Giulia",
                    "Lazio",
                    "Liguria",
                    "Lombardia",
                    "Marche",
                    "Molise",
                    "P.A. Bolzano",
                    "P.A. Trento",
                    "Piemonte",
                    "Puglia",
                    "Sardegna",
                    "Sicilia",
                    "Toscana",
                    "Umbria",
                    "Valle d'Aosta",
                    "Veneto"
                    ), enable_events=True, default_value="Italia")],
                [gui.Text("What do you want to visualize?", size=(25, 1)), gui.InputCombo((
                    "Ricoverati con sintomi",
                    "Terapia intensiva",
                    "Totale ospedalizzati",
                    "Isolamento domiciliare",
                    "Totale positivi",
                    "Variazione totale positivi",
                    "Nuovi positivi",
                    "Dimessi guariti",
                    "Deceduti",
                    "Casi da sospetto diagnostico",
                    "Casi da screening",
                    "Totale casi",
                    "Tamponi",
                    "Casi testati"
                    ), enable_events=True, default_value="Variazione totale positivi")],
                [gui.Button("Plot"), gui.Button("Download data"), gui.Button("Close")],
                [gui.Image(key="PLOT", size=(20, 10))]
            ]

    # initializing
    window = gui.Window("Coronavirus Data",
        auto_size_buttons=True,
        finalize=True,
        font="Helvetica 11",
        icon=r"icons/favicon.ico",
        layout=layout,
        resizable=True
        )
    window.Maximize()

    stats = Stats("Italia", "Variazione totale positivi")
    data_check(stats)

    stats.plot()
    window.Element("PLOT").Update(filename="data/fig.png")

    # looping
    while True:
        event, values = window.read()
        gc.collect()

        if event == "Plot":
            stats.set(values[0], values[1])
            stats.plot()
            window.Element("PLOT").Update(filename="data/fig.png")
        elif event == "Download data":
            stats.update()
        elif event == "Close" or event == gui.WIN_CLOSED:
            break
        else:
            pass

    # closing
    window.close()
    del window

if __name__ == "__main__":
    main()
