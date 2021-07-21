def extract_dataset(wildcards):
    ds = wildcards.prefix.split('/')[0]
    print(ds)
    return ds


def get_translated(wildcards):
    return config['translated'][extract_dataset(wildcards)]


rule feems_initialize_graph:
    input:
        multiext('data/{prefix}', '.bed', '.bim', '.fam', '.coord', '.outer'),
        grid_path = 'data/grids/grid_{gridsize}.shp'
    output:
        'output/{prefix}/feems/grid_{gridsize}/sp_graph.pkl'
    params:
        data_path = 'data/{prefix}',
        translated = get_translated
    conda:
        '../envs/feems.yaml'
    script:
        '../scripts/feems_init_sp_graph.py'

rule feems_leave_node_out_split:
    """
    create coord files that do not have locations for samples from each node
    """
    input:
        sp_graph='output/{prefix}/feems/grid_{gridsize}/sp_graph.pkl',
        coord='data/{prefix}.coord'
    output:
        directory('output/{prefix}/feems/grid_{gridsize}/leave_node_out/coord')
    params:
        nsplits = 1e6
    conda:
        '../envs/feems.yaml'
    script:
        "../scripts/feems_split_nodes.py"

rule feems_leave_node_out_fit:
    input:
        sp_graph='output/{prefix}/feems/grid_{gridsize}/sp_graph.pkl',
        coord_dir=directory('output/{prefix}/feems/grid_{gridsize}/leave_node_out/coord')
    output:
        directory('output/{prefix}/feems/grid_{gridsize}/leave_node_out/{fit}_{predict}')
    conda:
        '../envs/feems.yaml'
    script:
        "../scripts/feems_lno.py"


rule run_feems:
    input:
        directory('output/wolves/wolvesadmix/feems/grid_100/leave_node_out/ibd_point'),
        directory('output/wolves/wolvesadmix/feems/grid_100/leave_node_out/feems_point'),
        directory('output/popres/c1global1nfd/feems/grid_250/leave_node_out/ibd_point')
        directory('output/popres/c1global1nfd/feems/grid_250/leave_node_out/feems_point')
    resources:
        time='4:0:0'


rule feems_run_split_nodes:
    input:
        sp_graph='output/{prefix}/feems/grid_{gridsize}/sp_graph.pkl',
        coord='output/{prefix}/grid_{gridsize}/node_splits/grid_{gridsize}_split_{split}.coord'
    output:
        'output/{prefix}/feems/node_splits/feems_{fit}_{predict}_grid_{gridsize}_split_{split}.pkl'
    conda:
        '../envs/feems.yaml'
    script:
        "../scripts/feems_fit.py"




