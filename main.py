from statistician import Stats
import PySimpleGUI as gui

gui.theme("Topanga")
layout = [  [gui.Text("Remember to 'Download data' if you have no .csv files to analize")],
            [gui.Text("Which region?", size=(20, 1)), gui.InputCombo((
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
                ), size=(20, 1), enable_events=True, default_value="Abruzzo")],
            [gui.Text("What do you want to visualize?", size=(20, 1)), gui.InputCombo((
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
                ), size=(20, 1), enable_events=True, default_value="Ricoverati con sintomi")],
            [gui.Button("Plot"), gui.Button("Download data"), gui.Button("Close")]
        ]

window = gui.Window("Coronavirus Data", size=(500, 130)).Layout(layout)

stats = Stats("Abruzzo", "ricoverati_con_sintomi")
while True:
    event, values = window.read()
    stats.set(values[0], values[1].lower().replace(" ", "_"))

    if event == "Plot":
        stats.plot()
    elif event == "Download data":
        stats.update()
    elif event == "Close" or event == gui.WIN_CLOSED:
        break

window.close()
del window
