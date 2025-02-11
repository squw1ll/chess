import tkinter as tk
from tkinter import PhotoImage
from tkinter import font
from PIL import Image, ImageTk
import subprocess
from tkinter import ttk

timer_running = False
seconds = 0



def close_window():
    root.destroy()

def update_timer():
    global timer_running, seconds
    if timer_running:
        seconds += 1
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        timer_label.config(text=f"{minutes:02}:{remaining_seconds:02}")
        root.after(1000, update_timer)

def start_timer():
    global timer_running
    if not timer_running:  
        timer_running = True
        update_timer()

def reset_timer():
    global timer_running, seconds
    timer_running = False  
    seconds = 0  
    timer_label.config(text="00:00") 
    

def check_process():
    global external_process
    if external_process is not None:
        if external_process.poll() is not None:  
            external_process = None
            reset_timer()  
        else:
            root.after(100, check_process)

def on_enter(event):
    wh_canvas.itemconfig(rect, fill="#81b64c")

def on_leave(event):
    wh_canvas.itemconfig(rect, fill="#59946f")

def on_enter1(event):
    bl_canvas.itemconfig(rect, fill="#81b64c")

def on_leave1(event):
    bl_canvas.itemconfig(rect, fill="#59946f")

def on_enter2(event):
    ex_canvas.itemconfig(rect, fill="#d52e2f")

def on_leave2(event):
    ex_canvas.itemconfig(rect, fill="#1c1c1c")

def play_white():
    global external_process
    start_timer()  
    external_process = subprocess.Popen(["pythonw", "start_white.pyw"])  # Запускаем игровой процесс
    print("Play for White started")
    check_process()  

def play_black():
    global external_process
    start_timer()  
    external_process = subprocess.Popen(["pythonw", "start_black.pyw"])  
    print("Play for Black started")
    check_process()  

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)
####################################################################################################
root = tk.Tk()
root.title("Chess_bot @squw1ll")
root.geometry("1100x600+200+100")
root.resizable(False,False)
root.configure(bg="#1c1c1c")
root.overrideredirect(True)


custom_font = font.Font(family="Verdana", size=30, weight="bold")
custom_font1 = font.Font(family="Verdana", size=16, weight="bold")
custom_font2 = font.Font(family="Tahoma", size=14, weight="bold")
custom_font3 = font.Font(family="Verdana", size=10, weight="bold")
custom_font4 = font.Font(family="Verdana", size=20, weight="bold")
custom_font5 = font.Font(family="Verdana", size=25, weight="bold")


board_image = PhotoImage(file="chess_board.png")  # Добавьте изображение шахматной доски
board_label = tk.Label(root, image=board_image, bg="#1c1c1c")
board_label.place(x=50, y=50)

########################################### Текст 
title = tk.Label(root, text="Play Chess With Bot", font=custom_font, fg="white", bg="#1c1c1c")
title.place(x=610, y=35)
title1 = tk.Label(root, text="Choose the color you will play for", font=custom_font1, fg="white", bg="#1c1c1c")
title1.place(x=610, y=100)
title1 = tk.Label(root, text="Time:", font=custom_font4, fg="white", bg="#1c1c1c")
title1.place(x=900, y=195)

#########################секундомер
timer_label = tk.Label(root, text="00:00", font=custom_font5, fg="white", bg="#1c1c1c")
timer_label.place(x=892, y=235)

################################################# Кнопка Play for White
pawn_img = Image.open("white_pawn.png")
pawn_photo = ImageTk.PhotoImage(pawn_img)

wh_canvas = tk.Canvas(root, width=210, height=52, bg="#1c1c1c", highlightthickness=0)
wh_canvas.place(x=610, y=180)
rect = create_rounded_rectangle(wh_canvas, 0, 0, 210, 52, radius=25, fill="#59946f", outline="")

pawn = wh_canvas.create_image(25, 25, image=pawn_photo) 
text = wh_canvas.create_text(120, 28, text="Play for White", font=custom_font2, fill="black") 

wh_canvas.tag_bind(rect, "<Button-1>", lambda event: play_white()) 
wh_canvas.tag_bind(pawn, "<Button-1>", lambda event: play_white()) 
wh_canvas.tag_bind(text, "<Button-1>", lambda event: play_white()) 


wh_canvas.tag_bind(rect, "<Enter>", on_enter)
wh_canvas.tag_bind(rect, "<Leave>", on_leave)
wh_canvas.tag_bind(pawn, "<Enter>", on_enter)
wh_canvas.tag_bind(pawn, "<Leave>", on_leave)
wh_canvas.tag_bind(text, "<Enter>", on_enter)
wh_canvas.tag_bind(text, "<Leave>", on_leave)

