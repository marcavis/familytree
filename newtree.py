#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
import os

folder_path = 'portraits'
images = {}
OC_SIZE = 150
SPACING = 20

class Person:
    def __init__(self, name, mom=None, dad=None):
        self.name = name
        self.mom = mom
        self.dad = dad
        self.sires = []
        self.dams = []
    
    def getlevel(self):
        if not self.mom and not self.dad:
            return 0
        else:
            return max(self.mom.getlevel(), self.dad.getlevel()) + 1
        
    def __str__(self):
        if self.mom and self.dad:
            return f"Person({self.name} mom={self.mom.name} dad={self.dad.name})"
        return f"Person({self.name})"

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
    people = {}

    # Loop over each line in the file
    for line in f:
        # Split the line into a tuple of names
        thesenames = tuple(line.lower().strip().split())
        
        # Append the tuple to the list of families
        families.append(thesenames)

        people[thesenames[0]] = (Person(thesenames[0]))
        people[thesenames[1]] = (Person(thesenames[1]))
        people[thesenames[2]] = (Person(thesenames[2]))
    
    for fam in families:
        people[fam[0]].mom = people[fam[1]]
        people[fam[0]].dad = people[fam[2]]
        if fam[2] not in people[fam[1]].sires:
            people[fam[1]].sires.append((fam[2], fam[0], max(people[fam[1]].getlevel(), people[fam[2]].getlevel())))
        if fam[1] not in people[fam[2]].dams:
            people[fam[2]].dams.append((fam[1], fam[0], max(people[fam[1]].getlevel(), people[fam[2]].getlevel())))


print(people["aoife"].dams)
print(people["aoife"].sires)
# for p in people:
#     print(people[p])
# print (people["aoife"].getlevel())
# print (people["aoife"].mom.getlevel())
# print (people["aoife"].dad.getlevel())






# Draw a grid on the image
grid_step = OC_SIZE

# for x in range(0, table_width, grid_step):
#     draw.line([(x, 0), (x, table_height)], fill=(0, 0, 0), width = 3)
# for y in range(0, table_height, grid_step):
#     draw.line([(0, y), (table_width, y)], fill=(0, 0, 0), width = 3)

font_size = 36
font = ImageFont.truetype('arial.ttf', font_size)

#draw.text((0,100), "MOMS↓", font=font, fill=(127,0,0))
#draw.text((20,0), "DADS→", font=font, fill=(127,0,0))

# Draw the images or names onto the table

positions = {}
#TODO: check the person's level;
# if their parents are here, send to column (parent +1)
# first column:
# momdad = offspring
# AMALIAAMALIA = LEA

# second column:
# LEAMYOU = MIYA

for p in people:
    print(people[p], people[p].getlevel())
    
#maxlevel = max([people[p].getlevel() for p in people]) + 1
levels = [people[p].getlevel() for p in people]
maxlevel = max(levels) + 1
maxheight = max([levels.count(x) for x in range(maxlevel)])

# Create a new image for the table
table_width = maxlevel * (OC_SIZE + SPACING) * 2
table_height = maxheight * (OC_SIZE + SPACING) * 2
table_image = Image.new('RGB', (table_width, table_height), (255, 255, 255))
draw = ImageDraw.Draw(table_image)


births = [people[p].sires for p in people]
#let's start with moms
for i in range(0, maxlevel):
    j = 0
    for p in people:
        person = people[p]
        if person.getlevel() == i and len(person.sires) > 0:
            for other in person.sires:
                dad = people[other[0]]
                kid = people[other[1]]
                mompos = (i*OC_SIZE*2 + i*SPACING, j*OC_SIZE + j*SPACING)
                dadpos = (i*OC_SIZE*2 + i*SPACING, j*OC_SIZE + OC_SIZE + j*SPACING)
                kidpos = (i*OC_SIZE*2 + OC_SIZE + i*SPACING, j*OC_SIZE + OC_SIZE//2 + j*SPACING)

                for box in [mompos, dadpos, kidpos]:
                    draw.rectangle((box[0], box[1], box[0] + OC_SIZE - 1, box[1] + OC_SIZE - 1), outline="black", width=2)
                
                try:
                    table_image.paste(images[person.name], mompos, images[person.name])
                except KeyError:
                    # If the image doesn't exist, draw the name instead
                    table_image.paste(images['unknown'], mompos, images['unknown'])
                    draw.text(mompos, person.name, font=font, fill=(0, 0, 0))
                except ValueError:
                    #this portrait isn't transparent
                    table_image.paste(images[person.name], mompos)

                try:
                    table_image.paste(images[dad.name], dadpos, images[dad.name])
                except KeyError:
                    # If the image doesn't exist, draw the name instead
                    table_image.paste(images['unknown'], dadpos, images['unknown'])
                    draw.text(dadpos, dad.name, font=font, fill=(0, 0, 0))
                except ValueError:
                    #this portrait isn't transparent
                    table_image.paste(images[dad.name], dadpos)

                try:
                    table_image.paste(images[kid.name], kidpos, images[kid.name])
                except KeyError:
                    # If the image doesn't exist, draw the name instead
                    table_image.paste(images['unknown'], kidpos, images['unknown'])
                    draw.text(kidpos, kid.name, font=font, fill=(0, 0, 0))
                except ValueError:
                    #this portrait isn't transparent
                    table_image.paste(images[kid.name], kidpos)
                j = j + 2


# Save the table image to a file
table_image.save('pictree.png')