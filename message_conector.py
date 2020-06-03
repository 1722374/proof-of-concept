import webbrowser
import json

def tigger_route(msg):
   f = open('command.json')
   commands = json.load(f)
   webbrowser.open_new_tab(commands[msg.decode('ascii')])