################################## Кнопка Play for Black
pawn_img1 = Image.open("black_pawn.png")
pawn_photo1 = ImageTk.PhotoImage(pawn_img1)

bl_canvas = tk.Canvas(root, width=210, height=52, bg="#1c1c1c", highlightthickness=0)
bl_canvas.place(x=610, y=250)
rect1 = create_rounded_rectangle(bl_canvas, 0, 0, 210, 52, radius=25, fill="#59946f", outline="")

pawn1 = bl_canvas.create_image(25, 25, image=pawn_photo1) 
text1 = bl_canvas.create_text(120, 28, text="Play for Black", font=custom_font2, fill="black") 

bl_canvas.tag_bind(rect1, "<Button-1>", lambda event: play_black()) 
bl_canvas.tag_bind(pawn1, "<Button-1>", lambda event: play_black()) 
bl_canvas.tag_bind(text1, "<Button-1>", lambda event: play_black()) 

bl_canvas.tag_bind(rect1, "<Enter>", on_enter1)
bl_canvas.tag_bind(rect1, "<Leave>", on_leave1)
bl_canvas.tag_bind(pawn1, "<Enter>", on_enter1)
bl_canvas.tag_bind(pawn1, "<Leave>", on_leave1)
bl_canvas.tag_bind(text1, "<Enter>", on_enter1)
bl_canvas.tag_bind(text1, "<Leave>", on_leave1)

#Кнопка закрытия окна#########################################################
exit_img = Image.open("exit.png")
exit_photo = ImageTk.PhotoImage(exit_img)

ex_canvas = tk.Canvas(root, width=30, height=30, bg="#1c1c1c", highlightthickness=0)
ex_canvas.place(x=1050, y=10)
rect2 = create_rounded_rectangle(ex_canvas, 0, 0, 30, 30, radius=25, fill="#1c1c1c", outline="")


but_x = ex_canvas.create_image(15, 15, image=exit_photo) 

ex_canvas.tag_bind(rect2, "<Button-1>", lambda event: close_window()) 
ex_canvas.tag_bind(but_x, "<Button-1>", lambda event: close_window()) 

ex_canvas.tag_bind(rect2, "<Enter>", on_enter2)
ex_canvas.tag_bind(rect2, "<Leave>", on_leave2)
ex_canvas.tag_bind(but_x, "<Enter>", on_enter2)
ex_canvas.tag_bind(but_x, "<Leave>", on_leave2)
# Подпись снизу ###########################################################################
footer = tk.Label(root, text="Final project for ITStep", font=custom_font3, fg="white", bg="#1c1c1c")
footer.place(x=915, y=570)
###############################################Ползунок сложности
# Создание кастомного ползунка
difficulty_label = tk.Label(root, text="Bot Difficulty", font=custom_font, fg="white", bg="#1c1c1c")
difficulty_label.place(x=650, y=350)

slider_canvas = tk.Canvas(root, width=300, height=80, bg="#1c1c1c", highlightthickness=0)
slider_canvas.place(x=610, y=420)

slider_canvas.create_rectangle(50, 25, 250, 35, fill="#59946f", outline="black",width=1)

current_difficulty = tk.StringVar(value="Medium")

slider_knob = slider_canvas.create_oval(125, 15, 145, 45, fill="#59946f", outline="black", width=2)



def move_slider(event):
    x = min(max(event.x, 50), 250) 
    slider_canvas.coords(slider_knob, x - 10, 15, x + 10, 45)
    if x < 100:
        current_difficulty.set("Easy")
    elif x < 200:
        current_difficulty.set("Medium")
    else:
        current_difficulty.set("Hard")

    difficulty_label.config(text=current_difficulty.get())

def on_knob_hover(event):
    slider_canvas.itemconfig(slider_knob, fill="#81b64c")######цвет при наведении

def on_knob_leave(event):
    slider_canvas.itemconfig(slider_knob, fill="#59946f")

slider_canvas.tag_bind(slider_knob, "<B1-Motion>", move_slider) 
slider_canvas.tag_bind(slider_knob, "<Enter>", on_knob_hover) 
slider_canvas.tag_bind(slider_knob, "<Leave>", on_knob_leave) 

difficulty_label = tk.Label(root, text=current_difficulty.get(), font=custom_font1, fg="white", bg="#1c1c1c")
difficulty_label.place(x=900, y=430)




root.mainloop()
