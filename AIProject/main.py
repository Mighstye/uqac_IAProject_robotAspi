import PySimpleGUI as sg


layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

# Create window
window = sg.Window("Demo", layout)

# Create event loop
while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
