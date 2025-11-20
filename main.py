import os
import random
import webbrowser
import time
import threading
import shutil
import json


# CONFIG

default_config = {
    "firsttime": True,
    "username": None,
    "password": None,
    "cookies": 0,
    "clickers": 1,
    "foreground_color": "white",
    "background_color": "black"
}

# Load config or create default
if os.path.exists("config.json"):
    with open("config.json", "r") as f:
        config = json.load(f)
else:
    config = {
        "firsttime": True,
        "username": None,
        "password": None,
        "foreground_color": "white",
        "background_color": "black",
        "cookies": 0,
        "clickers": 1
    }

# First-time setup
if config["firsttime"] == True:
    un = input("What is your name? ")
    pw = input("Set a password: ")
    config["username"] = un
    config["password"] = pw
    config["firsttime"] = False

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

username = config["username"]
password = config["password"]

while True:
    print("JSH v1.2! Login required.")
    usern = input("Username: ")
    passw = input("Password: ")
    if usern == username and passw == password:
        print("Access granted.")
        break
    else:
        print("Incorrect username and/or password. Try again.")

# JSH SETUP

cd = os.getcwd()
running = True

fg_colors = {
    "black": "\033[1;30m","red": "\033[1;31m","green": "\033[1;32m",
    "yellow": "\033[1;33m","blue": "\033[1;34m","magenta": "\033[1;35m",
    "cyan": "\033[1;36m","white": "\033[1;37m"
}
bg_colors = {
    "black": "\033[1;40m","red": "\033[1;41m","green": "\033[1;42m",
    "yellow": "\033[1;43m","blue": "\033[1;44m","magenta": "\033[1;45m",
    "cyan": "\033[1;46m","white": "\033[1;47m"
}

fcolor_code = fg_colors.get(config["foreground_color"], "\033[1;37m")
bcolor_code = bg_colors.get(config["background_color"], "\033[1;40m")

def prompt():
    return input(f"{bcolor_code}{fcolor_code}JSH@{username}>\033[0m ").strip().split()

print("Welcome to James Shell Version 1.2!")
print("Type 'help' for commands!")
print(f"Current Directory: {cd}")
command = prompt()


# COMMANDS


def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def pwd():
    print(cd)

def echo(*text):
    print(" ".join(text))

def help():
    print("Commands:\n"
          "help - show this message\n"
          "echo <text> - print text\n"
          "pwd - print working directory\n"
          "cd <dir> - change directory\n"
          "ls <dir> - list directory\n"
          "mkdir <dir> - make directory\n"
          "rm <file/dir> - delete file/directory\n"
          "touch <file> - create file\n"
          "cat <file> - print file\n"
          "edit <file> - overwrite file\n"
          "ver - version info\n"
          "clear - clear screen\n"
          "connect <site> - open website\n"
          "random <min> <max> - random number\n"
          "fcolor <color> - set text color\n"
          "bcolor <color> - set background color\n"
          "jsh - ascii logo\n"
          "calc <expr> - calculator\n"
          "blush - >_<\n"
          "cookieclicker - game\n"
          "run <script.jsh> - run script\n"
          "randw - random word\n"
          "ftc <°F> - convert to Celsius\n"
          "ctf <°C> - convert to Fahrenheit\n"
          "bth <binary> - bin→hex\n"
          "htb <hex> - hex→bin\n"
          "dtbah <decimal> - dec→bin+hex\n"
          "btd <binary> - bin→dec\n"
          "htd <hex> - hex→dec\n"
          "bindump <file> - binary dump\n"
          "hexdump <file> - hex dump\n"
          "setusername <name> - change username\n"
          "setpassword <password> - change password\n"
          "coin - flip a coin\n"
          "dice <sides> - roll a dice\n"
          "quit - exit JSH\n")

def changedir(path=None):
    global cd
    if not path:
        return print("Please give a directory.")
    p = os.path.normpath(path)
    if os.path.isdir(p):
        os.chdir(p); cd = p
    else:
        print("Not valid directory.")

