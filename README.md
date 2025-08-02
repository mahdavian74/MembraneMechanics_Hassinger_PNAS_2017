# '''MembraneMechanics_Main.py''' Code Structure
The '''MembraneMechanics_Main.py''' is the extended version that includes:
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

# Running the Code
to Run the code you can clone it, then usidng the command
python MembraneMechanics_Main.py --lambdas 0.02 --alpha_start 0.5 --alpha_end 12 --n_alpha 150
    --lambdas: A single value or list of membrane tension values (e.g., 0.02 or 0.2 0.02)

    --alpha_start, --alpha_end: Range of coated arclength values

    --n_alpha: Number of points to sweep across that range
     
     
If no arguments are provided, the script uses the following defaults:
    lambda0 = [2, 0.2, 0.02, 0.002]           # Membrane tensions (pN/nm)
    coating_range = (0.5, 12, 150)            # Coated arclength range and resolution

# Output
The coresponding results will save in ./anmations
     
