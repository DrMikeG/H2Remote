import math
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

# Determine the size of the array (n x m)
n = 10
m = 10
n_sm = 10

# Create the checkerboard pattern
checkerboard = np.indices((n, m)).sum(axis=0) % 2
checkerboard_sm = np.indices((n_sm, m)).sum(axis=0) % 2

# Define the colors for light gray, dark gray, and plum
light_gray = 'lightgray'
dark_gray = 'darkgray'
plum = 'plum'

# Set the first four pixels in the top row to plum color
#checkerboard[0, :4] = 2

# Create the figure and axis for the subplots
fig, axs = plt.subplots(1, 5, figsize=(12, 3))

# Plot the images side-by-side
images = [checkerboard, checkerboard, checkerboard, checkerboard, checkerboard_sm]
titles = ['Image 1', 'Image 2', 'Image 3', 'Image 4','Image 5']

for i in range(5):
    axs[i].imshow(images[i], cmap=plt.cm.colors.ListedColormap([light_gray, dark_gray, plum]))
    axs[i].set_title(titles[i])
    axs[i].set_xticks([])
    axs[i].set_yticks([])

# Adjust the spacing between subplots
plt.subplots_adjust(wspace=0.05)

# Show the plot
plt.show()
