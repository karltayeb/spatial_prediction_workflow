import numpy as np
from sklearn.impute import SimpleImputer
from pandas_plink import read_plink
import pickle
from feems.utils import prepare_graph_inputs
from feems import SpatialGraph


data_path = snakemake.params.data_path
# read the genotype data and mean impute missing data
(bim, fam, G) = read_plink(snakemake.params.data_path)
imp = SimpleImputer(missing_values=np.nan, strategy="mean")
genotypes = imp.fit_transform((np.array(G)).T)

print("n_samples={}, n_snps={}".format(genotypes.shape[0], genotypes.shape[1]))


# setup graph
coord = np.loadtxt("{}.coord".format(data_path))  # sample coordinates
outer = np.loadtxt("{}.outer".format(data_path))  # outer coordinates
grid_path = snakemake.input.grid_path  # path to discrete global grid

# graph input files
print('preparing graph inputs...')
outer, edges, grid, _ = prepare_graph_inputs(coord=coord, 
                                             ggrid=grid_path,
                                             translated=True, 
                                             buffer=0,
                                             outer=outer)

print('initializing spatial graph')
sp_graph = SpatialGraph(genotypes, coord, grid, edges, scale_snps=True)
pickle.dump(sp_graph, open(snakemake.output[0], 'wb'))