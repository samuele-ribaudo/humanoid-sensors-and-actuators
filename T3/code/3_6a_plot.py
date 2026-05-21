import numpy as np
import matplotlib.pyplot as plt

# 1. Define your experimental data vectors (Replace with your actual coordinates)
# Index corresponds to: [0ml, 10ml, 20ml, 30ml]
k = np.array([0, 5, 10, 15, 20, 25, 30])  # Removed air volume in mL

ax = np.array([0, 0, 0, 0, 0, 0, 0])  # Point A (fixed near base)
ay = np.array([0, 0, 0, 0, 0, 0, 0])

bx = np.array([6.4, 6.4, 6.3, 5.9, 3.5, 2.3, 2])  # Point B (moving midpoint)
by = np.array([0, 0.1, 0.2, 2, 4.8, 4.1, 4])

cx = np.array([13, 13, 12.7, 8.6, -1.6, -2, -1.9])  # Point C (moving tip)
cy = np.array([0.8, 1, 2.5, 7.9, 5.7, 1.5, 1.3])

# 2. Calculate coordinates components for the formula
x1, y1 = ax, ay
x2, y2 = bx, by
x3, y3 = cx, cy

# Common analytical determinants
D = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

# Avoid division by zero for the collinear/straight line case (0ml)
# We will calculate where D is non-zero
valid = D != 0

x0 = np.zeros_like(k, dtype=float)
y0 = np.zeros_like(k, dtype=float)
R = np.zeros_like(k, dtype=float)
curvature = np.zeros_like(k, dtype=float)

# Calculate Center (x0, y0)
x0[valid] = ((x1[valid]**2 + y1[valid]**2) * (y2[valid] - y3[valid]) +
             (x2[valid]**2 + y2[valid]**2) * (y3[valid] - y1[valid]) +
             (x3[valid]**2 + y3[valid]**2) * (y1[valid] - y2[valid])) / D[valid]

y0[valid] = ((x1[valid]**2 + y1[valid]**2) * (x3[valid] - x2[valid]) +
             (x2[valid]**2 + y2[valid]**2) * (x1[valid] - x3[valid]) +
             (x3[valid]**2 + y3[valid]**2) * (x2[valid] - x1[valid])) / D[valid]

# Calculate Radius R and Curvature (1/R)
R[valid] = np.sqrt((x1[valid] - x0[valid])**2 + (y1[valid] - y0[valid])**2)
curvature[valid] = 1.0 / R[valid]

# For the 0mL case where it's straight: R is infinity, curvature is 0
R[~valid] = np.inf
curvature[~valid] = 0.0

# 3. Plotting Curvature vs Removed Air Volume
plt.figure(figsize=(8, 5))
plt.plot(k, curvature, marker='o', linestyle='-', color='b', linewidth=2, label='Measured Curvature')

plt.title('Actuator Curvature vs. Removed Air Volume', fontsize=14)
plt.xlabel('Removed Air Volume (mL)', fontsize=12)
plt.ylabel('Curvature 1/R ($cm^{-1}$)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(k)
plt.legend()

# Show the plot
plt.show()

# Print calculated values to check console output
for i in range(len(k)):
    print(f"Volume: {k[i]} mL | Radius: {R[i]:.2f} mm | Curvature: {curvature[i]:.4f} mm^-1")