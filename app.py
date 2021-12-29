from src.Spreadsheets import Spreadsheet
from src.Commands import CommandInterpreter

def main():
    spr = Spreadsheet()
    cmd_inter = CommandInterpreter(spr)
    while True:
        inp = input('>')
        resp = cmd_inter.parse_command(inp)
        print(resp)
        print(spr.spreadsheet_view())



if __name__ == '__main__':
    main()
