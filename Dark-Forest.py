import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)

# window
window = tk.Tk()
window.title("Dark Forest")
window.geometry("400x500")
window.resizable(False, False)

if sys.platform.startswith('win'):
    icon_file = "Dark-Moon.png"
else:
    icon_file = "The-Forest.icns"

window.iconbitmap(resource_path(icon_file))

# image
img = Image.open(resource_path("misty-landscape.jpg"))
img = img.resize((400, 500), resample=Image.LANCZOS)
photo = ImageTk.PhotoImage(img)

def create_text(canvas, text_list, width, height, title_size=27, other_size=18):
    # create canvas and add image
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)
    # create caption
    caption = canvas.create_text(width/2, height/3 - 110, text=text_list[0],
                       font=("Times", title_size, "bold"), fill="white")

    # create additional texts
    y_offset = height/3
    other_texts = []
    for text in text_list[1:]:
        other_text = canvas.create_text(width/2, y_offset, text=text,
                           font=("Times", other_size, "bold"), fill="white")
        other_texts.append(other_text)
        y_offset += other_size * 2
    return [caption] + other_texts

def restart():
    canvas.delete("all")
    step_one()

def create_button(text, x_position, y_position, command=None):
    global button_photo
    # create a transparent image for the background of the button
    button_img = Image.new('RGBA', (50, 20), (0, 0, 0, 0))
    button_photo = ImageTk.PhotoImage(button_img)
    # create a button with a transparent background
    button = tk.Button(canvas, text=text, image=button_photo, compound='center', font=("Times", 14, "bold"), command=command)
    button.configure(bg="white", bd=0, highlightthickness=0, activebackground="white")
    # place the button on the canvas
    button.place(relx=x_position, rely=y_position, anchor='center')
    return button

def create_input(canvas, x_position):
    # create an input field with a white background
    input_field = tk.Entry(canvas, bg="white", fg="black", font=("Times", 15))
    input_field.configure(state="normal",insertbackground="black")
    
    # define function to handle enter key press
    def on_enter(event):
        value = input_field.get().lower()
        print("Entered value:", value)
        input_field.delete(0, tk.END)
    
    # bind the function to the <Return> key event
    input_field.bind("<Return>", on_enter)

    # place the input field on the canvas
    input_field.place(relx=x_position, rely=0.8, anchor='center')
    # set focus on input
    input_field.focus()
    # disable focus highlight on canvas
    canvas.configure(highlightthickness=0)
    return input_field

def create_image(canvas, image_path, x, y, anchor='nw', tagOrId=None):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    canvas.image = photo # save the PhotoImage as an attribute of the canvas
    return canvas.create_image(x, y, image=photo, anchor=anchor, tag=tagOrId)

def step_one():
    # create the text and input field
    question = create_text(canvas, ["You see three paths ahead of you.", "", "You go 'left', 'right' or 'straight'?"], 400, 500, title_size=24, other_size=16)
    input_field = create_input(canvas, 0.4)
    
    # define function to handle input
    def handle_input():
        value = input_field.get().lower()
        print("Entered value:", value)
        input_field.delete(0, tk.END)
        if not value:
            return
        if value == "left":
            left(value)
            go_button.destroy()
            input_field.destroy()
        elif value == "right":
            right()
            go_button.destroy()
            input_field.destroy()
        elif value == "straight":
            straight()
            go_button.destroy()
            input_field.destroy()
        else:
            # clear the input field if the entered value is not valid
            error = create_text(canvas, ["Sorry, I didn't understand your input.", "", "Please enter 'left', 'right', or 'straight'."], 400, 500, title_size=22, other_size=16)
            input_field.delete(0, tk.END)
            
    go_button = create_button("Go", 0.7, 0.8, handle_input)
    # bind the Enter key to the input field
    input_field.bind("<Return>", lambda event: handle_input())

