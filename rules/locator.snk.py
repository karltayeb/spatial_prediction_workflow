import pickle

node2sample = pickle.load(open('/Users/karltayeb/Research/spatial_prediction/feems/feems/data/node2sample.pkl', 'rb'))
observed_nodes = [k for k in node2sample if len(node2sample[k]) > 0]

rule locator_all:
    input:
        expand('output/wolves/locator/wolvesadmix_{node}/locator_predlocs.txt', node=observed_nodes)
    output:
        'output/wolves/locator/prediction.txt'
    shell:
        "awk FNR!=1 {input} > {output}"

rule run_locator:
    input:
        vcf='data/{prefix}.vcf',
        loc='data/{prefix}.coord'
    output:
        directory('output/wolves/locator/wolvesadmix_{node}')
    params:
        out = 'output/wolves/locator/wolvesadmix_{node}/locator'
    conda:
        '../envs/locator.yaml'
    shell:
        "mkdir -p {params.out} \n"
        "python /Users/karltayeb/Research/spatial_prediction/locator/scripts/locator.py --vcf {input.vcf} --sample_data {input.loc} --out {params.out}"