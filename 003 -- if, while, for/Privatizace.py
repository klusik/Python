import PySimpleGUI as gui



layout=[[gui.Text("Ahoj, tohle bude úžasná hra, jednou.")],[gui.Button("Oki"), gui.Button("Nope")]]

gui.Window(title="Privatizace", layout=layout, margins=(800,400)).read()

