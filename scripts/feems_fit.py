import pickle
from feems.spatial_prediction import predict_held_out_nodes
import pandas as pd
import numpy as np

# check valid fit wildcard
if snakemake.wildcards.fit == 'ibd':
    fit = False
elif snakemake.wildcards.fit == 'feems':
    fit = True
else:
    assert(False)


def regularize_frequencies(self, alpha=0):
    """
    update attributes frequencies and S in self
    compute weighted average of global freuqencies
    and and observed node frequencies
    """
    alpha = 0.5

    n = self.n_samples_per_obs_node_permuted
    mu = self.mu
    scale = np.sqrt(mu * (1-mu))

    f = self.frequencies * scale
    f_reg = (1 - alpha / n)[:, None] * f + (alpha / n)[:, None] * mu * 2
    
    self.frequencies = f_reg / scale
    self.S = self.frequencies @ self.frequencies.T / self.n_snps

sp_graph = pickle.load(open(snakemake.input.sp_graph, 'rb'))
coord = pd.read_csv(snakemake.input.coord, sep='\t', header=None)

if 'alpha' in snakemake.wildcards.reg:
    alpha = float(snakemake.wildcards.reg.split('-')[-1])
    print('regularizing node frequencies: alpha={}'.format(alpha))
    regularize_frequencies(sp_graph, alpha)

results = predict_held_out_nodes(
        sp_graph, coord,
        predict_type=snakemake.wildcards.predict,
        fit_feems = fit
    )
pickle.dump(results, open(snakemake.output[0], 'wb'))