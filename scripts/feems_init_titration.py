import numpy as np
from sklearn.impute import SimpleImputer
from pandas_plink import read_plink
import pickle
from feems.utils import prepare_graph_inputs
from feems import SpatialGraph

sp_graph = pickle.load(open(snakemake.input.sp_graph_in, 'rb'))

# redo initialization with new genotype
n = sp_graph.genotypes.shape[1]
subset = np.random.choice(n, snakemake.params.n, replace=False)
sp_graph.genotypes = sp_graph.genotypes[:, subset]
if verbose_init:
    print('estimating allele frequencies...')
sp_graph._estimate_allele_frequencies()

if scale_snps:
    sp_graph.mu = sp_graph.frequencies.mean(axis=0) / 2
    sp_graph.frequencies = sp_graph.frequencies / np.sqrt(sp_graph.mu * (1 - sp_graph.mu))

# compute precision
sp_graph.comp_precision(s2=1)

if verbose_init:
    print('estimating sample covariance matrix...')
# estimate sample covariance matrix
sp_graph.S = sp_graph.frequencies @ sp_graph.frequencies.T / sp_graph.n_snps

pickle.dump(sp_graph, open(snakemake.output[0], 'wb'))