def left(value):
    # create the text
    question = create_text(canvas, ["You are by the river.", "", "You can 'swim' or try to find a 'boat'."], 400, 500, title_size=24, other_size=16)
    input_field = create_input(canvas, 0.4)

    # define function to handle input for the left() function
    def handle_input():
        nonlocal input_field
        value = input_field.get().lower()
        print("Entered value:", value)
        input_field.delete(0, tk.END)
        if not value:
            return
        if value == "swim":
            swim = create_text(canvas, ["What a shame, you drowned in the river.", "", "Game over."], 400, 500, title_size=22, other_size=18)
            death_image_id = create_image(canvas, resource_path("death.png"), 185, 320, anchor='center', tagOrId="all")
            play_again = create_button("Play again", 0.5, 0.8, command=lambda:[restart(), play_again.destroy()])
            go_button.destroy()
            input_field.destroy()
        elif value == "boat":
            boat = create_text(canvas, ["         You managed to find boat\nand reach the other side of the river.", "", "You see two doors in front of you.\nOpen the 'left' or 'right'?"], 400, 500, title_size=22, other_size=16)
            door()
            go_button.destroy()
            input_field.destroy()
        else:
            error = create_text(canvas, ["Sorry, I didn't understand your input.", "", "Please enter 'swim', or 'boat'."], 400, 500, title_size=24, other_size=16)
            input_field.delete(0, tk.END)
            
    go_button = create_button("Go", 0.7, 0.8, handle_input)
    # bind the Enter key to the input field
    input_field.bind("<Return>", lambda event: handle_input())

    def door():
        input_field = create_input(canvas, 0.4)
        
        def handle_input():
            value = input_field.get().lower()
            print("Entered value:", value)
            input_field.delete(0, tk.END)
            if not value:
                return
            if value == "left":
                treasure = create_text(canvas, ["You entered the room with a treasure.", "", "Congratulations, you won!"], 400, 500, title_size=22, other_size=18)
                win_image = create_image(canvas, resource_path("treasure2.png"), 198, 425, anchor='center', tagOrId="all")
                play_again = create_button("Play again", 0.5, 0.5, command=lambda:[restart(), play_again.destroy()])
                go_button.destroy()
                input_field.destroy()
            elif value == "right":
                dragon = create_text(canvas, ["What a shame, you entered the room\nwith a dangerous dragon.", "", "Beware of your life! The game is over."], 400, 500, title_size=22, other_size=16)
                death_image_id = create_image(canvas, resource_path("death.png"), 185, 320, anchor='center', tagOrId="all")
                play_again = create_button("Play again", 0.5, 0.8, command=lambda:[restart(), play_again.destroy()])
                go_button.destroy()
                input_field.destroy()
            else:
                error = create_text(canvas, ["Sorry, I didn't understand your input.", "", "Please enter 'left', or 'right'."], 400, 500, title_size=24, other_size=16)
                input_field.delete(0, tk.END)
                
        go_button = create_button("Go", 0.7, 0.8, handle_input)
        # bind the Enter key to the input field
        input_field.bind("<Return>", lambda event: handle_input())

def right():
    cottage = create_text(canvas, ["You are in an old abandoned cottage.", "", "You see two rooms in front of you.\n    'Left' or 'right'?"], 400, 500, title_size=22, other_size=14)
    input_field = create_input(canvas, 0.4)
    
    def handle_input():
        value = input_field.get().lower()
        input_field.delete(0, tk.END)
        if not value:
            return
        if value == "left":
            go_left = create_text(canvas, ["You walked into a room full of traps\n                      and you died."], 400, 500, title_size=20, other_size=14)
            death_image = create_image(canvas, resource_path("death.png"), 185, 320, anchor='center', tagOrId="all")
            play_again = create_button("Play again", 0.5, 0.8, command=lambda:[restart(), play_again.destroy()])
            go_button.destroy()
            input_field.destroy()
        elif value == "right":
            go_right = create_text(canvas, ["You have entered\na room with a treasure chest.", "", "Congratulations, you have won!"], 400, 500, title_size=24, other_size=16)
            win_image = create_image(canvas, resource_path("treasure2.png"), 198, 425, anchor='center', tagOrId="all")
            play_again = create_button("Play again", 0.5, 0.5, command=lambda:[restart(), play_again.destroy()])
            go_button.destroy()
            input_field.destroy()
        else:
            error = create_text(canvas, ["Sorry, I didn't understand your input.", "", "Please enter 'left', or 'right'."], 400, 500, title_size=24, other_size=16)
            input_field.delete(0, tk.END)
    go_button = create_button("Go", 0.7, 0.8, handle_input)
    # bind the Enter key to the input field
    input_field.bind("<Return>", lambda event: handle_input())

