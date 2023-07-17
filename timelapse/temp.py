import math
import matplotlib.pyplot as plt
import numpy as np


total_items = 4800
ratio = 1 / 4

# Calculate the number of columns (m) and rows (n)
m = round(math.sqrt(total_items / ratio))
n = round(total_items / m)

# Create the array with n rows and m columns
arr = [[None] * m for _ in range(n)]

# Populate the array with the desired number of items (e.g., 1000 items)
# ...

# Print the dimensions of the array
print(f"The array dimensions: {n} x {m}")


# Generate random colors for each element in the array
colors = np.random.choice(['plum', 'plum', 'blue', 'yellow'], size=(n, m))

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Plot the colored boxes with gaps between each cell
for i in range(n):
    for j in range(m):
        color = 'lightgray'
        if i == (n-1) and j < 4:
            color = 'plum'
        rect = plt.Rectangle((j + 0.1, i + 0.1), 0.8, 0.8, color=color)
        ax.add_patch(rect)

# Remove ticks
ax.set_xticks([])
ax.set_yticks([])

# Set the aspect ratio and grid lines
ax.set_aspect('equal')
ax.grid(True, which='both', color='white', linewidth=0.1)

# Set the axis limits to add gaps between cells
ax.set_xlim(0, m)
ax.set_ylim(0, n)

# Customize the plot appearance
#ax.set_facecolor('lightgray')  # Set the background color of the plot area

# Add a border around the plot area
#ax.spines['top'].set_visible(True)
#ax.spines['bottom'].set_visible(True)
#ax.spines['left'].set_visible(True)
#ax.spines['right'].set_visible(True)

# Show the plot
plt.show()