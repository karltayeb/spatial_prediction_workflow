rule prepare_feems:
    """
    prepare inputs for feems
    """
    input:
        multiext('data/wolves/wolvesadmix', 'bed', 'bim', 'fam', 'coord'),
    output:
        'output/wolves/feems/prep.pkl'
    params:
        prefix = 'data/wolves/wolvesadmix'
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