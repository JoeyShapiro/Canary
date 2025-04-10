from PIL import Image

# open png
mc = Image.open("sup/ascii.png")

keep = {
    (0, 3): '0',
    (1, 3): '1',
    (2, 3): '2',
    (3, 3): '3',
    (4, 3): '4',
    (5, 2): 'per',
    (5, 3): '5',
    (6, 3): '6',
    (7, 3): '7',
    (8, 3): '8',
    (9, 3): '9',
    (10, 3): 'colon',
    (13, 2): 'minus',
    (14, 2): 'dot',
    (15, 3): 'err',
}

# create folder if not exists
import os
if not os.path.exists("mc"):
    os.makedirs("mc")

# break the atlast into 16x16 sprites
px = 8
rows = mc.size[1] // px
cols = mc.size[0] // px

for y in range(cols):
    for x in range(rows):
        # crop the image
        box = (x * px, y * px, (x + 1) * px, (y + 1) * px)
        sprite = mc.crop(box)

        # check if all transparent
        if (x, y) not in keep or sprite.getbbox() is None:
            continue

        sprite = sprite.resize((16, 16), Image.NEAREST)
        
        # Open an existing image
        image = Image.new("P", (16, 16))
        new_palette = [
            255, 255, 255,
            255, 0, 0,
            0, 0, 0,
        ]
        flat_palette = [item for sublist in [new_palette[i:i+3] for i in range(0, len(new_palette), 3)] for item in sublist]
        image.putpalette(flat_palette)
        image.paste(sprite, (0, 0))

        # change all red to black
        pixels = list(image.getdata())
        new_pixels = []
        for pixel in pixels:
            if pixel == 1:
                new_pixels.append(2)
            else:
                new_pixels.append(pixel)
        image.putdata(new_pixels)

        image.save(f"mc/{keep[(x, y)]}.bmp")
        image.close()
