
############
# Author: Jon Welch 
# PHYS-2425: Engineering Physics 1 
# Purpose: Measurement Lab part 1
# Note: With violin plot
# Date: [9-7-24] 
############




#############
'''

Understanding the Violin Plot & Shape:

The shape of each "violin" reflects the distribution of the data points.
The width of the violin at different points represents the density or frequency of the data values at that level. A wider section indicates that more data points are
concentrated around that value.

Central Line and Box:

The central black line shows the range between the first quartile (Q1) and third quartile (Q3) of the data, known as the interquartile range (IQR).
The small blue box-dot represents the median of the data.

The vertical lines [whiskers] extending above and below the box show the range of data points that fall within 1.5 times the IQR from Q1 and Q3. They help to identify potential
outliers beyond this range.

What the Plot Shows:

For Length [the first violin plot]:
The violin plot is relatively flat, indicating the measurements are closely clustered around a central value [152.2 cm].

The median [blue box-dot] is near the middle of the violin, and the shape is symmetrical, showing that the data is fairly evenly distributed around the median.
The width of the violin suggests that most of the data points are close to the mean length value, with little variation.

The plot only displays the "Length" data prominently because the violin plot uses three different measurements [length, width, and thickness], but the scale is heavily
affected by the much larger range of the length measurements (around 152 cm), making the width and thickness distributions less visible.

Effect of Data Clustering:

If several data points are exactly at the same value [like multiple measurements of "Length" being 152.2], the whisker will appear thicker at that point
because it's visually stacking multiple overlapping lines.

'''
############




import numpy as np
import matplotlib.pyplot as plt


# Data: Measurements of the length, width, and thickness of the tabletop (in cm)
length_measurements = np.array([152.2, 152.2, 152.0, 152.4, 152.0])  
width_measurements = np.array([60.5, 60.8, 60.5, 60.7, 60.5])         
thickness_measurements = np.array([3.2, 3.3, 3.2, 3.3, 3.3])  

    
# Step 1: Calculate the mean values
mean_length = np.mean(length_measurements)
mean_width = np.mean(width_measurements)
mean_thickness = np.mean(thickness_measurements)

# Step 2: Calculate the standard deviation
std_length = np.std(length_measurements, ddof=1)  # Using ddof=1 for sample standard deviation
std_width = np.std(width_measurements, ddof=1)
std_thickness = np.std(thickness_measurements, ddof=1)

# Step 3: Calculate the standard error
stderr_length = std_length / np.sqrt(len(length_measurements))
stderr_width = std_width / np.sqrt(len(width_measurements))
stderr_thickness = std_thickness / np.sqrt(len(thickness_measurements))

# Step 4: Calculate surface area and volume
surface_area = 2 * (mean_length * mean_width + mean_length * mean_thickness + mean_width * mean_thickness)
volume = mean_length * mean_width * mean_thickness

# Step 5: Calculate the uncertainties using the absolute value formula

# Partial derivatives for surface area
dSA_dL = 2 * (mean_width + mean_thickness)
dSA_dW = 2 * (mean_length + mean_thickness)
dSA_dT = 2 * (mean_length + mean_width)

# Uncertainty for surface area using the absolute value formula
delta_surface_area = abs(dSA_dL) * stderr_length + abs(dSA_dW) * stderr_width + abs(dSA_dT) * stderr_thickness

# Partial derivatives for volume
dV_dL = mean_width * mean_thickness
dV_dW = mean_length * mean_thickness
dV_dT = mean_length * mean_width

# Uncertainty for volume using the absolute value formula
delta_volume = abs(dV_dL) * stderr_length + abs(dV_dW) * stderr_width + abs(dV_dT) * stderr_thickness

# Preparing data for the violin plot
data = [length_measurements, width_measurements, thickness_measurements]

# Creating the violin plot
#was(12,8)
fig, ax = plt.subplots(figsize=(24, 24))  # Adjusted figure size for clarity
ax.set_title('Violin Plot of Measurements with Mean and Uncertainties [Jon Welch]')
parts = ax.violinplot(data, showmeans=False, showmedians=False, showextrema=False)

# Customizing each violin
for pc in parts['bodies']:
    pc.set_facecolor('#D43F3A')  # Custom color
    pc.set_edgecolor('black')  # Black edge color
    pc.set_alpha(0.7)  # Partial transparency for visual appeal

# Calculating quartiles and whiskers
quartile1, medians, quartile3 = np.percentile(data, [25, 50, 75], axis=1)
whiskers_min = [np.min(d) for d in data]
whiskers_max = [np.max(d) for d in data]

# Overlaying medians, quartiles, and whiskers
inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker='s', color='blue', s=30, zorder=3)
ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
ax.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)

# Set style for the axes
labels = ['Length', 'Width', 'Thickness']
ax.set_xticks(np.arange(1, len(labels) + 1))
ax.set_xticklabels(labels)
ax.set_xlabel('Measurement Type')
ax.set_ylabel('Values (cm)')

