from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as gui
from statistician import Stats

def draw_figure(canvas, figure):
    fig_canvas = FigureCanvasTkAgg(figure, canvas)
    fig_canvas.draw()
    fig_canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
    return fig_canvas

def delete_figure(figure):
    figure.get_tk_widget().pack_forget()
    figure.get_tk_widget().delete("all")

def data_check(stats):
    try:
        file = open("data/data.csv")
    except IOError:
        stats.update()

def main():
    # setting
    gui.theme("DarkTeal9")
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
                [gui.Button("Plot"), gui.Button("Download data"), gui.Button("Close")],
                [gui.Canvas(key="PLOT")]
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

    stats = Stats("Abruzzo", "Ricoverati con sintomi")
    data_check(stats)

    fig_canvas = draw_figure(window["PLOT"].TKCanvas, stats.plot())

    # looping
    while True:
        event, values = window.read()
        fig_canvas.flush_events()

        if event == "Plot":
            stats.set(values[0], values[1])
            delete_figure(fig_canvas)
            fig_canvas = draw_figure(window["PLOT"].TKCanvas, stats.plot())
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
