from PIL import Image, ImageDraw, ImageFont
import os

def pasteat(oc, x, y, table, images):
    table.paste(images[oc],(x*150,y*150),images[oc])

folder_path = 'portraits'
images = {}
OC_SIZE = 150

# Iterate over the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a PNG image
    if filename.endswith('.png'):
        # Extract the name of the image from the filename
        name = os.path.splitext(filename)[0]
        # Load the image using Pillow and store it in the dictionary
        images[name] = Image.open(os.path.join(folder_path, filename))

# Create a new image for the table
table_width = 6 * OC_SIZE
table_height = 6 * OC_SIZE
table_image = Image.new('RGB', (table_width, table_height), (255, 255, 255))

# Paste the oc images onto the table
# pasteat('lea', 1, 0, table_image, images)
# pasteat('lea', 0, 1, table_image, images)
# pasteat('kazue', 2, 0, table_image, images)
# pasteat('kazue', 0, 2, table_image, images)
# pasteat('karin', 3, 0, table_image, images)
# pasteat('karin', 0, 3, table_image, images)
# pasteat('tohka', 4, 0, table_image, images)
# pasteat('tohka', 0, 4, table_image, images)
# pasteat('yuria', 5, 0, table_image, images)
# pasteat('yuria', 0, 5, table_image, images)


# Draw a grid on the image
grid_step = OC_SIZE
draw = ImageDraw.Draw(table_image)
for x in range(0, table_width, grid_step):
    draw.line([(x, 0), (x, table_height)], fill=(0, 0, 0), width = 3)
for y in range(0, table_height, grid_step):
    draw.line([(0, y), (table_width, y)], fill=(0, 0, 0), width = 3)

font_size = 36
font = ImageFont.truetype('arial.ttf', font_size)

draw.text((0,100), "MOMS↓", font=font, fill=(127,0,0))
draw.text((20,0), "DADS→", font=font, fill=(127,0,0))

# Draw the images or names onto the table
for i, name in enumerate(['lea', 'kazue', 'karin', 'aedus', 'aoife']):
    x = (i + 1) * grid_step 
    y = 0 * grid_step 
    try:
        table_image.paste(images[name], (x, y), images[name])
    except KeyError:
        # If the image doesn't exist, draw the name instead
        draw.text((x, y), name, font=font, fill=(0, 0, 0))
    try:
        table_image.paste(images[name], (y, x), images[name])
    except KeyError:
        # If the image doesn't exist, draw the name instead
        draw.text((y, x), name, font=font, fill=(0, 0, 0))

# Save the table image to a file
table_image.save('board.png')