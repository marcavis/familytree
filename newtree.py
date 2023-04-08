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
with open("families2.txt", "r") as f:
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
            people[fam[1]].sires.append((fam[1], fam[2], fam[0]))
        if fam[1] not in people[fam[2]].dams:
            people[fam[2]].dams.append((fam[2], fam[1], fam[0]))

font_size = 36
font = ImageFont.truetype('arial.ttf', font_size)

births = []
for p in people:
    births = births + people[p].sires

levels = [people[p].getlevel() for p in people]
maxlevel = max(levels) 
#maxheight = max([levels.count(x) for x in range(maxlevel)])
relLevels = [max(people[b[0]].getlevel(), people[b[1]].getlevel()) for b in births]
maxheight = max([relLevels.count(x) for x in relLevels])

# Create a new image for the table
table_width = maxlevel * (OC_SIZE * 2 + SPACING)
table_height = maxheight * (OC_SIZE * 2 + SPACING)
table_image = Image.new('RGB', (table_width, table_height), (255, 255, 255))
draw = ImageDraw.Draw(table_image)


#let's start with moms
for i in range(0, maxlevel):
    j = 0
    for b in births:
        #person = people[p]
        mom = people[b[0]]
        dad = people[b[1]]
        kid = people[b[2]]
        relationshiplevel = max(mom.getlevel(), dad.getlevel())
        if relationshiplevel == i:
            mompos = (i*OC_SIZE*2 + i*SPACING, j*OC_SIZE + j*SPACING//2)
            dadpos = (i*OC_SIZE*2 + i*SPACING, j*OC_SIZE + OC_SIZE + j*SPACING//2)
            kidpos = (i*OC_SIZE*2 + OC_SIZE + i*SPACING, j*OC_SIZE + OC_SIZE//2 + j*SPACING//2)

            for box in [mompos, dadpos, kidpos]:
                draw.rectangle((box[0], box[1], box[0] + OC_SIZE - 1, box[1] + OC_SIZE - 1), outline="black", width=2)
            
            try:
                table_image.paste(images[mom.name], mompos, images[mom.name])
            except KeyError:
                # If the image doesn't exist, draw the name instead
                table_image.paste(images['unknown'], mompos, images['unknown'])
                draw.text(mompos, mom.name, font=font, fill=(0, 0, 0))
            except ValueError:
                #this portrait isn't transparent
                table_image.paste(images[mom.name], mompos)

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
            print(i, j)

# Save the table image to a file
table_image.save('pictree.png')