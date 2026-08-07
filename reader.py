import headyawtracker
import fitz  # PyMuPDF

from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Sheetviewer")
root.state('zoomed')
# Open PDF and find total pages
doc = fitz.open("example.pdf")
total_pages = len(doc)
current_page = 0  
old_page = 0

pages = []
photos = [] 


page_frame = Frame(root)
page_frame.place(x=0,y=0)

def update_page_display():
    page_frame.place(x=-current_page*headyawtracker.screen_width,y=0)

def setup_pages():
    global pages
    global photos
    for i in range(total_pages):
        label = Label(page_frame, border=False, bg='#FFFFFF', width=headyawtracker.screen_width, height=headyawtracker.screen_height)
        pages.append(label)
    for i in range(len(pages)):
        page = pages[i]
        page_obj = doc.load_page(i)
        pix = page_obj.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        photo = ImageTk.PhotoImage(img)
        photos.append(photo)
        page.config(image=photo)
        page.grid(column=i, row=0)

setup_pages()
print(len(pages), "pages")

def lerp(a,b,t):
    t = max(0.0, min(t,1.0))
    return a + t*(b-a)

def from_rgb(rgb):
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

def lerp_color(a, b, t):
    red = int(lerp(a[0],b[0],t))
    green = int(lerp(a[1],b[1],t))
    blue = int(lerp(a[2],b[2],t))
    return from_rgb([red,green,blue])

headyawtracker.settings["turn_time"] = 0.5
headyawtracker.settings["turn_begin_threshold_degrees"] = 20

while True:
    root.update()
    
    col = lerp_color([30, 30, 30], [0,0,0], headyawtracker.turning_progress)
    root.configure(bg=col)
    
    headyawtracker.Track()
    
    if headyawtracker.turn == "right":
        if current_page < total_pages - 1:
            current_page += 1
            update_page_display()
            old_page = current_page
            
    elif headyawtracker.turn == "left":
        if current_page > 0:
            current_page -= 1
            update_page_display()
            old_page = current_page
