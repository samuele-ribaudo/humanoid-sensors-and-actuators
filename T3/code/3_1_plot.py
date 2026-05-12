import numpy as np
import matplotlib.pyplot as plt

air_volume_ml = np.array([100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0])
#length_transformation_mm = np.array([29, 26, 24 ,22, 19, 17, 13, 10, 6, 3, 0])
length_transformation_mm = np.array([0, -3, -5 ,-7, -10, -12, -16, -19, -23, -26, -29])

# Linearer Fit: y = m*x + b
coefficients = np.polyfit(air_volume_ml, length_transformation_mm, deg=1)
fit_function = np.poly1d(coefficients)

air_smooth = np.linspace(0, 100, 500)
length_fit = fit_function(air_smooth)

plt.figure(figsize=(8, 5))

plt.scatter(
    air_volume_ml,
    length_transformation_mm,
    label="Measured data",
    zorder=3
)

plt.plot(
    air_smooth,
    length_fit,
    label="Linear fit",
    linewidth=2
)

plt.xlabel("Injected air volume (mL)")
plt.ylabel("Length transformation (mm)")
plt.title("Actuator Length Transformation vs Injected Air Volume")

plt.xlim(100, 0)
plt.ylim(-30, 5)

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print(f"Fit equation: y = {coefficients[0]:.4f}x + {coefficients[1]:.4f}")