import pickle
from feems.spatial_graph import query_node_attributes
from copy import deepcopy
import pandas as pd
import numpy as np
import os

os.makedirs(snakemake.output[0], exist_ok=True)


def mask_meta(meta, mask):
    meta2 = deepcopy(meta)
    meta2.iloc[mask, :2] = np.nan
    return meta2

sp_graph = pickle.load(open(snakemake.input[0], 'rb'))
meta = pd.read_csv(snakemake.input[1], delim_whitespace=True, header=None)


sample_idx = query_node_attributes(sp_graph, 'sample_idx')
node2sample = {i: s for i, s in enumerate(sample_idx) if len(s) > 0}

nodes = np.random.permutation(list(node2sample.keys()))

nsplits = np.min([snakemake.params.nsplits, nodes.size])
node_splits = np.array_split(nodes, nsplits)

for i, node_split in enumerate(node_splits):
    mask = np.concatenate([node2sample.get(node) for node in node_split])
    output = '{}/{}.coord'.format(
        snakemake.output[0], str(i).zfill(3))
    mask_meta(meta, mask).to_csv(output, sep='\t', index=None, header=False)