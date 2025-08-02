# --- Title and Description ---
# CME Simulation
# Based on Hassinger paper published in PNAS 2017 : https://www.pnas.org/doi/full/10.1073/pnas.1617705114
# The original code: https://github.com/Rangamani-Lab/hassinger-rangamani-2017/tree/master 
# Author: Anoosh Mahdavian
    # July 2025
    # Last Edit: [31 July 2025]
# --- Code Structure ---
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
