import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

air_volume_ml = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
length_transformation_mm = np.array([0, 0.3, 0.6, 1.0, 1.3, 1.7, 1.9, 2.2, 2.4, 2.6, 2.9])

interpolator = PchipInterpolator(air_volume_ml, length_transformation_mm)

air_smooth = np.linspace(0, 100, 500)
length_smooth = interpolator(air_smooth)

plt.figure(figsize=(8, 5))

plt.scatter(
    air_volume_ml,
    length_transformation_mm,
    label="Measured data",
    zorder=3
)

plt.plot(
    air_smooth,
    length_smooth,
    label="Interpolated curve"
)

plt.xlabel("Injected air volume (mL)")
plt.ylabel("Length transformation (mm)")
plt.title("Actuator Length Transformation vs Injected Air Volume")

plt.xlim(0, 100)
plt.ylim(bottom=0)

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()