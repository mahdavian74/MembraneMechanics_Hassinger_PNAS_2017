# %%
# --- Title and Description ---

# Membrane mechanics simulation
# Based on MemberaneMechanics_Hassinger_PNAS_2017: https://www.pnas.org/doi/full/10.1073/pnas.1617705114
#The original code could be found on Rangamani Lab github: https://github.com/Rangamani-Lab/hassinger-rangamani-2017/tree/master 

# Author: Anoosh mahdavian
# July 2025
# Last Edit: [31 July 2025]

# %%
# --- Code Structure ---
# The code contains:
    # - Imprting the needed packages
    # - Ploting style
    # - Getting tension and coating area from the user
    # - 1. The physical parameter determination, 
    # - 2. The parametrization of arch length and area of curvature 
    # - 3. The set of 6 ODEs to be solved
    # - 4. The BCs
    # - 5. The initial Guess
    # - 6. The solver
    # - 7. Visualization
    # - Sweep values over the arguments
    # - Save the animation 

# --- Reference Parameters ---
# R0 = 20                                                 
# kappa0_bare = 320
# kappa0_coat = 2400                                      
# gamma = 20
# C0 = 0.02  
# alpha_max = 100
# lamda0= [2, 0.2, 0.02, 0.002]
# coating_range = (1,12,100)     

# %%
# --- Imports and Setup ---

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp
from numpy import tanh, cos, sin
import os
import matplotlib
matplotlib.use("Agg")
from matplotlib.animation import FuncAnimation, PillowWriter
import argparse

# Plot style
plt.style.use('classic')  

# --- Command-line ---
parser = argparse.ArgumentParser(description="Membrane animation sweep")

parser.add_argument('--lambdas', type=float, nargs='+', default = [0.02],
                    help='List of lambda values to sweep (e.g., 0.02 0.002)')
parser.add_argument('--alpha_start', type=float, default=1.0,
                    help='Start of alpha range')
parser.add_argument('--alpha_end', type=float, default=12.0,
                    help='End of alpha range')
parser.add_argument('--n_alpha', type=int, default=100,
                    help='Number of alpha values in sweep')

args = parser.parse_args()

# %%
# --- 1.  Reference Values for Physical and Model Parameters ---

# Memberane 
R0 = 20                                                 # nm, reference length
kappa0 = 320                                            # pN.nm, reference bending modulus
gamma = 20                                              # Sharpness of coat/force transition

# Coat properties
C0 = 0.02                                               # nm^-1, spontaneous curvature in coated region
c0_nd = C0 * R0                                         # dimensionless spontaneous curvature

# Coat area range
alpha_max = 100                                         # matches disk radius R = 400 nm

# Bending modulus 
kappa_coat = 2400                                       # pN.nm
kappa_bare = 320                                        # pN.nm
kappa_coat_nd = kappa_coat / kappa0
kappa_bare_nd = kappa_bare / kappa0

# Gaussian modulus 
kappaG_coat_nd = 0
kappaG_bare_nd = 0

# Tension
def set_tension(lambda0_val):
    global lambda0, lambda0_nd
    lambda0 = lambda0_val                                # pN.nm^-1
    lambda0_nd = lambda0 * R0**2 / kappa0

# Force 
f0 = 0                                                   # pN
def define_force_region(alpha_end_val):
    global alpha_end, alpha_in, alpha_out, f0_nd
    alpha_end = alpha_end_val
    alpha_in = alpha_end
    alpha_out = alpha_in + 3
    force_area = 2 * np.pi * R0**2 * (alpha_out - alpha_in)
    f0_nd = (f0 / force_area) * (R0**3 / kappa0)
# Pressure
p0_nd = 0                                                # dimensionless pressure/but the pressure unit in pN/nm^2

# %%
# --- 2. Coat and Force Profile Functions (One-Sided for Half-Membrane) ---

# --- Smooth coat profile: active near the tip, decays toward edge (alpha_start ≡ a0) ---
def s(alpha_nd):
    return 0.5 * (1 - np.tanh(gamma * (alpha_nd - alpha_end)))

def ds(alpha_nd):
    return 0.5 * gamma * (np.tanh(gamma * (alpha_nd - alpha_end))**2 - 1)

def d2s(alpha_nd):
    tanh_term = np.tanh(gamma * (alpha_nd - alpha_end))
    return -gamma**2 * tanh_term * (1 - tanh_term**2)

# --- Spontaneous curvature profile and its derivative ---
def c_nd(alpha_nd):
    return c0_nd * s(alpha_nd)

