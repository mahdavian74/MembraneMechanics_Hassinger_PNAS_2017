# --- Title and Description ---
Simulation of clathrin-mediated endocytosis (CME) based on the membrane mechanics model proposed in: Hassinger et al., "Design principles for robust vesiculation in clathrin-mediated endocytosis," PNAS, 2017
Based on Hassinger paper published in PNAS 2017 : https://www.pnas.org/doi/full/10.1073/pnas.1617705114
The original code in MATLAB: https://github.com/Rangamani-Lab/hassinger-rangamani-2017/tree/master 
# Author: Anoosh Mahdavian
     July 2025
     Last Edit: [1 Aug 2025]
# --- Code Structure ---
     - Imprting the needed packages
     - Ploting style
     - Getting tension and coating area from the user
     - 1. The physical parameter determination, 
     - 2. The parametrization of arch length and area of curvature 
     - 3. The set of 6 ODEs to be solved
     - 4. The BCs
     - 5. The initial Guess
     - 6. The solver
     - 7. Visualization
     - Sweep values over the arguments
     - Save the animation 
# --- Reference Parameters ---
     R0 = 20                                                 
     kappa0_bare = 320
     kappa0_coat = 2400                                      
     gamma = 20
     C0 = 0.02  
     alpha_max = 100
     lamda0= [2, 0.2, 0.02, 0.002]
     coating_range = (1,12,100)
# --- Code Branches ---
     This package consists a basic form which is only the essential parts: 
         - 1. The physical parameter determination, 
         - 2. The parametrization of arch length and area of curvature 
         - 3. The set of 6 ODEs to be solved
         - 4. The BCs
         - 5. The initial Guess
         - 6. The solver   
    This structure is general and can be adapted for sweeping over various parameters (e.g., lambda0, C0, coated area, or actin forces). It is not a standalone executable for all analyses but rather a clean foundation for exploration.
    
    #Thre is a master branch also, which consists the modified version for loops over different coating areas of clatherin. Find the running commands of this branch in its corresponding Readme

Simulation of clathrin-mediated endocytosis (CME) based on the membrane mechanics model proposed in:

Hassinger et al., "Design principles for robust vesiculation in clathrin-mediated endocytosis," PNAS, 2017
