import math
import matplotlib.pyplot as plt
import numpy as np

# Determine the size of the array (n x m)
## This is how much is used in the 12 hours I ran for

total_items = 4800
ratio = 3 / 2

# Calculate the number of columns (m) and rows (n)
m = round(math.sqrt(total_items / ratio))
n = round(total_items / m)
m2 = round(m * 0.8)
n2 = round(n * 0.8)

# Create the checkerboard pattern
checkerboard0 = np.indices((n, m)).sum(axis=0) % 2
checkerboard1 = np.indices((n, m)).sum(axis=0) % 2
checkerboard2 = np.indices((n, m)).sum(axis=0) % 2
checkerboard3 = np.indices((n, m)).sum(axis=0) % 2
checkerboard4 = np.indices((n2, m)).sum(axis=0) % 2

# Define the colors for light gray, dark gray, and plum
light_gray = 'lightgray'
dark_gray = 'darkgray'
plum = 'plum'

# Set the first four pixels in the top row to plum color
checkerboard0[0, :25*12] = 2

# Create the figure and axis for the subplots
fig, axs = plt.subplots(1, 5)#, figsize=(12, 3))

# Plot the images side-by-side
images = [checkerboard0, checkerboard1, checkerboard2, checkerboard3,checkerboard4]
titles = ['Image 1', 'Image 2', 'Image 3', 'Image 4', 'Image 5']

for i in range(5):
    if i==0:
        axs[i].imshow(images[i], cmap=plt.cm.colors.ListedColormap([light_gray,dark_gray,plum]))
    else:
        axs[i].imshow(images[i], cmap=plt.cm.colors.ListedColormap([light_gray,dark_gray]))
    #axs[i].set_title(titles[i])
    axs[i].set_xticks([])
    axs[i].set_yticks([])

#plt.annotate("4800mAh")
# Adjust the spacing between subplots
#plt.subplots_adjust(wspace=-0.20)

# Show the plot
plt.show()
