WIDTH = display.width
HEIGHT = display.height
STRIPE_WIDTH = WIDTH // 3

# Create a bitmap with 3 colors (0, 1, 2)
bitmap = displayio.Bitmap(WIDTH, HEIGHT, 3)

# Fill bitmap with vertical stripes of each color
for x in range(WIDTH):
    for y in range(HEIGHT):
        if x < STRIPE_WIDTH:
            bitmap[x, y] = 0  # First third: Black
        elif x < STRIPE_WIDTH * 2:
            bitmap[x, y] = 1  # Middle third: White
        else:
            bitmap[x, y] = 2  # Last third: Red

# Create a palette with the three colors
palette = displayio.Palette(3)
palette[0] = 0x000000  # Black
palette[1] = 0xFFFFFF  # White
palette[2] = 0xFF0000  # Red

# Create the TileGrid using the bitmap and palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
tile_grid.x = 0  # Start at top-left
tile_grid.y = 0

# Add the TileGrid to the main group to display it
main_group.append(tile_grid)