def straight():
    castle = create_text(canvas, ["You are at the old castle.", "", "You see a 'bridge', 'gate' or 'path' in front of you."], 400, 500, title_size=24, other_size=14)
    input_field = create_input(canvas, 0.4)
    
    def handle_input():
        value = input_field.get().lower()
        input_field.delete(0, tk.END)
        if not value:
            return
        if value == "bridge":
            bridge = create_text(canvas, ["What a shame.\nThe bridge is broken\nand you've fallen through.", "", "End of game."], 400, 500, title_size=22, other_size=16)
            death_image_id = create_image(canvas, resource_path("death.png"), 185, 320, anchor='center', tagOrId="all")
            play_again = create_button("Play again", 0.5, 0.8, command=lambda:[restart(), play_again.destroy()])
            go_button.destroy()
            input_field.destroy()
        elif value == "gate":
            go_right = create_text(canvas, ["You managed to pass through the gate.", "You find yourself in a dark forest.\nThere's a 'cave' and a 'river' nearby."], 400, 500, title_size=22, other_size=14)
            gate()
            go_button.destroy()
            input_field.destroy()
        elif value == "path":
            path = create_text(canvas, ["You follow the winding path through the forest.", "After walking for a while, you come across a clearing.", "", "In the middle of the clearing stands a small cottage.", "", "You hear a faint noise coming from inside.", "", "Do you want to 'enter' the cottage or 'leave' the clearing?"], 400, 500, title_size=18, other_size=14)
            go_path()
            go_button.destroy()
            input_field.destroy()
        else:
            error = create_text(canvas, ["Sorry, I didn't understand your input.", "", "Please enter 'bridge', 'gate' or 'path'."], 400, 500, title_size=24, other_size=16)
            input_field.delete(0, tk.END)

    go_button = create_button("Go", 0.7, 0.8, handle_input)
    # bind the Enter key to the input field
    input_field.bind("<Return>", lambda event: handle_input())
    
    def gate():
        input_field = create_input(canvas, 0.4)
        
        def handle_input():
            value = input_field.get().lower()
            input_field.delete(0, tk.END)
            if not value:
                return
            if value == "cave":
                cave = create_text(canvas, ["You have entered the dark cave.\nYou see two paths in front of you.", "", "Which one do you want to take?\nEnter 'left' or 'right'."], 400, 500, title_size=22, other_size=14)
                go_cave()
                go_button.destroy()
                input_field.destroy()
            elif value == "river":
                river = create_text(canvas, ["You have arrived at the river.\nYou notice a boat by the bank.", "", "        Do you want to take\nthe boat and follow the river?", "", "Enter 'yes' or 'no'."], 400, 500, title_size=22, other_size=14)
                go_river()
                go_button.destroy()
                input_field.destroy()
            else:
                error = create_text(canvas, ["Sorry, I didn't understand your input.", "", "Please enter 'cave' or 'river'."], 400, 500, title_size=24, other_size=16)
                input_field.delete(0, tk.END)
                
        go_button = create_button("Go", 0.7, 0.8, handle_input)
        # bind the Enter key to the input field
        input_field.bind("<Return>", lambda event: handle_input())
        
    def go_path():
        input_field = create_input(canvas, 0.4)
        
        def handle_input():
            value = input_field.get().lower()
            input_field.delete(0, tk.END)
            if not value:
                return
            if value == "enter":
                enter = create_text(canvas, ["You cautiously push open the door to the cottage.", "", "Inside, you see a small, cramped room.\nThere is a table with a candle on it.\nYou approach the table to get a closer look.\nAs you lean in, the candle flickers and goes out.\nYou feel something grab your shoulder.\nSuddenly, you are pulled into darkness.\nEnd of game."], 400, 500, title_size=18, other_size=14)
                death_image_id = create_image(canvas, resource_path("death.png"), 185, 360, anchor='center', tagOrId="all")
                play_again = create_button("Play again", 0.5, 0.9, command=lambda:[restart(), play_again.destroy()])
                go_button.destroy()
                input_field.destroy()
            elif value == "leave":
                leave = create_text(canvas, ["You quickly leave the clearing.\nAs you walk away,\nyou hear a strange noise behind you.\nYou don't turn around,\nand soon find your way to the hidden treasure!", "", "Congrats, you won!"], 400, 500, title_size=17, other_size=14)
                win_image = create_image(canvas, resource_path("treasure2.png"), 198, 425, anchor='center', tagOrId="all")
                play_again = create_button("Play again", 0.5, 0.5, command=lambda:[restart(), play_again.destroy()])
                go_button.destroy()
                input_field.destroy()
            else:
                error = create_text(canvas, ["Sorry, I didn't understand your input.", "", "Please enter 'enter' or 'leave'."], 400, 500, title_size=24, other_size=16)
                input_field.delete(0, tk.END)
                
        go_button = create_button("Go", 0.7, 0.8, handle_input)
        # bind the Enter key to the input field
        input_field.bind("<Return>", lambda event: handle_input())
        
    def go_cave():
        input_field = create_input(canvas, 0.4)
        
        def handle_input():
            value = input_field.get().lower()
            input_field.delete(0, tk.END)
            if not value:
                return
            if value == "left":
                go_left = create_text(canvas, ["You chose the left path\nand find a hidden treasure!", "", "Congrats, you won!"], 400, 500, title_size=24, other_size=16)
                win_image = create_image(canvas, resource_path("treasure2.png"), 198, 425, anchor='center', tagOrId="all")
                play_again = create_button("Play again", 0.5, 0.5, command=lambda:[restart(), play_again.destroy()])
                go_button.destroy()
                input_field.destroy()
            elif value == "right":
                go_river = create_text(canvas, ["You chose the right path and\nfall into a pit.", "", "You are trapped and cannot escape.", "End of game."], 400, 500, title_size=22, other_size=14)
                death_image_id = create_image(canvas, resource_path("death.png"), 185, 320, anchor='center', tagOrId="all")
                play_again = create_button("Play again", 0.5, 0.8, command=lambda:[restart(), play_again.destroy()])
                go_button.destroy()
                input_field.destroy()
            else:
                error = create_text(canvas, ["Sorry, I didn't understand your input.", "", "Please enter 'left' or 'right'."], 400, 500, title_size=24, other_size=16)
                input_field.delete(0, tk.END)
                
        go_button = create_button("Go", 0.7, 0.8, handle_input)
        # bind the Enter key to the input field
        input_field.bind("<Return>", lambda event: handle_input())
        
    def go_river():
        input_field = create_input(canvas, 0.4)
        
        def handle_input():
            value = input_field.get().lower()
            input_field.delete(0, tk.END)
            if not value:
                return
            if value == "yes":
                yes_option = create_text(canvas, ["You decide to swim across the river.", "The current is strong and you struggle to stay afloat,\nbut you eventually make it to the other side.\nYou continue on your journey and eventually find\nthe treasure hidden deep within the forest.", "", "Congratulations, you have won the game!"], 400, 500, title_size=23, other_size=14)
                win_image = create_image(canvas, resource_path("treasure2.png"), 198, 425, anchor='center', tagOrId="all")
                play_again = create_button("Play again", 0.5, 0.5, command=lambda:[restart(), play_again.destroy()])
                go_button.destroy()
                input_field.destroy()
            elif value == "no":
                no_option = create_text(canvas, ["You decide not to risk swimming across the river.", "As you turn to walk away,\nyou hear a growl behind you.\nYou look back to see a hungry pack of wolves\nemerging from the trees. You try to run,\nbut they quickly catch up to you and overpower you.\nYou have been killed by the wolves. Game over."], 400, 500, title_size=18, other_size=14)
                death_image_id = create_image(canvas, resource_path("death.png"), 185, 320, anchor='center', tagOrId="all")
                play_again = create_button("Play again", 0.5, 0.8, command=lambda:[restart(), play_again.destroy()])
                go_button.destroy()
                input_field.destroy()
            else:
                error = create_text(canvas, ["Sorry, I didn't understand your input.", "", "Please enter 'yes' or 'no'."], 400, 500, title_size=24, other_size=16)
                input_field.delete(0, tk.END)
                
        go_button = create_button("Go", 0.7, 0.8, handle_input)
        # bind the Enter key to the input field
        input_field.bind("<Return>", lambda event: handle_input())
# create a canvas and add an image
canvas = tk.Canvas(window, width=img.width, height=img.height)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)
canvas.pack()

# create text
welcom_text = create_text(canvas, ["Welcome to the Dark Forest!", "Your goal is to find the treasure.", "Where might it be located?"], 400, 500, title_size=30, other_size=16)

def start_game_logic():
    for item in welcom_text:
        canvas.delete(item)
        start_button.destroy()
    step_one()

# create start button
start_button = create_button("Start !", 0.5, 0.8, start_game_logic)

# start the graphical user interface
window.mainloop()