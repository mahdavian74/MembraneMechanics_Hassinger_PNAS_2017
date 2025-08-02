# Title and Description
Python Simulation of clathrin-mediated endocytosis (CME) based on the membrane mechanics model proposed in:
Hassinger et al., *"Design principles for robust vesiculation in clathrin-mediated endocytosis,"* PNAS, 2017  
https://www.pnas.org/doi/full/10.1073/pnas.1617705114
The original MATLAB code is available here:  
https://github.com/Rangamani-Lab/hassinger-rangamani-2017/tree/master

**Author:** Anoosh Mahdavian  
📅 August 2025 | ✏️ Last Edit: July 25, 2025

---

## Code Structure and Branches

This repository contains **two** key branches:

###  `main` branch - ```MembraneMechanics_Basic.py``` - the non-executable version  
This version contains only the essential components:

1. Physical parameter definitions  
2. Parametrization of arclength and curvature  
3. Definition of 6 nonlinear ODEs  
4. Boundary conditions (BCs)  
5. Initial guess for the solver  
6. Solving the BVP  

This structure is clean and general-purpose. It can be adapted for sweeping over various parameters such as `lambda0`, `C0`, coated area, or actin forces. It is **not a standalone executable** for all analyses but serves as a reusable foundation.


###  `master` branch – ```MembraneMechanics_Main.py``` - the executable version

The extended version includes:

- Loops over varying clathrin-coated areas  
- Automated parameter sweeps  
- Visualization of membrane shapes  
- Saving results as `.gif` animations  

See [`master/README.md`](./master/README.md) for full instructions on how to run this version.

---

## Reference Parameters

```python
R0 = 20                         # Reference radius of the membrane (nm)
kappa0_bare = 320               # Bending rigidity of bare membrane (pN·nm)
kappa0_coat = 2400              # Bending rigidity of coated membrane (pN·nm)
gamma = 20                      # Membrane surface tension (pN/nm)
C0 = 0.02                       # Spontaneous curvature of the coat (1/nm)
alpha_max = 100                 # Maximum coated area along arclength (dimensionless)
lambda0 = [2, 0.2, 0.02, 0.002] # Membrane tension values to sweep (pN/nm)
coating_range = (0.5, 12, 150)  # Coated region range: start, stop, and steps
