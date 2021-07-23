import pickle
import numpy as np
import pandas as pd
from copy import deepcopy

def regularize_frequencies(self, alpha):
    """
    update attributes frequencies and S in self
    compute weighted average of global freuqencies
    and and observed node frequencies
    """
    self.factor = None
    sp_graph = deepcopy(self)

    n = self.n_samples_per_obs_node_permuted
    mu = self.mu
    scale = np.sqrt(mu * (1-mu))

    f = self.frequencies * scale
    f_reg = (1 - alpha / n)[:, None] * f + (alpha / n)[:, None] * mu * 2
    
    sp_graph.frequencies = f_reg / scale
    sp_graph.S = sp_graph.frequencies @ sp_graph.frequencies.T / sp_graph.n_snps

    return sp_graph

# check valid fit wildcard
if snakemake.wildcards.fit == 'ibd':
    fit = False
elif snakemake.wildcards.fit == 'feems':
    fit = True
else:
    assert(False)

sp_graph = pickle.load(open(snakemake.input.sp_graph, 'rb'))
sp_graph.factor = None

if 'alpha' in snakemake.wildcards.reg:
    alpha = float(snakemake.wildcards.reg.split('-')[-1])
    print('regularizing node frequencies: alpha={}'.format(alpha))
    sp_graph = regularize_frequencies(sp_graph, alpha)

sp_graph.fit_null_model()
sp_graph.fit(lamb=2.0)
sp_graph.factor = None
pickle.dump(sp_graph, open(snakemake.output[0], 'wb'))
