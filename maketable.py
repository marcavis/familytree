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
        images[name] = Image.open(os.path.join(folder_path, filename)).resize((OC_SIZE, OC_SIZE))


# Open the families file
with open("families.txt", "r") as f:
    # Initialize the list of families
    families = []
    moms = []
    dads = []

    # Loop over each line in the file
    for line in f:
        # Split the line into a tuple of names
        thesenames = tuple(line.lower().strip().split())
        
        # Append the tuple to the list of families
        families.append(thesenames)

        moms.append(thesenames[1])
        dads.append(thesenames[2])

moms = list(set(moms))
dads = list(set(dads))

# Print the list of families
# print(families)

names = list(set([elem for tup in families for elem in tup]))
#names = ['lea', 'kazue', 'karin', 'aedus', 'aoife', 'myou']

# Create a new image for the table
table_width = len(dads) * OC_SIZE + OC_SIZE
table_height = len(moms) * OC_SIZE + OC_SIZE
table_image = Image.new('RGB', (table_width, table_height), (255, 255, 255))


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

rollcalldads = enumerate(dads)
for i, name in rollcalldads:
    x = (i + 1) * grid_step 
    y = 0 * grid_step 
    try:
        table_image.paste(images[name], (x, y), images[name])
    except KeyError:
        # If the image doesn't exist, draw the name instead
        table_image.paste(images['unknown'], (x, y), images['unknown'])
        draw.text((x+20, y+100), name, font=font, fill=(0, 0, 0))
    except ValueError:
        #this portrait isn't transparent
        table_image.paste(images[name], (x, y))

rollcallmoms = enumerate(moms)
for i, name in rollcallmoms:
    x = (i + 1) * grid_step 
    y = 0 * grid_step 
    try:
        table_image.paste(images[name], (y, x), images[name])
    except KeyError:
        # If the image doesn't exist, draw the name instead
        table_image.paste(images['unknown'], (y, x), images['unknown'])
        draw.text((y+20, x+100), name, font=font, fill=(0, 0, 0))
    except ValueError:
        #this portrait isn't transparent
        table_image.paste(images[name], (y, x))


for p in families:
    childpos = (dads.index(p[2]) * grid_step + grid_step, moms.index(p[1]) * grid_step + grid_step)
    try:
        table_image.paste(images[p[0]], childpos, images[p[0]])
    except KeyError:
        # If the image doesn't exist, draw the name instead
        table_image.paste(images['unknown'], childpos, images['unknown'])
        draw.text((childpos[0]+20, childpos[1]+100), p[0], font=font, fill=(0, 0, 0))
    except ValueError:
        #this portrait isn't transparent
        table_image.paste(images[p[0]], childpos)

# Save the table image to a file
table_image.save('board.png')