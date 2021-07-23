import pickle
import pandas as pd
import numpy as np
from copy import deepcopy

from feems.objective import Objective, comp_mats
from feems.spatial_graph import query_node_attributes
from feems.cross_validation import train_test_split
from feems.spatial_prediction import *


# check valid fit wildcard
if snakemake.wildcards.fit == 'ibd':
    fit = False
elif snakemake.wildcards.fit == 'feems':
    fit = True
else:
    assert(False)

predict_type = snakemake.wildcards.predict
fit_feems = fit

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

sp_graph = pickle.load(open(snakemake.input.sp_graph, 'rb'))
coord = pd.read_csv(snakemake.input.coord, sep='\t', header=None)

sample_idx = query_node_attributes(sp_graph, 'sample_idx')
permuted_idx = query_node_attributes(sp_graph, "permuted_idx")
sp_graph.fit_null_model()

# deepcopy doesn't like sp_graph.factor...
sp_graph.factor = None

# remove test demes from training
n = sp_graph.sample_pos.shape[0]
split = ~np.isnan(coord.iloc[:, 0])
sp_graph_train, sp_graph_test = train_test_split(sp_graph, split)

if 'alpha' in snakemake.wildcards.reg:
    alpha = float(snakemake.wildcards.reg.split('-')[-1])
    print('regularizing node frequencies: alpha={}'.format(alpha))
    sp_graph_train = regularize_frequencies(sp_graph_train, alpha)

test_sample_idx = query_node_attributes(sp_graph_test, 'sample_idx')
test_node2sample = {i: test_sample_idx[i]
    for i in range(len(test_sample_idx))
    if len(test_sample_idx[i]) > 0}
test_nodes = list(test_node2sample.keys())
print('fit feems w/o observations @ node: {}'.format(test_nodes))

if fit_feems:
    # TODO use fit_kwargs
    # sp_graph_train.fit(**fit_kwargs)
    sp_graph_train.fit(lamb=2., verbose=True)

print(sp_graph_train.w[:10])

# get genotypes of test deme
g = sp_graph.genotypes
g[~np.isclose(g, g.astype(int))] = np.nan

# predict
if predict_type == 'point':
    z, post_mean = predict_deme_point_mu(g, sp_graph_train)

# predict
if predict_type == 'trunc':
    z, post_mean = predict_deme_trunc_normal_mu(g, sp_graph_train)

results = {
    'post_assignment': z[~split],
    'w': sp_graph_train.w,
    'w0': sp_graph_train.w0,
    's2': sp_graph_train.s2,
    #'post_mean': post_mean, # compute posterior mean
    'map_coord': sp_graph.node_pos[permuted_idx][z.argmax(1)],
    'pred_idx': np.where(~split)[0],
    'test_nodes': test_nodes
}


# results = predict_held_out_nodes(
#         sp_graph, coord,
#         predict_type=snakemake.wildcards.predict,
#         fit_feems = fit
#     )
pickle.dump(results, open(snakemake.output[0], 'wb'))
