import pickle
from feems.spatial_prediction import predict_held_out_nodes
from glob import glob
import pandas as pd
from tqdm import tqdm
import os


os.makedirs(snakemake.output[0], exist_ok=True)
paths = glob(snakemake.input.coord_dir + '/*')

print('Leave one node out feems...')

# check valid fit wildcard
if snakemake.wildcards.fit == 'ibd':
    fit = False
elif snakemake.wildcards.fit == 'feems':
    fit = True
else:
    assert(False)

for p in tqdm(paths):
    sp_graph = pickle.load(open(snakemake.input.sp_graph, 'rb'))
    coord = pd.read_csv(p, sep='\t', header=None)

    results = predict_held_out_nodes(
            sp_graph, coord,
            predict_type=snakemake.wildcards.predict,
            fit_feems = fit
        )

    split_id = p.split('/')[-1].split('.')[0]
    save_path = '{}/{}.fit.pkl'.format(snakemake.output[0], split_id)
    pickle.dump(results, open(save_path, 'wb'))