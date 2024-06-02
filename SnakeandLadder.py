import tkinter as tk
import random
from PIL import Image, ImageTk
from gtts import gTTS
from playsound import playsound
import os

def speak(text, callback=None):
    obj = gTTS(text=text, lang='en', slow=False)
    obj.save('text.mp3')
    playsound('text.mp3')
    os.remove('text.mp3')
    if callback:
        callback()

def start_game():
    global im, b1, b2, b3, exit_btn
    b1.place(x=1000, y=400)
    b2.place(x=1000, y=550)

    im = Image.open("images/dice.png")
    im = im.resize((65, 65))
    im = ImageTk.PhotoImage(im)
    b3 = tk.Button(root, image=im, height=80, width=80)
    b3.place(x=1000, y=300)
    
    exit_btn = tk.Button(root, text="Click here to exit", height=2, width=20, fg="black", bg="yellow", font=('times new roman', 14, 'bold'), activebackground="white", command=root.destroy)
    exit_btn.place(x=1000, y=20)

def reset_coins():
    global player_1, player_2, pos1, pos2
    player_1.place(x=0, y=650)
    player_2.place(x=50, y=650)
    pos1 = 0
    pos2 = 0

def load_dice_images():
    global Dice
    names = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
    for name in names:
        im = Image.open("images/" + name)
        im = im.resize((65, 65))
        im = ImageTk.PhotoImage(im)
        Dice.append(im)

def check_Ladder(Turn):
    global pos1, pos2, Ladders
    found = 0
    if Turn == 1:
        if pos1 in Ladders:
            speak("ladder at " + str(pos1) + " moving up to position " + str(Ladders[pos1]), lambda: move_coin_callback(Turn))
            pos1 = Ladders[pos1]
            found = 1
    else:
        if pos2 in Ladders:
            speak("ladder at " + str(pos2) + " moving up to position " + str(Ladders[pos2]), lambda: move_coin_callback(Turn))
            pos2 = Ladders[pos2]
            found = 1
    return found

def check_snake(Turn):
    global pos1, pos2
    if Turn == 1:
        if pos1 in snakes:
            speak("snake at " + str(pos1) + " going down to its tail position " + str(snakes[pos1]), lambda: move_coin_callback(Turn))
            pos1 = snakes[pos1]
    else:
        if pos2 in snakes:
            speak("snake at " + str(pos2) + " going down to its tail position " + str(snakes[pos2]), lambda: move_coin_callback(Turn))
            pos2 = snakes[pos2]

def roll_dice():
    global Dice, turn, pos1, pos2, b1, b2
    r = random.randint(1, 6)
    b3 = tk.Button(root, image=Dice[r-1], height=80, width=80)
    b3.place(x=1000, y=300)
    root.after(1000, lambda: roll_dice_continued(r))
    
def roll_dice_continued(r):
    global turn, pos1, pos2, b1, b2
    speak("it's " + str(r))
    ladder = 0  # no ladder
    if turn == 1:
        if (pos1 + r) <= 100:
            pos1 = pos1 + r
        ladder = check_Ladder(turn)
        check_snake(turn)
        move_coin(turn, pos1, lambda: speak("now you are at position " + str(pos1)))
        if r != 6 and ladder != 1:
            turn = 2
            b1.configure(state='disabled')
            b2.configure(state='normal')
    else:
        if (pos2 + r) <= 100:
            pos2 = pos2 + r
        ladder = check_Ladder(turn)
        check_snake(turn)
        move_coin(turn, pos2, lambda: speak("now you are at position " + str(pos2)))
        if r != 6 and ladder != 1:
            turn = 1
            b2.configure(state='disabled')
            b1.configure(state='normal')
    speak("player - " + str(turn) + " turn ")
    is_winner()

