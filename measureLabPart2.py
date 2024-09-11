##################
# Author: Jon Welch 
# PHYS-2425: Engineering Physics 1 
# Purpose: Mesurement Lab part 2
# Note: Data is related to a cylinder
# Date: [8-29-24] 
##################

import numpy as np
import matplotlib.pyplot as plt

# Data: circumference and diameter of the five cylinders [in cm and mm]
circumference = np.array([3.1, 7.1, 10.9, 26.1, 43.2])  # in cm
diameter = np.array([9.7, 21.2, 35.8, 82.3, 148.2])     # in mm

# Convert diameters to cm for CONSISTENCY [must convert]
diameter = diameter / 10  # Convert from mm to cm

# Uncertainties [replace with actual uncertainties if/when provided]
uncertainty_circumference = np.array([0.1, 0.1, 0.1, 0.1, 0.1])  # example uncertainties
uncertainty_diameter = np.array([0.05, 0.05, 0.05, 0.05, 0.05])  

# Number of data points
N = len(circumference)

# Calculate means
mean_diameter = np.mean(diameter)
mean_circumference = np.mean(circumference)

# Calculate sums needed for linear regression
sum_x = np.sum(diameter)
sum_y = np.sum(circumference)
sum_xx = np.sum(diameter ** 2)
sum_xy = np.sum(diameter * circumference)

# Setting partial derivatives to zero and solving for slope [m] and intercept [b]
m = ((N*sum_xy) - (sum_x*sum_y)) / ((N*sum_xx) - (sum_x** 2))
b = mean_circumference - (m * mean_diameter)

# Step 1: take partial derivatives and set to zero
# Partial derivatives for S = sum((y_i - (m*x_i + b))^2)

###[not working]###
#partial_derivative_m = -2 * np.sum(diameter * (circumference - (mean_circumference + mean_diameter * (diameter - mean_diameter) )))
#partial_derivative_b = -2 * np.sum(circumference - (mean_circumference + mean_diameter * (diameter - mean_diameter) ))
###
partial_derivative_m = -2 * np.sum(diameter * (circumference - (m * diameter + b)))
partial_derivative_b = -2 * np.sum(circumference - (m * diameter + b))

# Step 2: Calculate residuals [differences between observed and predicted y values]
residuals = circumference - ((m * diameter) + b)

# Step 3: Calculate standard error of the estimate [Se]
Se = np.sqrt(np.sum(residuals ** 2) / (N - 2))

# Step 4: Calculate uncertainties in slope [m] and intercept [b]
###[not working]###
#b_uncertainty = m_uncertainty * np.sqrt(np.sum(diameter** 2) / N)
###
m_uncertainty = Se / np.sqrt(np.sum( (diameter - mean_diameter)** 2) )
b_uncertainty = Se * np.sqrt( (1 / N) + (mean_diameter ** 2 / np.sum((diameter - mean_diameter) ** 2)) )

# Step 5: Check second derivatives to verify minima
second_derivative_m = 2 * sum_xx
second_derivative_b = 2 * N

# if they are minima
minima_check_m = "minima" if second_derivative_m > 0 else "not minima"
minima_check_b = "minima" if second_derivative_b > 0 else "not minima"

# Calculate percent error relative to pi
percent_error = (abs(m - np.pi) / np.pi) * 100

# Print results in the shell for verification
print(f"Partial Derivative wrt m: {partial_derivative_m:.5f}, Partial Derivative wrt b: {partial_derivative_b:.5f}")
print("zero, is expected at the minimum of the sum of squared residuals.")
print(f"Second Derivative wrt m: {second_derivative_m} ({minima_check_m}), Second Derivative wrt b: {second_derivative_b} ({minima_check_b})")
print(f"Slope (m): {m:.5f} cm/cm, Intercept (b): {b:.5f} cm")
print(f"Uncertainty in Slope: {m_uncertainty:.5f} cm/cm, Uncertainty in Intercept: {b_uncertainty:.5f} cm")
print(f"Percent Error: {percent_error:.2f}%")

# Plotting the data
plt.figure(figsize=(10, 6))
plt.errorbar(diameter, circumference, xerr=uncertainty_diameter, yerr=uncertainty_circumference, fmt='o', capsize=5, label='Data Points with Uncertainty')

# Plot the best fit line
x_fit = np.linspace(min(diameter), max(diameter), 100)
y_fit = m * x_fit + b
plt.plot(x_fit, y_fit, '-', label=f'Best Fit Line: y = {m:.5f}x + {b:.5f}')

# Labels and title
plt.xlabel('[X-axis] Diameter (cm)')
plt.ylabel('[Y-axis] Circumference (cm)')
plt.title('Circumference vs. Diameter of Cylinders   [Jon Welch]')
plt.grid(True)
plt.legend()


# Creating a table with the calculated values
table_data = [
    ['Partial Derivative wrt m', f'{partial_derivative_m:.5f}'],
    ['Partial Derivative wrt b', f'{partial_derivative_b:.5f}'],
    ['Second Derivative wrt m', f'{second_derivative_m:.5f} ({minima_check_m})'],
    ['Second Derivative wrt b', f'{second_derivative_b:.5f} ({minima_check_b})'],
]

# Add the table  # best; bbox=[0, -0.8, 1, 0.6]
table = plt.table(cellText=table_data, colLabels=['Description', 'Value'], loc='bottom', cellLoc='center', bbox=[0, -0.8, 1, 0.6])
table.auto_set_font_size(False)
table.set_fontsize(10)

# Adjust to make room for the table
plt.subplots_adjust(left=0.2, bottom=0.4)

# Text box with data on the graph
summary_text = (
    f"Slope (m): {m:.5f} cm/cm\n"
    f"Intercept (b): {b:.5f} cm\n"
    f"Uncertainty in m: {m_uncertainty:.5f} cm/cm\n"
    f"Uncertainty in b: {b_uncertainty:.5f} cm\n"
    f"Percent Error: {percent_error:.2f}%"
)
#[For data box] was[0.05, 0.05,]; Alpha was [0.7];
plt.text(0.7, 0.05, summary_text, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='bottom', bbox=dict(facecolor='white', alpha=0.9))

# Show the plot
plt.show()
