import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate a 3D sphere
theta = np.linspace(0, np.pi, 30)
phi = np.linspace(0, 2 * np.pi, 60)
theta, phi = np.meshgrid(theta, phi)

# Convert spherical coordinates to Cartesian (3D)
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

# Stereographic Projection (3D -> 2D)
x_proj = x / (1 - z)
y_proj = y / (1 - z)

# Inverse Projection (2D -> 3D)
x_recon = (2 * x_proj) / (1 + x_proj**2 + y_proj**2)
y_recon = (2 * y_proj) / (1 + x_proj**2 + y_proj**2)
z_recon = (1 - x_proj**2 - y_proj**2) / (1 + x_proj**2 + y_proj**2)

# Create figure with 3 subplots
fig = plt.figure(figsize=(18, 6))

# --- Original 3D Sphere ---
ax1 = fig.add_subplot(131, projection='3d')
ax1.plot_surface(x, y, z, color='cyan', edgecolor='black', alpha=0.3)
ax1.set_title("Original 3D Sphere")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")

# --- 2D Stereographic Projection (Emergent Dimension Encoding) ---
ax2 = fig.add_subplot(132)
ax2.scatter(x_proj, y_proj, s=1, color='blue')
ax2.set_title("2D Projection (Holographic Encoding)")
ax2.set_xlabel("X'")
ax2.set_ylabel("Y'")
ax2.set_xlim([-5, 5])
ax2.set_ylim([-5, 5])
ax2.set_aspect('equal')

# --- Reconstructed 3D Sphere ---
ax3 = fig.add_subplot(133, projection='3d')
ax3.scatter(x_recon, y_recon, z_recon, s=1, color='red')
ax3.set_title("Reconstructed 3D Sphere")
ax3.set_xlabel("X")
ax3.set_ylabel("Y")
ax3.set_zlabel("Z")

plt.show()

