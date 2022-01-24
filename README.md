# spatial_prediction_workflow

Snakemake workflow for running FEEMS, and comparing it to other methods (IBD-FEEMS which is FEEMS null model, Locator a neural network based approach)
Attempted to also include SPASIBA in the pipeline but could not get it working.

Check out `notebooks/peter2020.ipynb` to see the comparative performance of FEEMS, IBD-FEEMS, and Locator on Peter 2020 Data
Run `notebooks/peter2020_assignment_uncertainty.ipynb` for interactive plots to explore uncertainty in FEEMS assignments

Check out `notebooks/wolves.ipynb` to see the comparative performance of FEEMS, IBD-FEEMS, and Locator on wolf migration example
Run `notebooks/wolves_assignment_uncertainty.ipynb` for interactive plots to explore uncertainty in FEEMS assignments

Trying to identify scenarios where FEEMS clearly outperforms IBD-FEEMS. You can start at `notebooks/feems_vs_ibd_anisotropic_sim.ipynb`. In this simulation both models work comparably, but you can use this as a starting point for making new simulations that challenge one/both methods. 
