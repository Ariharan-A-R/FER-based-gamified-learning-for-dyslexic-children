import tkinter as tk
from tkinter import messagebox, Toplevel
import random
from PIL import Image, ImageTk, ImageSequence

# Dictionary of letter-image matches (A-Z)
letter_images = {letter: f"matchAlphabets{letter.lower()}.png" for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

# Create main window
root = tk.Tk()
root.title("Alphabet Matching Game")
root.geometry("900x600")
root.configure(bg="purple")

# Label to display which letter to match
letter_label = tk.Label(root, text="", font=("Arial", 30, "bold"), bg="purple", fg="yellow")
letter_label.pack(pady=20)

# Drop box frame with text
drop_box = tk.Frame(root, width=150, height=150, bg="white", highlightbackground="black", highlightthickness=2)
drop_box.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
drop_label = tk.Label(drop_box, text="Drop here", font=("Arial", 15, "bold"), bg="white", fg="black")
drop_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Dragging storage
image_refs = []
current_stage = 0
stages = random.sample(list(letter_images.keys()), len(letter_images))  # Shuffle full alphabet


def on_drag_start(event):
    widget = event.widget
    widget.lift()
    widget.startX = event.x
    widget.startY = event.y


def on_drag_motion(event):
    widget = event.widget
    widget.place(x=widget.winfo_x() + event.x - widget.startX, y=widget.winfo_y() + event.y - widget.startY)


def on_drop(event, letter, img_label):
    global current_stage
    x1, y1 = drop_box.winfo_x(), drop_box.winfo_y()
    x2, y2 = x1 + 150, y1 + 150

    if x1 < img_label.winfo_x() < x2 and y1 < img_label.winfo_y() < y2:
        if letter == stages[current_stage]:
            img_label.place(x=x1 + 15, y=y1 + 15)
            show_fireworks()  # 🎉 Cheer up effect
            current_stage += 1
            if current_stage < len(stages):
                load_images()
            else:
                messagebox.showinfo("Game Over", "\U0001F389 You completed all stages!")
        else:
            img_label.place(x=random.randint(200, 700), y=random.randint(200, 250))
            show_sad_smiley()  # ❌ Sad face animation


# 🎆 Cheer up animation when correct (Transparent Background & Full Animation)
def show_fireworks():
    fireworks = Toplevel(root)
    fireworks.overrideredirect(True)  # Remove window border

    x = root.winfo_x() + (900 - 300) // 2
    y = root.winfo_y() + (600 - 300) // 2
    fireworks.geometry(f"300x300+{x}+{y}")

    gif = Image.open("matchAlphabets/fireworks.gif")
    frames = [ImageTk.PhotoImage(frame.convert("RGBA").resize((280, 280))) for frame in ImageSequence.Iterator(gif)]

    total_frames = len(frames)
    loops = 2  # Run twice
    frame_speed = 20  # Speed up (lower = faster)

    gif_label = tk.Label(fireworks, bg="black")
    gif_label.pack(expand=True)

    def animate(index=0, loop_count=0):
        if loop_count < loops:
            gif_label.config(image=frames[index])
            if index < total_frames - 1:
                fireworks.after(frame_speed, animate, index + 1, loop_count)
            else:
                fireworks.after(frame_speed, animate, 0, loop_count + 1)
        else:
            fireworks.after(500, fireworks.destroy)  # Close after full animation

    animate()


# 😔 Sad smiley animation when wrong (Transparent Background & Full Animation)
def show_sad_smiley():
    sad_window = Toplevel(root)
    sad_window.overrideredirect(True)

    x = root.winfo_x() + (900 - 220) // 2
    y = root.winfo_y() + (600 - 220) // 2
    sad_window.geometry(f"220x220+{x}+{y}")

    sad_gif = Image.open("matchAplhabets/sad_smiley.gif")
    frames = [ImageTk.PhotoImage(frame.convert("RGBA").resize((200, 200))) for frame in ImageSequence.Iterator(sad_gif)]

    sad_label = tk.Label(sad_window, bg="white")
    sad_label.pack(expand=True)

    def animate(index=0):
        sad_label.config(image=frames[index])
        if index < len(frames) - 1:
            sad_window.after(100, animate, index + 1)
        else:
            sad_window.after(500, sad_window.destroy)  # Close after full animation

    animate()


# Load images dynamically
def load_images():
    global image_refs
    letter_label.config(text=f"Match the letter: {stages[current_stage]}")

    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and widget != letter_label:
            widget.destroy()

    image_refs.clear()
    options = random.sample(list(letter_images.keys()), 5)  # 5 random options including correct one
    if stages[current_stage] not in options:
        options[random.randint(0, 4)] = stages[current_stage]  # Ensure correct option is present

    x_pos = (900 - (140 * len(options))) // 2  # Centering the options dynamically

    for letter in options:
        img = Image.open(letter_images[letter]).resize((130, 130))
        img = ImageTk.PhotoImage(img)
        image_refs.append(img)

        lbl = tk.Label(root, image=img, bg="purple")
        lbl.image = img
        lbl.place(x=x_pos, y=120)
        lbl.bind("<Button-1>", on_drag_start)
        lbl.bind("<B1-Motion>", on_drag_motion)
        lbl.bind("<ButtonRelease-1>", lambda event, l=letter, img_lbl=lbl: on_drop(event, l, img_lbl))

        x_pos += 140

# Function to handle exit confirmation
def confirm_exit():
    exit_window = Toplevel(root)
    exit_window.title("Exit Confirmation")
    exit_window.geometry("400x300")
    exit_window.configure(bg="white")

    # Centering the window
    exit_window.update_idletasks()
    x = root.winfo_x() + (900 - 400) // 2
    y = root.winfo_y() + (600 - 300) // 2
    exit_window.geometry(f"+{x}+{y}")

    # Load resized GIF
    gif = Image.open("matchAlphabets/quit.gif").resize((200, 200))
    gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

    gif_label = tk.Label(exit_window, bg="white")
    gif_label.pack()

    def animate(index=0):
        gif_label.config(image=gif_frames[index])
        exit_window.after(100, animate, (index + 1) % len(gif_frames))

    animate()

    # Message Label
    message_label = tk.Label(exit_window, text="Are you sure you want to leave the game?", font=("Arial", 12, "bold"), bg="white")
    message_label.pack(pady=5)

    # Buttons
    button_frame = tk.Frame(exit_window, bg="white")
    button_frame.pack(pady=10)

    continue_btn = tk.Button(button_frame, text="Continue", font=("Arial", 12, "bold"), bg="green", fg="white", command=exit_window.destroy)
    continue_btn.grid(row=0, column=0, padx=10)

    quit_btn = tk.Button(button_frame, text="Quit", font=("Arial", 12, "bold"), bg="red", fg="white", command=root.quit)
    quit_btn.grid(row=0, column=1, padx=10)

    exit_window.grab_set()  # Make it modal


# Exit Button
exit_btn = tk.Button(root, text="Exit", command=confirm_exit, font=("Arial", 15, "bold"), bg="red", fg="white")
exit_btn.place(x=750, y=550)



# ✅ Start game
load_images()
root.mainloop()
