import numpy as np
import matplotlib.pyplot as plt

k = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40])  # Removed air volume in mL
force = np.array([0.0, 0.0, 0.05, 0.1, 0.2, 0.5, 0.7, 1.0, 1.2]) # force measured

# 2. Plotting Force vs Removed Air Volume
plt.figure(figsize=(8, 5))
plt.plot(k, force, marker='o', linestyle='-', color='r', linewidth=2, label='Measured Force')

plt.title('Actuator Force Output vs. Removed Air Volume', fontsize=14)
plt.xlabel('Removed Air Volume (mL)', fontsize=12)
plt.ylabel('Force (N)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(k)
plt.legend()

# Show the plot
plt.show()

# Print calculated values to check console output
for i in range(len(k)):
    print(f"Volume: {k[i]} mL | Force: {force[i]:.2f} N")