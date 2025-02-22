import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def parametric_surface(u, v, shape):
    """
    Generate parametric surface based on user selection.
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
    else:
        raise ValueError("Unknown shape: Choose 'sphere', 'cone', 'paraboloid'")
    return x, y, z

def stereographic_projection(x, y, z):
    """
    Apply stereographic projection from the north pole (z = 1).
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        x_proj = x / (1 - z)
        y_proj = y / (1 - z)
    return x_proj, y_proj

def inverse_projection(x_proj, y_proj, shape):
    """
    Reconstruct 3D surface based on original shape equation.
    """
    r_proj = np.sqrt(x_proj**2 + y_proj**2)
    phi_proj = np.arctan2(y_proj, x_proj)
    
    if shape == "sphere":
        denom = 1 + r_proj**2
        x_recon = (2 * x_proj) / denom
        y_recon = (2 * y_proj) / denom
        z_recon = (1 - r_proj**2) / denom
    elif shape == "cone":
        x_recon = x_proj
        y_recon = y_proj
        z_recon = np.sqrt(x_proj**2 + y_proj**2)  # Matching cone equation
    elif shape == "paraboloid":
        x_recon = x_proj
        y_recon = y_proj
        z_recon = x_proj**2 + y_proj**2  # Matching paraboloid equation
    
    else:
        raise ValueError("Unknown shape: Choose 'sphere', 'cone', 'paraboloid', or 'ellipsoid'.")
    
    return x_recon, y_recon, z_recon

# Select shape
shape_type = "cone"  # Change this to test different shapes

# Generate a parametric surface
u_res, v_res = 190, 100  # Increased resolution
u = np.linspace(0, np.pi, u_res) if shape_type == "sphere" else np.linspace(0, 1, u_res)
v = np.linspace(0, 2 * np.pi, v_res)
u, v = np.meshgrid(u, v)

x, y, z = parametric_surface(u, v, shape_type)

# Apply stereographic projection
x_proj, y_proj = stereographic_projection(x, y, z)

# Reconstruct the surface using inverse projection
x_recon, y_recon, z_recon = inverse_projection(x_proj, y_proj, shape_type)

# Explicitly close the grid by appending the first row to the end
x_recon = np.vstack([x_recon, x_recon[0, :]])
y_recon = np.vstack([y_recon, y_recon[0, :]])
z_recon = np.vstack([z_recon, z_recon[0, :]])

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

# Choose between coarse surface grid or wireframe
visualization_mode = "coarse_grid"  # Change to "coarse_grid" for coarse surface grid

if visualization_mode == "coarse_grid":
    # Coarse surface grid
    ax3.plot_surface(x_recon, y_recon, z_recon, color='red', edgecolor='black', alpha=0.3, rstride=5, cstride=5)
elif visualization_mode == "wireframe":
    # Wireframe
    ax3.plot_wireframe(x_recon, y_recon, z_recon, color='red', rstride=5, cstride=5)
else:
    raise ValueError("Unknown visualization mode: Choose 'coarse_grid' or 'wireframe'")

ax3.set_title(f"Reconstructed 3D {shape_type.capitalize()}")
ax3.set_xlabel("X")
ax3.set_ylabel("Y")
ax3.set_zlabel("Z")

plt.show()
