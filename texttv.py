import requests
import os
from colorama import Fore, Back

COLORS = {
    "green": '\033[92m',
    "ggreen": '\033[92m',
    "white": '\33[97m',
    "gwhite": '\33[97m',
    "cyan": '\033[96m',
    "gcyan": '\033[96m',
    "blue": '\033[94m',
    "gblue": '\033[94m',
    "red": '\033[91m',
    "black": '\033[0m'
}

FG_COLORS = {
    "green": Fore.GREEN,
    "ggreen": Fore.GREEN,
    "white": Fore.WHITE,
    "gwhite": Fore.WHITE,
    "cyan": Fore.CYAN,
    "gcyan": Fore.CYAN,
    "blue": Fore.BLUE,
    "gblue": Fore.BLUE,
    "red": Fore.RED,
    "black": Fore.BLACK
}

BG_COLORS = {
    "green": Back.GREEN,
    "ggreen": Back.GREEN,
    "white": Back.WHITE,
    "gwhite": Back.WHITE,
    "cyan": Back.CYAN,
    "gcyan": Back.CYAN,
    "blue": Back.BLUE,
    "gblue": Back.BLUE,
    "red": Back.RED,
    "black": Back.BLACK
}

api_id = os.getenv("YLE_APP_ID", "")
api_key = os.getenv("YLE_APP_KEY", "")
base_url = "https://external.api.yle.fi/v1/teletext/pages/{}.json?app_id="+ \
            api_id + "&app_key=" + api_key
clear = lambda: os.system('clear')

def get_page(page_num):
    url = base_url.format(page_num)
    res = requests.get(url)
    try:
        return res.json()
    except:
        return None

def get_fg_color(run):
    fg_color = ""
    try:
        fg_color = FG_COLORS[run["fg"]]
    except:
        fg_color = FG_COLORS["white"]
    return fg_color

def get_bg_color(run):
    bg_color = ""
    try:
        bg_color = BG_COLORS[run["bg"]]
    except:
        bg_color = BG_COLORS["black"]
    return bg_color

def print_page(page):
    lines = page["teletext"]["page"]["subpage"][0]["content"][2]["line"]
    for line in lines:
        print_line = ""
        text_length = 0
        if type(line["run"]) == dict:
            run = line["run"]
            bg_color = get_bg_color(run)
            text_color = get_fg_color(run)
            try:
                try:
                    text = ord(run["charcode"])
                except Exception as e:
                    text = run["Text"]
                
            except:
                try:
                    text = " "*int(run["length"])
                except:
                    pass
            print_line += bg_color + text_color + text
            text_length += len(text)
            if text_length < 40:
                print_line = print_line + " "*(40-text_length)
            print(print_line)
            continue

        for run in line["run"]:
            bg_color = get_bg_color(run)
            text_color = get_fg_color(run)
            try:
                try:
                    text = run["charcode"]
                    text = " "
                except Exception as e:
                    text = run["Text"]
                    if len(text) > 4 and text[0] == text[1] and text[0] == text[2] and text[0] == text[2] and text[0] != " " and text[0] != "-":
                        text = " "*40
            except:
                try:
                    text = " "*int(run["length"])
                except:
                    pass
            print_line += bg_color + text_color + text
            text_length += len(text)
        if text_length < 40:
            print_line = print_line + " "*(40-text_length)
        if text_length > 40:
            print(line)
        print(print_line)
    
    print(COLORS["white"] + COLORS["black"])

def main():
    while True:
        page = input("> ")
        if page == "q":
            break
        if len(page) != 3:
            continue
        clear()
        print(page)
        page_json = get_page(page)
        if page_json:
            print_page(page_json)
        else:
            continue

if __name__ == "__main__":
    main()