def ls(path=None):
    target = path or cd
    if os.path.isdir(target):
        for n in os.listdir(target):
            print(n)
    else:
        print("Not valid directory.")

def mkdir(path=None):
    if not path: return print("Not valid.")
    if not os.path.exists(path):
        os.mkdir(path); print(f"'{path}' created.")
    else:
        print("Already exists.")

def rm(path=None):
    if not path:
        return print("Usage: rm <file or directory>")
    if os.path.isdir(path):
        ok = input(f"Delete directory '{path}' and contents? (y/n): ")
        if ok.lower() == "y":
            shutil.rmtree(path)
            print(f"Directory '{path}' deleted.")
        else:
            print("Cancelled.")
    elif os.path.isfile(path):
        ok = input(f"Delete file '{path}'? (y/n): ")
        if ok.lower() == "y":
            os.remove(path)
            print("File deleted.")
        else:
            print("Cancelled.")
    else:
        print("Does not exist.")

def touch(file=None):
    if not file: return print("Not valid.")
    if os.path.exists(file): return print("Already exists.")
    contents = input("Enter file content: ")
    with open(file, "w") as f:
        f.write(contents)
    print(f"'{file}' created.")

def cat(file=None):
    if not file: return print("Not valid.")
    if not os.path.exists(file): return print("No such file.")
    with open(file, "r") as f:
        print(f.read())

def edit(file=None):
    if not file: return print("Not valid.")
    if not os.path.exists(file): return print("No such file.")
    contents = input("Enter new content: ")
    with open(file, "w") as f:
        f.write(contents)
    print("Updated.")

def ver():
    print("James Shell v1.2\nby James Baum")

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def connect(site=None):
    if not site:
        return print("Usage: connect <site>")
    webbrowser.open(site)

def rand(min_val=None, max_val=None):
    if min_val is None or max_val is None:
        return print("Usage: random <min> <max>")
    try:
        print(random.randint(int(min_val), int(max_val)))
    except:
        print("Invalid numbers.")

def fcolor(color=None):
    global fcolor_code
    if color not in fg_colors:
        return print("Invalid color.")
    fcolor_code = fg_colors[color]
    config["foreground_color"] = color
    save_config()
    print(f"Foreground set to {color}.")

def bcolor(color=None):
    global bcolor_code
    if color not in bg_colors:
        return print("Invalid color.")
    bcolor_code = bg_colors[color]
    config["background_color"] = color
    save_config()
    print(f"Background set to {color}.")

def jsh():
    print("""
--------  /-----   |    |
   //     |        |    |
   /      \-----   |----|
__/       _____/   |    |
v1.2 by James Baum
""")

def calc(expr=None):
    if not expr: return print("Usage: calc <expr>")
    print(eval(expr))

def blush():
    print(">_<")

def cookieclicker():
    global config

    cookie = config.get("cookies", 0)
    click = config.get("clickers", 1)

    def auto():
        nonlocal cookie
        while True:
            time.sleep(1)
            cookie += click

    threading.Thread(target=auto, daemon=True).start()

    print("Type 0 for stats, quit to exit.")

    while True:
        x = input("> ")
        if x == "0":
            print(f"""
{cookie} cookies
{click} cookies/sec
Type 1 to buy clicker (5 cookies)
""")
            c = input("> ")
            if c == "1":
                if cookie < 5:
                    print("Not enough cookies.")
                else:
                    cookie -= 5
                    click += 1
        elif x == "quit":
            config["cookies"] = cookie
            config["clickers"] = click
            save_config()
            break

def jshinterpret(script=None):
    if not script: return print("Usage: run <script.jsh>")
    if not os.path.exists(script): return print("Script not found.")
    with open(script, "r") as f:
        for line in f:
            parts = line.strip().split()
            if not parts: continue
            c = parts[0]
            a = parts[1:]
            if c in commands:
                try:
                    commands[c](*a)
                except:
                    try: commands[c]()
                    except: print("Command error.")
            else:
                print(f"{c}: invalid command")

