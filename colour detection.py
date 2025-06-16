import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import pandas as pd

#load color data
CSV_FILE = r'C:\Users\ACER\Documents\colors.csv'
columns = ["color", "color_name", "hex", "R", "G", "B"]
color_data = pd.read_csv(CSV_FILE, names=columns, header=None)

#pixel position
img_cv = None
img_tk = None
r = g = b = xpos = ypos = 0

#max canvas size
MAX_WIDTH = 800
MAX_HEIGHT = 500

#find matching color
def get_color_name(R, G, B):
    min_dist = float('inf')
    color_name = "Unknown"
    for i in range(len(color_data)):
        d = abs(int(R) - int(color_data.loc[i, "R"])) + \
            abs(int(G) - int(color_data.loc[i, "G"])) + \
            abs(int(B) - int(color_data.loc[i, "B"]))
        if d < min_dist:
            min_dist = d
            color_name = color_data.loc[i, "color_name"]
    return color_name

#open & display image
def open_image():
    global img_cv, img_tk
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
    if not file_path:
        return

    img_cv_original = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
    height, width = img_cv_original.shape[:2]

    #resize image if too large
    scale = min(MAX_WIDTH / width, MAX_HEIGHT / height, 1.0)
    new_width = int(width * scale)
    new_height = int(height * scale)
    img_cv = cv2.resize(img_cv_original, (new_width, new_height))

    img_pil = Image.fromarray(img_cv)
    img_tk = ImageTk.PhotoImage(img_pil)

    canvas.config(width=new_width, height=new_height)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

#mouse click
def on_click(event):
    global r, g, b, xpos, ypos
    xpos, ypos = event.x, event.y
    if img_cv is not None and 0 <= xpos < img_cv.shape[1] and 0 <= ypos < img_cv.shape[0]:
        r, g, b = img_cv[ypos, xpos]
        show_color_info()

#show color name & rgb value
def show_color_info():
    color_name = get_color_name(r, g, b)
    color_hex = f'#{r:02x}{g:02x}{b:02x}'
    info_text = f"{color_name}   R={r} G={g} B={b}"

    color_display.config(bg=color_hex)
    label_result.config(
        text=info_text,
        bg=color_hex,
        fg='black' if (int(r) + int(g) + int(b)) >= 600 else 'white'
    )

#GUI setup
root = tk.Tk()
root.title("Color Detection App")
root.geometry("850x650")

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

btn_open = tk.Button(top_frame, text="Open Image", command=open_image, font=("Arial", 12))
btn_open.pack()

canvas = tk.Canvas(root, bg='gray')
canvas.pack()
canvas.bind("<Button-1>", on_click)

color_display = tk.Label(root, text="", width=40, height=2)
color_display.pack(pady=5)

label_result = tk.Label(root, text="Click anywhere on the image to detect color", font=("Arial", 14))
label_result.pack(pady=5)

root.mainloop()