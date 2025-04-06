from PIL import Image


# Open an existing image
image = Image.open("indexed_image.bmp")

# Create a new image with a palette
image = Image.new("P", (256, 256))


# Get the current palette (if any)
palette = image.getpalette()

# Define a new palette (list of RGB triplets)
new_palette = [
    0, 0, 0,    # Index 0: Black
    255, 0, 0,  # Index 1: Red
    255, 255, 255,  # Index 2: Green
]

# Flatten the palette if needed
flat_palette = [item for sublist in [new_palette[i:i+3] for i in range(0, len(new_palette), 3)] for item in sublist]

# Set the palette
image.putpalette(flat_palette)


# Save the image as an indexed BMP
image.save("output_indexed.bmp")
