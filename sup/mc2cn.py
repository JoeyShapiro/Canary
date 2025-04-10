from PIL import Image

# open png
mc = Image.open("sup/ascii.png")

# TODO only get list of thigns i need

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
        if sprite.getbbox() is None:
            continue

        sprite = sprite.resize((16, 16), Image.NEAREST)
        # TODO save as indexed bmp
        sprite.save(f"sup/mc/sprite_{x}_{y}.png")
