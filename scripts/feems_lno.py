import pickle
from feems.spatial_prediction import leave_node_out_spatial_prediction

print('Leave one node out feems...')

# check valid fit wildcard
if snakemake.wildcards.fit == 'ibd':
    fit = False
elif snakemake.wildcards.fit == 'feems':
    fit = True
else:
    assert(False)

sp_graph = pickle.load(open(snakemake.input[0], 'rb'))
result = leave_node_out_spatial_prediction(
    sp_graph,
    predict_type=snakemake.wildcards.predict,
    fit_feems = fit
)
pickle.dump(result, open(snakemake.output[0], 'wb'))