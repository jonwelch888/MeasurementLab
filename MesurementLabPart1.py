
############
# Author: Jon Welch 
# PHYS-2425: Engineering Physics 1 
# Purpose: Mesurement Lab part 1
# Note: Data is related to a Tabletop
# Date: [8-29-24] 
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

# Plotting the means and their uncertainties
fig, ax = plt.subplots(figsize=(12, 8))  # Adjusted figure size for clarity
measurements = ['Length', 'Width', 'Thickness']
mean_values = [mean_length, mean_width, mean_thickness]
stderr_values = [stderr_length, stderr_width, stderr_thickness]

# Plotting with error bars
ax.errorbar(measurements, mean_values, yerr=stderr_values, fmt='o', capsize=5, label='Mean Values with Uncertainty')

# Adding labels and title
plt.xlabel('Measurements')
plt.ylabel('Values (cm)')
plt.title('Mean Measurements of Tabletop with Uncertainties [Jon Welch]')
plt.grid(True)
plt.legend()

# Creating a table with calculated values including standard deviations
table_data = [
    ['Length', f'{mean_length:.2f}', f'{std_length:.4f}', f'{stderr_length:.4f}'],
    ['Width', f'{mean_width:.2f}', f'{std_width:.4f}', f'{stderr_width:.4f}'],
    ['Thickness', f'{mean_thickness:.2f}', f'{std_thickness:.4f}', f'{stderr_thickness:.4f}'],
    ['Surface Area', f'{surface_area:.2f}', '-', f'{delta_surface_area:.2f}'],
    ['Volume', f'{volume:.2f}', '-', f'{delta_volume:.2f}']
]

# Add the table to the plot
#[0, -0.8, 1, 0.6]
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
#best, [0.7, 0.05,]; 
# Display the summary text at the bottom
plt.figtext(0.7, 0.05, summary_text, wrap=True, horizontalalignment='center', fontsize=10)

# Show the plot
plt.show()
