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

rule feems_initialize_titration:
    input:
        sp_graph_in = 'output/{prefix}/feems/grid_{gridsize}/sp_graph.pkl'
    output:
        sp_graph_out = 'output/{prefix}/titration/{n}/{idx}/feems/grid_{gridsize}/sp_graph.pkl'
    params:
        data_path = 'data/{prefix}',
        n = int('{n}')
    conda:
        '../envs/feems.yaml'
    script:
        '../scripts/feems_init_titration.py'

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
        coord='output/{prefix}/feems/grid_{gridsize}/leave_node_out/coord/{id}.coord'
    output:
        'output/{prefix}/feems/grid_{gridsize}/leave_node_out/{fit}_{predict}_{reg}/{id}_fit.pkl'
    conda:
        '../envs/feems.yaml'
    resources:
        mem=4000
    script:
        "../scripts/feems_fit.py"


rule feems_fit_full:
    input:
        sp_graph='output/{prefix}/feems/grid_{gridsize}/sp_graph.pkl'
    output:
        'output/{prefix}/feems/grid_{gridsize}/{fit}_{reg}/fit.pkl'
    conda:
        '../envs/feems.yaml'
    resources:
        mem=4000
    script:
        "../scripts/fit_feems_full.py"


rule run_popres_250_ibd_point_noreg:
    input:
        expand('output/popres/c1global1nfd/feems/grid_250/leave_node_out/ibd_point_noreg/{id}_fit.pkl', id=[str(i).zfill(3) for i in range(297)])

rule run_popres_250_feems_point_noreg:
    input:
        expand('output/popres/c1global1nfd/feems/grid_250/leave_node_out/feems_point_noreg/{id}_fit.pkl', id=[str(i).zfill(3) for i in range(297)])


rule run_popres_alpha1:
    input:
        expand('output/popres/c1global1nfd/feems/grid_250/leave_node_out/feems_point_alpha-0.1/{id}_fit.pkl', id=[str(i).zfill(3) for i in range(297)]),
        expand('output/popres/c1global1nfd/feems/grid_250/leave_node_out/ibd_point_alpha-0.1/{id}_fit.pkl', id=[str(i).zfill(3) for i in range(297)])


rule run_popres_alpha5:
    input:
        expand('output/popres/c1global1nfd/feems/grid_250/leave_node_out/feems_point_alpha-0.5/{id}_fit.pkl', id=[str(i).zfill(3) for i in range(297)]),
        expand('output/popres/c1global1nfd/feems/grid_250/leave_node_out/ibd_point_alpha-0.5/{id}_fit.pkl', id=[str(i).zfill(3) for i in range(297)])

# rule run_feems:
#     input:
#         directory('output/wolves/wolvesadmix/feems/grid_100/leave_node_out/ibd_point'),
#         directory('output/wolves/wolvesadmix/feems/grid_100/leave_node_out/feems_point'),
#         directory('output/popres/c1global1nfd/feems/grid_250/leave_node_out/ibd_point')
#         directory('output/popres/c1global1nfd/feems/grid_250/leave_node_out/feems_point')
#     resources:
#         time='4:0:0'


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




