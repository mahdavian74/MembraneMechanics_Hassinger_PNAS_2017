# --- Title and Description ---
Simulation of clathrin-mediated endocytosis (CME) based on the membrane mechanics model proposed in: Hassinger et al., "Design principles for robust vesiculation in clathrin-mediated endocytosis," PNAS, 2017

Based on Hassinger paper published in PNAS 2017 : https://www.pnas.org/doi/full/10.1073/pnas.1617705114

The original code in MATLAB: https://github.com/Rangamani-Lab/hassinger-rangamani-2017/tree/master 

Author: Anoosh Mahdavian
Aug 2025; Last Edit: [25 July 2025]
# --- Code Structure and Branches ---
     This package consists a basic form which is only the essential parts: 
         - 1. The physical parameter determination, 
         - 2. The parametrization of arch length and area of curvature 
         - 3. The set of 6 ODEs to be solved
         - 4. The BCs
         - 5. The initial Guess
         - 6. The solver   
    This structure is general and can be adapted for sweeping over various parameters (e.g., lambda0, C0, coated area, or actin forces). It is not a standalone executable for all analyses but rather a clean foundation for exploration.
    
    An extended version that includes Loops over varying clathrin-coated areas, automated parameter sweeps, GIF animation saving, and batch visualization of membrane shapes is in the master branch. See the master/README.md file for specific instructions on how to run this version.
# --- Reference Parameters ---
    R0 = 20                         # Reference radius of the membrane (nm)
    kappa0_bare = 320               # Bending rigidity of bare membrane (pN·nm)
    kappa0_coat = 2400              # Bending rigidity of coated membrane (pN·nm)
    gamma = 20                      # Membrane surface tension (pN/nm)
    C0 = 0.02                       # Spontaneous curvature of the coat (1/nm)
    alpha_max = 100                 # Maximum coated area along arclength (dimensionless, in arclength units) 
    lamda0 = [2, 0.2, 0.02, 0.002]  # Membrane tension values to sweep over (pN/nm)
    coating_range = (0.5, 12, 150)  # Coated region range: start, stop, and number of samples (dimensionless arclength units)


