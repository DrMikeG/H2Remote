import math
import matplotlib.pyplot as plt
import numpy as np


## This is how much is used in an hour

total_items = 1000 * 10
ratio = 1 / 4

# Calculate the number of columns (m) and rows (n)
m = round(math.sqrt(total_items / ratio))
n = round(total_items / m)

# Create the checkerboard pattern
checkerboard = np.indices((n, m)).sum(axis=0) % 2

# Define the colors for light gray, dark gray, and plum
light_gray = 'lightgray'
dark_gray = 'darkgray'
plum = 'plum'

# Set the first four pixels in the top row to plum color
checkerboard[0, :4] = 2

# Create the figure and axis for the plot
fig, ax = plt.subplots()

# Create the image plot with the checkerboard pattern and plum color
ax.imshow(checkerboard, cmap=plt.cm.colors.ListedColormap([light_gray, dark_gray, plum]))

# Remove ticks
ax.set_xticks([])
ax.set_yticks([])

# Show the plot
plt.show()