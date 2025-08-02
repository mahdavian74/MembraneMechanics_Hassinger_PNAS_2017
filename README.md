##  Code Structure of `MembraneMechanics_Main.py` 

`MembraneMechanics_Main.py` is the **extended version** of the `MembraneMechanics_Basic.py` that include
parameter sweeps and animation saving for different coated regions and membrane tensions. It main Parts are: 

- Importing required packages  
- Setting plot styles  
- Receiving user input for membrane tension and coated area range  
   1. Physical parameter definitions  
   2. Parametrization of arclength and curvature  
   3. Definition of 6 nonlinear ODEs  
   4. Boundary conditions (BCs)  
   5. Initial guess for the solver  
   6. Solving the BVP  
   7. Visualization of membrane shape  
- Sweeping values over input parameters  
- Saving results as animated GIFs  

---

## Running the Code
After cloning the repository, you can run the simulation using:
```bash
python MembraneMechanics_Main.py --lambdas 0.02 --alpha_start 0.5 --alpha_end 12 --n_alpha 150
```
- `--lambdas`: A single value or a list of membrane tensions (e.g., `0.02` or `[0.2, 0.02]`)  
- `--alpha_start`, `--alpha_end`: Start and end of coated area range  
- `--n_alpha`: Number of step points between `alpha_start` and `alpha_end`   


If no arguments are provided, the following defaults are used:

```python
lambda0 = [2, 0.2, 0.02, 0.002]         # Membrane tensions (pN/nm)
coating_range = (0.5, 12, 150)          # Coated arclength range and resolution
```
---
## Output
The resulting GIF animations will be saved in
./animations