def dc_nd(alpha_nd):
    return c0_nd * ds(alpha_nd)

# --- Bending modulus profile and its derivative ---
def kappa_nd(alpha_nd):
    return kappa_bare_nd + (kappa_coat_nd - kappa_bare_nd) * s(alpha_nd)

def dkappa_nd(alpha_nd):
    return (kappa_coat_nd - kappa_bare_nd) * ds(alpha_nd)

# --- Gaussian modulus profile and its derivatives ---
def kappaG_nd(alpha_nd):
    return kappaG_bare_nd + (kappaG_coat_nd - kappaG_bare_nd) * s(alpha_nd)

def dkappaG_nd(alpha_nd):
    return (kappaG_coat_nd - kappaG_bare_nd) * ds(alpha_nd)

def d2kappaG_nd(alpha_nd):
    return (kappaG_coat_nd - kappaG_bare_nd) * d2s(alpha_nd)

# --- Pressure profile (localized near tip) ---
def p_nd(alpha_nd):
    return p0_nd * s(alpha_nd)

# --- Actin force profile (one-sided inward pull from tip) ---
def force_profile(alpha_nd, alpha_in, alpha_out, gamma):
    """
    One-sided actin pulling force profile (decays from tip outward).
    Matches Hassinger MATLAB 'fbar' definition.
    """
    return (-f0_nd )* 0.5 * (np.tanh(gamma * (alpha_nd - alpha_in) - np.tanh(gamma * (alpha_nd - alpha_out))))

# %%
# --- 3. ODE System ---

def membrane_odes(alpha_nd, X):

    x, y, psi, h, l, lam = X

    # Property profiles
    c = c_nd(alpha_nd)
    dc = dc_nd(alpha_nd)
    k = kappa_nd(alpha_nd)
    dk = dkappa_nd(alpha_nd)
    kG = kappaG_nd(alpha_nd)
    dkG = dkappaG_nd(alpha_nd)
    d2kG = d2kappaG_nd(alpha_nd)
    
    # Optional: clip profiles to avoid instability
    x = x = np.clip(x, 1e-3, None)
    k = np.clip(k, 1e-3, None)
    dk = np.clip(dk, -10, 10)
    
    # Gaussian curvature
    g = h**2 - (h - sin(psi)/x)**2

    # Pressure
    p = p_nd(alpha_nd)    # could be 0 or localized, defined in profile section
    
    # External force
    fbar = force_profile(alpha_nd, alpha_in, alpha_out, gamma)
    f_dot_n = fbar * np.cos(psi)
    f_dot_as = fbar * np.sin(psi)

    # ODE system
    dx = cos(psi) / x
    dy = sin(psi) / x
    dpsi = 2*h/x - sin(psi)/x**2
    dh = l/ x**2 + dc - (dk / k) * (h - c) 

    dl = (
        p / k + f_dot_n / k
        + 2*h*((h - c)**2 + lam / k)
        - 2*(h - c)*(h**2 + (h - sin(psi)/x)**2)
        - (dk / k)*l
        - (x*d2kG / k) * sin(psi)
        - (dkG / k) * cos(psi) * (2*h - sin(psi)/x)
    )

    dlam = -dk*(h - c)**2 + 2*k*(h - c)*dc - dkG*g - f_dot_as / x
 
    return np.vstack([dx, dy, dpsi, dh, dl, dlam])
    
# %%
# --- 4. Boundary Conditions ---

def membrane_bc(X0, X1):
    x0, y0, psi0, h0, l0, lam0 = X0
    x1, y1, psi1, h1, l1, lam1 = X1

    return np.array([
        x0 - 1e-4,         # x(0) = ds, for not being zero
        psi0,              # psi(0) = 0
        l0,                # l(0) = 0
        y1,                # y(alpha_max) = 0
        psi1,              # psi(alpha_max) = 0
        lam1 - lambda0_nd  # lambda(alpha_max) = prescribed
    ])

# %%
# --- 5. Initial Guess ---
def initialize_guess(alpha_mesh):
    X_guess = np.zeros((6, alpha_mesh.size))
    X_guess[0] = alpha_mesh + 1e-4  # x starts near 0
    X_guess[5] = lambda0_nd         # initialize lambda
    return X_guess
