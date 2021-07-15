def extract_dataset(wildcards):
    ds = wildcards.prefix.split('/')[0]
    print(ds)
    return ds


def get_translated(wildcards):
    return config['translated'][extract_dataset(wildcards)]


rule feems_initialize_graph:
    input:
        multiext('data/{prefix}', '.bed', '.bim', '.fam', '.coord', '.outer'),
        grid_path = 'data/grids/grid_100.shp'
    output:
        'output/{prefix}/feems/init_sp_graph.pkl'
    params:
        data_path = 'data/{prefix}',
        translated = get_translated
    conda:
        '../envs/feems.yaml'
    script:
        '../scripts/feems_init_sp_graph.py'


rule feems_split_nodes:
    """
    create coord files that do not have locations for samples from same node
    """
    input:
        sp_graph='output/{prefix}/feems/init_sp_graph.pkl',
        coord='data/{prefix}.coord'
    output:
        expand('output/{prefix}/node_splits/{split}.coord', split=range(10), allow_missing=True)
    params:
        nsplits = length(output)
    conda:
        '../envs/feems.yaml'
    shell:
        "../scripts feems_split_coord.py"


rule run_feems_split:
    input:
        sp_graph='output/{prefix}/feems/init_sp_graph.pkl',
        coord='data/{prefix}_splits/{split}.locator.coord'
    output:
        'output/{prefix}/feems/splits/{split}.feems.pkl'
    conda:
        '../envs/feems.yaml'
    shell:
        "../scripts feems_fit.py"


rule prepare_feems:
    """
    prepare inputs for feems
    """
    input:
        multiext('data/{prefix}', 'bed', 'bim', 'fam', 'coord'),
    output:
        'output/wolves/feems/prep.pkl'
    params:
        prefix = 'data/{prefix}'
    output:
        'output/wolves/feems/prep.pkl'
    run:
        (bim, fam, G) = read_plink(prefix)
        imp = SimpleImputer(missing_values=np.nan, strategy="mean")
        genotypes = imp.fit_transform((np.array(G)).T)

        # setup graph
        coord = np.loadtxt("{}.coord".format(prefix))  # sample coordinates
        outer = np.loadtxt("{}.outer".format(prefix))  # outer coordinates
        grid_path = "data/wolves/grid_100.shp"  # path to discrete global grid

        # graph input files
        outer, edges, grid, _ = prepare_graph_inputs(coord=coord, 
                                                     ggrid=grid_path,
                                                     translated=True, 
                                                     buffer=0,
                                                     outer=outer)
        sp_graph = SpatialGraph(genotypes, coord, grid, edges, scale_snps=True)

        results = {
            'genotypes': genotypes,
            'coord': coord,
            'sp_graph': sp_graph
        }
        pickle.dump(results, open(output[0], 'wb'))

rule run_feems:
    input:
        '/Users/karltayeb/Research/spatial_prediction/feems/docsrc/notebooks/wolf_sp_graph.pkl'
    output:
        'output/wolves/feems/leave_node_out_fit_{fit}_{predict}.pkl'
    conda:
        '../envs/feems.yaml'
    script:
        "../scripts/feems_lno.py"