# Adding the table with calculated values including standard deviations
table_data = [
    ['Length', f'{mean_length:.2f}', f'{std_length:.4f}', f'{stderr_length:.4f}'],
    ['Width', f'{mean_width:.2f}', f'{std_width:.4f}', f'{stderr_width:.4f}'],
    ['Thickness', f'{mean_thickness:.2f}', f'{std_thickness:.4f}', f'{stderr_thickness:.4f}'],
    ['Surface Area', f'{surface_area:.2f}', '-', f'{delta_surface_area:.2f}'],
    ['Volume', f'{volume:.2f}', '-', f'{delta_volume:.2f}']
]

# Add the table to the plot
table = plt.table(cellText=table_data, colLabels=['Measurement', 'Mean Value (cm or cm$^2$/cm$^3$)', 'Standard Deviation (cm)', 'Uncertainty (cm)'], loc='bottom', cellLoc='center', bbox=[0, -0.4, 1, 0.3])
table.auto_set_font_size(False)
table.set_fontsize(10)

# Adjust layout to make room for the table
plt.subplots_adjust(left=0.2, bottom=0.4)

# Adding a text box with summary data
summary_text = (
    f"Mean Length: {mean_length:.2f} cm, Standard Error: {stderr_length:.4f} cm\n"
    f"Mean Width: {mean_width:.2f} cm, Standard Error: {stderr_width:.4f} cm\n"
    f"Mean Thickness: {mean_thickness:.2f} cm, Standard Error: {stderr_thickness:.4f} cm\n"
    f"Surface Area: {surface_area:.2f} cm², Uncertainty in Surface Area: {delta_surface_area:.2f} cm²\n"
    f"Volume: {volume:.2f} cm³, Uncertainty in Volume: {delta_volume:.2f} cm³"
)
plt.figtext(0.7, 0.05, summary_text, wrap=True, horizontalalignment='center', fontsize=10)




############[ Normalize the data for plot ]#################





data = [
    (length_measurements - mean_length) / std_length,
    (width_measurements - mean_width) / std_width,
    (thickness_measurements - mean_thickness) / std_thickness
]

# Create the violin plot
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_title('Normalized Violin Plot of Measurements with Mean and Uncertainties [Jon Welch]')
parts = ax.violinplot(data, showmeans=False, showmedians=False, showextrema=False)

# Customize the violin plot appearance
for pc in parts['bodies']:
    pc.set_facecolor('#D43F3A')
    pc.set_edgecolor('black')
    pc.set_alpha(0.7)

# Calculate quartiles and whiskers for normalized data
quartile1, medians, quartile3 = np.percentile(data, [25, 50, 75], axis=1)
whiskers_min = [np.min(d) for d in data]
whiskers_max = [np.max(d) for d in data]

# Overlay medians, quartiles, and whiskers
inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker='s', color='blue', s=30, zorder=3)
ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
ax.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)

# Set axis labels and ticks
labels = ['Length', 'Width', 'Thickness']
ax.set_xticks(np.arange(1, len(labels) + 1))
ax.set_xticklabels(labels)
ax.set_xlabel('Measurement Type')
ax.set_ylabel('Normalized Values')

# Adding a table with calculated values including standard deviations
table_data = [
    ['Length', f'{mean_length:.2f}', f'{std_length:.4f}', f'{stderr_length:.4f}'],
    ['Width', f'{mean_width:.2f}', f'{std_width:.4f}', f'{stderr_width:.4f}'],
    ['Thickness', f'{mean_thickness:.2f}', f'{std_thickness:.4f}', f'{stderr_thickness:.4f}'],
    ['Surface Area', f'{surface_area:.2f}', '-', f'{delta_surface_area:.2f}'],
    ['Volume', f'{volume:.2f}', '-', f'{delta_volume:.2f}']
]

# Add the table to the plot
table = plt.table(cellText=table_data, colLabels=['Measurement', 'Mean Value (cm or cm$^2$/cm$^3$)', 'Standard Deviation (cm)', 'Uncertainty (cm)'], loc='bottom', cellLoc='center', bbox=[0, -0.4, 1, 0.3])
table.auto_set_font_size(False)
table.set_fontsize(10)

# Adjust layout to make room for the table
plt.subplots_adjust(left=0.2, bottom=0.4)

# Adding a text box with summary data
summary_text = (
    f"Mean Length: {mean_length:.2f} cm, Standard Error: {stderr_length:.4f} cm\n"
    f"Mean Width: {mean_width:.2f} cm, Standard Error: {stderr_width:.4f} cm\n"
    f"Mean Thickness: {mean_thickness:.2f} cm, Standard Error: {stderr_thickness:.4f} cm\n"
    f"Surface Area: {surface_area:.2f} cm², Uncertainty in Surface Area: {delta_surface_area:.2f} cm²\n"
    f"Volume: {volume:.2f} cm³, Uncertainty in Volume: {delta_volume:.2f} cm³"
)
plt.figtext(0.7, 0.05, summary_text, wrap=True, horizontalalignment='center', fontsize=10)

# Show the plot2

plt.show()