# --- 6. Generating Mesh ---
def generate_mesh(alpha_end_val, mesh_size):
    mesh1 = np.linspace(1e-4, alpha_end_val, mesh_size, endpoint=False)
    mesh2 = np.linspace(alpha_end_val, alpha_end_val + 3, mesh_size, endpoint=False)
    mesh3 = np.geomspace(alpha_end_val + 3, alpha_max, mesh_size // 10)
    return np.unique(np.concatenate([mesh1, mesh2, mesh3]))

# --- 7. Solve the BVP ---
def solve_membrane(alpha_mesh, X_guess):
    sol = solve_bvp(
        fun=membrane_odes,
        bc=membrane_bc,
        x=alpha_mesh,
        y=X_guess,
        tol=1e-3,
        max_nodes=200000,
        verbose=2
    )
    return sol

# %%
# --- 7. Visualization ---
def create_animation(lambda_val, alpha_range, filename, mesh_size=10000):
    """
    Creates an animation of membrane deformation over varying coat sizes (alpha_end),
    using continuation to improve convergence, and skipping failed solutions.
    """
    set_tension(lambda_val)
    fig, ax = plt.subplots(figsize=(6, 6))
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(-200, 200)
    ax.set_ylim(-300, 100)
    ax.set_xlabel("r (nm)")
    ax.set_ylabel("z (nm)")
    ax.grid(True)
    ax.set_aspect('equal')

    successful_frames = []
    alpha_successful = []
    prev_sol = None  # For continuation

    for alpha_val in alpha_range:
        define_force_region(alpha_val)
        alpha_mesh = generate_mesh(alpha_val, mesh_size=mesh_size)

        # Use continuation guess if available
        if prev_sol is None:
            X_guess = initialize_guess(alpha_mesh)
        else:
            X_guess = prev_sol.sol(alpha_mesh)

        sol = solve_membrane(alpha_mesh, X_guess)

        if sol.success:
            prev_sol = sol
            x = sol.y[0] * R0
            y = sol.y[1] * R0
            x_full = np.concatenate([-x[::-1], x])
            y_full = np.concatenate([y[::-1], y])
            successful_frames.append((x_full, y_full, alpha_val))
            alpha_successful.append(alpha_val)
        else:
            print(f" Solver failed for alpha_end = {alpha_val:.2f}")

    print(f" {len(successful_frames)} successful frames out of {len(alpha_range)}")

    def init():
        line.set_data([], [])
        return line,

    def update(i):
        x_full, y_full, alpha_val = successful_frames[i]
        ax.clear()
        ax.set_xlim(-200, 200)
        ax.set_ylim(-300, 100)
        ax.set_xlabel("r (nm)")
        ax.set_ylabel("z (nm)")
        ax.set_aspect("equal")
        ax.grid(True)

        # Title
        ax.set_title(
            f"$\\lambda_0 = {lambda_val:.3f}\\ \\mathrm{{pN/nm}}"
            f" \\quad | \\quad \\alpha_{{\\mathrm{{coated}}}} = {alpha_val:.2f}"
            f" \\quad | \\quad \\mathrm{{A}}_{{\\mathrm{{coated}}}} = {alpha_val * 2 * np.pi * R0**2:.0f}\\ \\mathrm{{nm^2}}$",
            fontsize=12
        )

        # Define coated region limit from alpha
        x_coated = np.sqrt(2 * alpha_val) * R0
        x_full, y_full = successful_frames[i]

        # Find left and right indices where coating ends
        left_coated_end = np.searchsorted(x_full, -x_coated)
        right_coated_end = np.searchsorted(x_full, x_coated)

        # Plot bare left
        ax.plot(x_full[:left_coated_end], y_full[:left_coated_end], color="goldenrod", lw=2)
        # Plot coated region
        ax.plot(x_full[left_coated_end:right_coated_end], y_full[left_coated_end:right_coated_end], color="blue", lw=2)
        # Plot bare right
        ax.plot(x_full[right_coated_end:], y_full[right_coated_end:], color="goldenrod", lw=2)


        return line,

    ani = FuncAnimation(
        fig, update, frames=len(successful_frames),
        init_func=init, blit=True, repeat=False, interval=800
    )
    ani.save(filename, writer='pillow', fps=8)
    plt.close(fig)

# Sweep values; Use the arguments
lambda_list = args.lambdas
alpha_range = np.linspace(args.alpha_start, args.alpha_end, args.n_alpha)

# Save animations
os.makedirs("animations", exist_ok=True)
for lam in lambda_list:
    filename = f"animations/membrane_animation_lambda{lam}.gif"
    print(f"Generating: {filename}")
    create_animation(lambda_val=lam, alpha_range=alpha_range, filename=filename)




   