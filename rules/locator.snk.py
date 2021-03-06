import pickle

# node2sample = pickle.load(open('/Users/karltayeb/Research/spatial_prediction/feems/feems/data/node2sample.pkl', 'rb'))
# observed_nodes = [k for k in node2sample if len(node2sample[k]) > 0]

rule prep_coord_for_locator:
    """
    just copy coords to locator output file,
    reformat coords for locator
    """
    input:
        fam='data/{prefix}.fam',
        coord_dir=directory('output/{prefix}/feems/grid_{gridsize}/leave_node_out/coord')
    output:
        directory('output/{prefix}/locator/grid_{gridsize}/leave_node_out/coord/')
    run:
        import pandas as pd
        import numpy as np
        import os
        from glob import glob
        import tqdm

        prefix = wildcards.prefix
        grid = wildcards.gridsize

        print('making directory...')
        os.makedirs(output[0], exist_ok=True)

        print('loading coords...')
        lno_coord_paths = np.sort(glob(input.coord_dir + '/*'))
        lno_coords = [pd.read_csv(f, sep='\t', header=None) for f in lno_coord_paths]

        fam = pd.read_csv(input.fam, index_col=False, header=None, sep='\s')

        for i in range(len(lno_coord_paths)):
            p = lno_coord_paths[i]
            p_out = 'output/{prefix}/locator/grid_{grid}/leave_node_out/coord'.format(prefix=prefix, grid=grid)
            p_out = '{}/{}'.format(p_out, p.split('/')[-1])
            fam['sampleID']=fam.apply(lambda x:'%s_%s' % (x[0],x[1]),axis=1)
            meta = pd.concat([lno_coords[i], fam['sampleID']], axis=1).iloc[:, :4]
            meta.columns = ['x', 'y', 'sampleID']

            print('saving to {}'.format(p_out))
            print(meta.head())
            meta.to_csv(p_out, sep='\t', index=None)

rule run_locator_leave_node_out:
    input:
        vcf='data/{prefix}.vcf',
        loc='output/{prefix}/locator/grid_{gridsize}/leave_node_out/coord/{id}.coord'
    output:
        'output/{prefix}/locator/grid_{gridsize}/leave_node_out/fit/{id}_predlocs.txt'
    params:
        outpath = lambda wildcard, output: output[0][:-len('_predlocs.txt')]
    conda:
        '../envs/locator_gpu.yaml'
    group:
        ''
    resources:
        partition='gpu2',
        gres='gpu:1',
        ntasks=1
    shell:
        "module load cuda/10.1 \n"
        #"mkdir -p {output[0]} \n"
        "python3 {config[locator_path]} --vcf {input.vcf} --sample_data {input.loc} --out {params.outpath} --keep_weights"


rule run_locator_popres_250:
    input:
        expand('output/popres/c1global1nfd/locator/grid_250/leave_node_out/fit/{id}_predlocs.txt', id=[str(i).zfill(3) for i in range(297)])

rule run_locator_wolves_100:
    input:
        expand('output/wolves/wolvesadmix/locator/grid_100/leave_node_out/fit/{id}_predlocs.txt', id=[str(i).zfill(3) for i in range(94)])
rule prep_coord_node_split:
    """
    just copy popres data to data repo
    """
    input:
        'data/{prefix}.fam',
        'output/{prefix}/node_splits/{split}.coord'
    output: 'output/{prefix}/node_splits/{split}.coord.locator'
    run:
        import pandas as pd
        coord = pd.read_csv(input[1], index_col=False, header=None, sep='\s')
        fam = pd.read_csv(input[0], index_col=False, header=None, sep='\s')
        fam['sampleID']=fam.apply(lambda x:'%s_%s' % (x[0],x[1]),axis=1)
        meta = pd.concat([coord, fam['sampleID']], axis=1).iloc[:, :4]
        meta.columns = ['x', 'y', 'sampleID']
        meta.to_csv(output[0], sep='\t', index=None)

rule run_locator_node_split:
    input:
        vcf='data/{prefix}.vcf',
        loc='output/{prefix}/node_splits/{split}.coord.locator'
    output:
        directory('output/{prefix}/locator/node_splits/{split}')
    params:
        out = 'output/{prefix}/locator/node_splits/{split}'
    conda:
        '../envs/locator.yaml'
    shell:
        "mkdir -p {params.out} \n"
        "python3 {config[locator_path]} --vcf {input.vcf} --sample_data {input.loc} --out {params.out} --keep_weights"


rule run_locator_all:
    input:
        expand('output/wolves/wolvesadmix/locator/splits/{split}', split=range(10)),
        expand('output/popres/c1global1nfd/locator/splits/{split}', split=range(10))


