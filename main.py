import os
import random
import webbrowser

#JSH Setup
cd = os.path.abspath(__file__)
running = True
fcolor_code = "\033[1;37m"
bcolor_code = "\033[1;40m"

def prompt():
    """Prompt user for command using current colors and working directory"""
    return input(f"{bcolor_code}{fcolor_code}JSH@{cd}>\033[0m ").strip().split(" ", 1)

print("Welcome to James Shell Version 1.0!")
print("Type 'help' for commands!")
print(f"Current Directory: {cd}")
command = prompt()

#Command Definitions
def pwd(): print(cd)

def printtext(text=None):
    print(text if text else "")

def help():
    print("Commands:\n"
          "help - displays this help message\n"
          "printtext <text> - print text\n"
          "pwd - print working directory\n"
          "cd <dir> - change directory\n"
          "ls <dir> - list directory\n"
          "newdir <dir> - makes a new directory\n"
          "rm <file/dir> - deletes a file or folder (caution!)\n"
          "newfile <file> - makes a new file\n"
          "printfile <file> - prints the contents of a file\n"
          "edit <file> - edit a file’s content\n"
          "ver - show version\n"
          "clear - clear screen\n"
          "connect <site> - open website\n"
          "random <min>(newline)<max> - random number between min and max\n"
          "fcolor <color> - set foreground text color\n"
          "bcolor <color> - set background color\n"
          "quit - close JSH\n")

def changedir(path=None):
    global cd
    if not path: return print("Please give a valid directory.")
    path = os.path.normpath(path)
    if os.path.exists(path) and os.path.isdir(path):
        os.chdir(path); cd = path
    else:
        print("Not valid directory.")

def ls(path=None):
    target = path or os.path.dirname(cd)
    if os.path.exists(target) and os.path.isdir(target):
        for name in os.listdir(target): print(name)
    else:
        print("Not a valid directory.")

def newdir(path=None):
    if not path: return print("Not valid.")
    if not os.path.exists(path):
        os.mkdir(path); print(f"'{path}' made successfully.")
    else:
        print(f"Directory '{path}' already exists.")

def rm(path=None):
    if not path: return print("Not valid.")
    if os.path.isdir(path):
        os.rmdir(path); print(f"Directory '{path}' deleted successfully.")
    elif os.path.isfile(path):
        os.remove(path); print(f"File '{path}' deleted successfully.")
    else:
        print(f"'{path}' doesn't exist.")

def newfile(file=None):
    if not file: return print("Not valid.")
    if not os.path.exists(file):
        contents = input("Enter file content: ")
        with open(file, "w") as f: f.write(contents)
        print(f"File '{file}' created successfully.")
    else:
        print("File already exists.")

def printfile(file=None):
    if not file: return print("Not valid.")
    if os.path.exists(file):
        with open(file, "r") as f:
            for line in f: print(line, end="")
    else:
        print("File doesn't exist.")

def edit(file=None):
    if not file: return print("Not valid.")
    if not os.path.exists(file): return print("File doesn't exist.")
    new_content = input("Enter new content: ")
    with open(file, "w") as f: f.write(new_content)
    print(f"File '{file}' updated successfully.")

def ver():
    print("James Shell v1.0\nPublished on November 4th 2025 with the MIT license by James Baum.")

def cls(): os.system("cls" if os.name == "nt" else "clear")

def connect(site=None):
    if not site: return print("Please give a website address.")
    webbrowser.open(site)

def rand(min_val=None):
    if not min_val: return print("Usage: random <min> <max>")
    try:
        min_int = int(min_val)
        max_int = int(input("Max value: "))
        print(random.randint(min_int, max_int))
    except ValueError:
        print("Please enter valid integers.")

def fcolor(arg=None):
    global fcolor_code
    colors = {
        "black": "\033[1;30m","red": "\033[1;31m","green": "\033[1;32m",
        "yellow": "\033[1;33m","blue": "\033[1;34m","magenta": "\033[1;35m",
        "cyan": "\033[1;36m","white": "\033[1;37m"
    }
    if arg in colors:
        fcolor_code = colors[arg]; print(f"Foreground color set to {arg}.")
    else:
        print("Invalid color. Valid options:", ", ".join(colors.keys()))

def bcolor(arg=None):
    global bcolor_code
    colors = {
        "black": "\033[1;40m","red": "\033[1;41m","green": "\033[1;42m",
        "yellow": "\033[1;43m","blue": "\033[1;44m","magenta": "\033[1;45m",
        "cyan": "\033[1;46m","white": "\033[1;47m"
    }
    if arg in colors:
        bcolor_code = colors[arg]; print(f"Background color set to {arg}.")
    else:
        print("Invalid color. Valid options:", ", ".join(colors.keys()))

#Command Registry
commands = {
    "pwd": pwd, "printtext": printtext, "help": help, "cd": changedir,
    "ls": ls, "newdir": newdir, "rm": rm, "newfile": newfile,
    "printfile": printfile, "edit": edit, "ver": ver, "clear": cls,
    "connect": connect, "random": rand, "fcolor": fcolor, "bcolor": bcolor
}

#Main loop
while running:
    cmd = command[0]
    arg = command[1] if len(command) > 1 else None

    if cmd == "quit":
        break
    elif cmd in commands:
        try:
            commands[cmd](arg)
        except TypeError:
            commands[cmd]()
    else:
        print(f"{cmd} is not a valid command.")

    command = prompt()
