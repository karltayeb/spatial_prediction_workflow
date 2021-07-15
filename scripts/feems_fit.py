import pickle
from feems.spatial_prediction import predict_held_out_nodes

# check valid fit wildcard
if snakemake.wildcards.fit == 'ibd':
    fit = False
elif snakemake.wildcards.fit == 'feems':
    fit = True
else:
    assert(False)

sp_graph = pickle.load(open(snakemake.input.sp_graph, 'rb'))
coord = pd.read_csv(snakemake.input.coord, sep='\t', header=None)

results = predict_held_out_nodes(
        sp_graph, coord,
        predict_type=snakemake.wildcards.predict,
        fit_feems = fit
    )
pickle.dump(snakemake.output[0], 'wb')