def randw():
    words = ["apple","vector","shadow","planet","hollow","switch","carbon", "river","memory","signal"]
    print(random.choice(words))

def ftc(arg=None):
    try:
        print(f"{(float(arg)-32)*5/9:.2f}°C")
    except:
        print("Usage: ftc <°F>")

def ctf(arg=None):
    try:
        print(f"{(float(arg)*9/5)+32:.2f}°F")
    except:
        print("Usage: ctf <°C>")

def bth(arg=None):
    try:
        print(hex(int(arg, 2)))
    except:
        print("Usage: bth <binary>")

def htb(arg=None):
    try:
        print(bin(int(arg, 16)))
    except:
        print("Usage: htb <hex>")

def dtbah(arg=None):
    try:
        n = int(arg)
        print("Binary:", bin(n))
        print("Hex:", hex(n))
    except:
        print("Usage: dtbah <decimal>")

def btd(arg=None):
    try:
        print(int(arg, 2))
    except:
        print("Usage: btd <binary>")

def htd(arg=None):
    try:
        print(int(arg, 16))
    except:
        print("Usage: htd <hex>")

def bindump(file=None):
    if not file: return print("Usage: bindump <file>")
    if not os.path.exists(file): return print("File not found.")
    with open(file, "rb") as f:
        data = f.read()
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        bits = " ".join(f"{b:08b}" for b in chunk)
        print(f"{i:08X}: {bits}")

def hexdump(file=None):
    if not file: return print("Usage: hexdump <file>")
    if not os.path.exists(file): return print("File not found.")
    with open(file, "rb") as f:
        data = f.read()
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hx = " ".join(f"{b:02X}" for b in chunk)
        print(f"{i:08X}: {hx}")

def set_username(name=None):
    global username
    if not name:
        return print("Usage: setusername <name>")
    username = name
    config["username"] = name
    save_config()
    print(f"Username set to {name}")

def set_password(pw=None):
    global password
    if not pw:
        return print("Usage: setpassword <password>")
    if pw:
        security_check = input("Enter current password: ")
        if security_check != password:
            return print("Incorrect password.")
        if security_check == password:
            config["password"] = pw
            save_config()
            print("Password updated.")

def coin():
    print(random.choice(["Heads", "Tails"]))

def dice(N=None):
    if N is None:
        return print("Usage: dice <sides>")
    try:
        sides = int(N)
        if sides < 1:
            return print("Number of sides must be at least 1.")
        print(random.randint(1, sides))
    except:
        print("Invalid number of sides.")

# COMMAND REGISTRY

commands = {
    "pwd": pwd, "echo": echo, "help": help, "cd": changedir,
    "ls": ls, "mkdir": mkdir, "rm": rm, "touch": touch,
    "cat": cat, "edit": edit, "ver": ver, "clear": cls,
    "connect": connect, "random": rand, "fcolor": fcolor,
    "bcolor": bcolor, "jsh": jsh, "blush": blush,
    "cookieclicker": cookieclicker, "calc": calc, "run": jshinterpret,
    "randw": randw, "ftc": ftc, "ctf": ctf, "bth": bth, "htb": htb,
    "dtbah": dtbah, "btd": btd, "htd": htd, "bindump": bindump,
    "hexdump": hexdump, "setusername": set_username, "setpassword": set_password,
    "coin": coin, "dice": dice
}


# MAIN LOOP

while running:
    parts = command
    cmd = parts[0]
    args = parts[1:]

    if cmd == "quit":
        break
    elif cmd in commands:
        try:
            commands[cmd](*args)
        except:
            try: commands[cmd]()
            except: print("Usage error.")
    else:
        print(f"{cmd}: invalid command")

    command = prompt()