def is_winner():
    global pos1, pos2
    if pos1 == 100:
        message = "Congratulations! Player1 is the Winner"
        speak(message)
        Lab = tk.Label(root, text=message, height=2, width=40, bg='red', font=('times new roman', 30, 'bold'))
        Lab.place(x=300, y=300)
        reset_coins()
        
    elif pos2 == 100:
        message = "Congratulations! Player2 is the Winner"
        speak(message)
        Lab = tk.Label(root, text=message, height=2, width=40, bg='red', font=('times new roman', 30, 'bold'))
        Lab.place(x=300, y=300)
        reset_coins()

def move_coin(Turn, r, callback=None):
    global player_1, player_2, index, pos1, pos2
    if Turn == 1:
        player_1.place(x=index[r][0], y=index[r][1])
        if callback:
            callback()
    else:
        player_2.place(x=index[r][0], y=index[r][1])
        if callback:
            callback()


def move_coin_callback(Turn):
    global turn
    if turn == 1:
        b1.configure(state='normal')
    else:
        b2.configure(state='normal')

def get_index():
    global player_1, player_2, index
    numbers = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91,
               81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
               80, 79, 78, 77, 76, 75, 74, 73, 72, 71,
               61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
               60, 59, 58, 57, 56, 55, 54, 53, 52, 51,
               41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
               40, 39, 38, 37, 36, 35, 34, 33, 32, 31,
               21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
               20, 19, 18, 17, 16, 15, 14, 13, 12, 11,
               1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    row = 5
    i = 0
    for x in range(1, 11):
        col = 50
        for y in range(1, 11):
            index[numbers[i]] = (col, row)
            col = col + 88
            i = i + 1
        row = row + 63
    print(index)


def restart_game():
    global turn
    reset_coins()
    turn = 1
    b1.configure(state='normal')
    b2.configure(state='disabled')
    start_game()

def pause_game():
    global paused
    paused = True
    b1.configure(state='disabled')
    b2.configure(state='disabled')
    speak("Game paused")

def resume_game():
    global paused
    paused = False
    if turn == 1:
        b1.configure(state='normal')
    else:
        b2.configure(state='normal')
    speak("Game resumed")

Dice = []
index = {}
pos1 = None
pos2 = None
paused = False

Ladders = {3: 21, 8: 30, 28: 84, 58: 77, 75: 86, 80: 100, 90: 91}
snakes = {17: 12, 52: 29, 57: 40, 62: 22, 88: 18, 95: 51, 97: 79}

root = tk.Tk()
root.geometry("1200x800")
root.title("Snake and Ladder Game")

F1 = tk.Frame(root, width=1200, height=800, relief='raised')
F1.place(x=0, y=0)

img1 = ImageTk.PhotoImage(Image.open("images/board.png"))
Lab = tk.Label(F1, image=img1)
Lab.place(x=0, y=0)

b1 = tk.Button(root, text="Player-1", height=3, width=20, fg="black", bg="red", font=('times new roman', 14, 'bold'), activebackground="white", command=roll_dice)
b2 = tk.Button(root, text="Player-2", height=3, width=20, fg="black", bg="blue", font=('times new roman', 14, 'bold'), activebackground="white", command=roll_dice)

player_1 = tk.Canvas(root, width=40, height=40)
player_1.create_oval(10, 10, 40, 40, fill='Red')

player_2 = tk.Canvas(root, width=40, height=40)
player_2.create_oval(10, 10, 40, 40, fill='Blue')

pause_btn = tk.Button(root, text="Pause", height=2, width=10, fg="black", bg="cyan", font=('times new roman', 14, 'bold'), activebackground="white", command=pause_game)
pause_btn.place(x=960, y=150)

resume_btn = tk.Button(root, text="Resume", height=2, width=10, fg="black", bg="violet", font=('times new roman', 14, 'bold'), activebackground="white", command=resume_game)
resume_btn.place(x=1110, y=150)

turn = 1
reset_coins()
get_index()
load_dice_images()
start_game()
speak("Welcome to Snake and Ladder game, let's start with player 1")
root.mainloop()

