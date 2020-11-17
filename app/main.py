import PySimpleGUI as gui
from statistician import Stats

def data_check(stats):
    try:
        file = open("data/data.csv")
    except IOError:
        stats.update()

def main():
    # setting
    gui.theme("Topanga")
    layout = [  [gui.Text("Remember to 'Download data' if you want more recent data")],
                [gui.Text("Which region?", size=(25, 1)), gui.InputCombo((
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
                    ), enable_events=True, default_value="Abruzzo")],
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
                    ), enable_events=True, default_value="Ricoverati con sintomi")],
                [gui.Button("Plot"), gui.Button("Download data"), gui.Button("Close")]
            ]

    # initializing
    window = gui.Window("Coronavirus Data",
        auto_size_text=True,
        auto_size_buttons=True,
        icon=r"icons/favicon.ico",
        size=(500, 120)
        ).Layout(layout)

    stats = Stats("Abruzzo", "ricoverati_con_sintomi")
    data_check(stats)

    # looping
    while True:
        event, values = window.read()

        if event == "Plot":
            stats.set(values[0], values[1].lower().replace(" ", "_"))
            stats.plot()
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
