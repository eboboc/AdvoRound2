from tkinter import *
from PIL import ImageTk, Image, ImageDraw
import math
import random


def impressionism(image_path):
    img = Image.open(image_path)
    width, height = img.size


    circle_radius = 8
    angle_step = 10  

    for y in range(0, height, 15):
        for x in range(0, width, 15):
            color = img.getpixel((x, y))
            for angle in range(0, 360, angle_step):
                for r in range(1, circle_radius):
                    x1 = r * math.cos(math.radians(angle))
                    y1 = r * math.sin(math.radians(angle))
                    new_x = round(x + x1)
                    new_y = round(y + y1)
                    if 0 <= new_x < width and 0 <= new_y < height:
                        img.putpixel((new_x, new_y), color)

    return img

def modify_colors(image, r_factor, g_factor, b_factor):
    img = image.copy()
    pixels = img.load()
    width, height = img.size

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            r = int(r * r_factor)
            g = int(g * g_factor)
            b = int(b * b_factor)
            pixels[x, y] = (r, g, b)

    return img


def cubism(image_path, num_pieces):

    img = Image.open(image_path)

    width, height = img.size

    # Calculate the number of rows and columns based on the total number of pieces
    cols = int(math.sqrt(num_pieces))
    rows = num_pieces // cols

    piece_widths = [random.randint(width // 5, width // 3) for _ in range(cols)]
    piece_heights = [random.randint(height // 5, height // 3) for _ in range(rows)]

    pieces = []

    for i in range(cols):
        for j in range(rows):
            left = sum(piece_widths[:i])
            upper = sum(piece_heights[:j])
            right = left + piece_widths[i]
            lower = upper + piece_heights[j]
            piece = img.crop((left, upper, right, lower))
            pieces.append(piece)

    random.shuffle(pieces)

    # Create a new image and paste the shuffled pieces
    cubist_img = Image.new("RGB", (width, height), img.getpixel((0, 0)))

    for i in range(cols):
        for j in range(rows):
            piece = pieces[i * rows + j]
            left = sum(piece_widths[:i])
            upper = sum(piece_heights[:j])
            cubist_img.paste(piece, (left, upper))

    return cubist_img


def andy_warhol_with_filters(image_path):

    img = Image.open(image_path)

    width, height = img.size

    frame_width = img_width * 3  
    frame_height = img_height * 2 

    width_scale = frame_width / width
    height_scale = frame_height / height

    scale_factor = min(width_scale, height_scale)

    img = img.resize((int(width * scale_factor), int(height * scale_factor)))

    # Get the new dimensions
    width, height = img.size

    # Create a new image for the 3x2 grid with color filters
    warhol_img = Image.new("RGB", (width * 3, height * 2))

    color_filters = [
        (1.6, 1.3, 1.1),  
        (1.0, 1.1, 1.6),  
        (1.3, 1.1, 1.0),  
        (1.1, 1.0, 1.6),
        (1.6, 1.1, 1.3), 
        (1.3, 1.6, 1.1)  
    ]

    for i in range(3):
        for j in range(2):
            piece = img.copy()
            r_factor, g_factor, b_factor = color_filters[i * 2 + j]
            piece = modify_colors(piece, r_factor, g_factor, b_factor)
            left = i * width
            upper = j * height
            warhol_img.paste(piece, (left, upper))

    return warhol_img

def process_image():
    selected_function = function_var.get()
    input_image_path = file_var.get()
    num_pieces = int(num_pieces_var.get()) if selected_function == "Cubism" else 0

    if selected_function == "Impressionism":
        processed_image = impressionism(input_image_path)
    elif selected_function == "Cubism":
        processed_image = cubism(input_image_path, num_pieces)
        r_factor = 1.5 
        g_factor = 1.2  
        b_factor = 1.0  
        processed_image = modify_colors(processed_image, r_factor, g_factor, b_factor)
    elif selected_function == "Andy Warhol":
        processed_image = andy_warhol_with_filters(input_image_path)
    else:
        return

    img = ImageTk.PhotoImage(processed_image)
    label.config(image=img)
    label.image = img

win = Tk()
win.title("Image Processing")

# Function selection
function_var = StringVar()
function_var.set("Impressionism")
function_menu = OptionMenu(win, function_var, "Impressionism", "Cubism", "Andy Warhol")
function_menu.pack()

# File selection
file_label = Label(win, text="Input Image:")
file_label.pack()
file_var = Entry(win)
file_var.pack()

# Number of pieces entry (for Cubism)
num_pieces_label = Label(win, text="Number of Pieces (for Cubism):")
num_pieces_label.pack()
num_pieces_var = Entry(win)
num_pieces_var.pack()

# Dimensions for Andy Warhol effect
img_width = 150
img_height = 150

# Process button
process_button = Button(win, text="Process Image", command=process_image)
process_button.pack()

# Display label
label = Label(win)
label.pack()

win.mainloop()
