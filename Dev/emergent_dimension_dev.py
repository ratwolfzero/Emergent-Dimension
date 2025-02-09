import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def parametric_surface(u, v, shape):
    """
    Generate parametric surface based on user selection.
    
    Available shapes: 'sphere', 'cone', 'paraboloid', 'ellipsoid'
    """
    if shape == "sphere":
        x = np.sin(u) * np.cos(v)
        y = np.sin(u) * np.sin(v)
        z = np.cos(u)

    elif shape == "cone":
        k = 1  # Cone slope
        r = u
        x = r * np.cos(v)
        y = r * np.sin(v)
        z = k * r

    elif shape == "paraboloid":
        r = u
        x = r * np.cos(v)
        y = r * np.sin(v)
        z = r ** 2  # Parabolic height

    elif shape == "ellipsoid":
        a, b, c = 1, 1, 2  # Ellipsoid axes
        x = a * np.sin(u) * np.cos(v)
        y = b * np.sin(u) * np.sin(v)
        z = c * np.cos(u)

    else:
        raise ValueError("Unknown shape: Choose 'sphere', 'cone', 'paraboloid', or 'ellipsoid'.")

    return x, y, z

def stereographic_projection(x, y, z):
    """
    Apply stereographic projection from the north pole (z = 1).
    """
    x_proj = x / (1 - z)
    y_proj = y / (1 - z)
    return x_proj, y_proj

def inverse_projection(x_proj, y_proj, shape):
    """
    Reconstruct 3D surface based on original shape equation.
    """
    if shape == "sphere":
        x_recon = (2 * x_proj) / (1 + x_proj**2 + y_proj**2)
        y_recon = (2 * y_proj) / (1 + x_proj**2 + y_proj**2)
        z_recon = (1 - x_proj**2 - y_proj**2) / (1 + x_proj**2 + y_proj**2)

    elif shape == "cone":
        r_recon = np.sqrt(x_proj**2 + y_proj**2)
        phi_recon = np.arctan2(y_proj, x_proj)
        k = 1  # Same parameter as in parametric_surface()
        x_recon = r_recon * np.cos(phi_recon)
        y_recon = r_recon * np.sin(phi_recon)
        z_recon = k * r_recon

    elif shape == "paraboloid":
        r_recon = np.sqrt(x_proj**2 + y_proj**2)
        phi_recon = np.arctan2(y_proj, x_proj)
        x_recon = r_recon * np.cos(phi_recon)
        y_recon = r_recon * np.sin(phi_recon)
        z_recon = r_recon ** 2  # Match paraboloid equation

    elif shape == "ellipsoid":
        a, b, c = 1, 1, 2  # Ellipsoid axes
        r_recon = np.sqrt(x_proj**2 + y_proj**2)
        phi_recon = np.arctan2(y_proj, x_proj)
        x_recon = a * r_recon * np.cos(phi_recon)
        y_recon = b * r_recon * np.sin(phi_recon)
        z_recon = (1 - x_proj**2 - y_proj**2) / (1 + x_proj**2 + y_proj**2) * c

    else:
        raise ValueError("Unknown shape: Choose 'sphere', 'cone', 'paraboloid', or 'ellipsoid'.")

    return x_recon, y_recon, z_recon

# Select shape: 'sphere', 'cone', 'paraboloid', or 'ellipsoid'
shape_type = "ellipsoid"  # Change this to test different shapes

# Generate a parametric surface
u = np.linspace(0, np.pi, 30) if shape_type == "sphere" else np.linspace(0, 1, 30)
v = np.linspace(0, 2 * np.pi, 60)
u, v = np.meshgrid(u, v)

x, y, z = parametric_surface(u, v, shape_type)

# Apply stereographic projection
x_proj, y_proj = stereographic_projection(x, y, z)

# Reconstruct the surface using inverse projection
x_recon, y_recon, z_recon = inverse_projection(x_proj, y_proj, shape_type)

# Create figure with 3 subplots
fig = plt.figure(figsize=(18, 6))

# --- Original 3D Surface ---
ax1 = fig.add_subplot(131, projection='3d')
ax1.plot_surface(x, y, z, color='cyan', edgecolor='black', alpha=0.3)
ax1.set_title(f"Original 3D {shape_type.capitalize()}")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")

# --- 2D Projection ---
ax2 = fig.add_subplot(132)
ax2.scatter(x_proj, y_proj, s=1, color='blue')
ax2.set_title("2D Projection (Holographic Encoding)")
ax2.set_xlabel("X'")
ax2.set_ylabel("Y'")
ax2.set_xlim([-5, 5])
ax2.set_ylim([-5, 5])
ax2.set_aspect('equal')

# --- Reconstructed 3D Surface ---
ax3 = fig.add_subplot(133, projection='3d')
ax3.scatter(x_recon, y_recon, z_recon, s=1, color='red')
ax3.set_title(f"Reconstructed 3D {shape_type.capitalize()}")
ax3.set_xlabel("X")
ax3.set_ylabel("Y")
ax3.set_zlabel("Z")

plt.show()
