import pickle

# node2sample = pickle.load(open('/Users/karltayeb/Research/spatial_prediction/feems/feems/data/node2sample.pkl', 'rb'))
# observed_nodes = [k for k in node2sample if len(node2sample[k]) > 0]

rule prep_coord:
    """
    just copy popres data to data repo
    """
    input:
        'data/{prefix}.fam',
        'data/{prefix}_splits/{split}.coord'
    output: 'data/{prefix}_splits/{split}.locator.coord'

    run:
        import pandas as pd
        coord = pd.read_csv(input[1], index_col=False, header=None, sep='\s')
        fam = pd.read_csv(input[0], index_col=False, header=None, sep='\s')
        fam['sampleID']=fam.apply(lambda x:'%s_%s' % (x[0],x[1]),axis=1)
        meta = pd.concat([coord, fam['sampleID']], axis=1).iloc[:, :4]
        meta.columns = ['x', 'y', 'sampleID']
        meta.to_csv(output[0], sep='\t', index=None)

rule run_locator:
    input:
        vcf='data/{prefix}.vcf',
        loc='data/{prefix}_splits/{split}.locator.coord'
    output:
        directory('output/{prefix}/locator/splits/{split}')
    params:
        out = 'output/{prefix}/locator/splits/{split}'
    conda:
        '../envs/locator.yaml'
    shell:
        "mkdir -p {params.out} \n"
        "python3 {config[locator_path]} --vcf {input.vcf} --sample_data {input.loc} --out {params.out}"


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
        out = 'output/{prefix}/locator/splits/{split}'
    conda:
        '../envs/locator.yaml'
    shell:
        "mkdir -p {params.out} \n"
        "python3 {config[locator_path]} --vcf {input.vcf} --sample_data {input.loc} --out {params.out}"


rule run_locator_all:
    input:
        expand('output/wolves/wolvesadmix/locator/splits/{split}', split=range(10)),
        expand('output/popres/c1global1nfd/locator/splits/{split}', split=range(10))
        

