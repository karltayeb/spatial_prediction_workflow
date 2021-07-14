import pickle

node2sample = pickle.load(open('/Users/karltayeb/Research/spatial_prediction/feems/feems/data/node2sample.pkl', 'rb'))
observed_nodes = [k for k in node2sample if len(node2sample[k]) > 0]

rule spasiba_all:
    input:
        expand('output/wolves/spasiba/wolvesadmix_{node}/spasiba_predlocs.txt', node=observed_nodes)
    output:
        'output/wolves/spasiba/prediction.txt'
    shell:
        "awk FNR!=1 {input} > {output}"

rule run_spasiba:
    input:
        vcf='/Users/karltayeb/Research/spatial_prediction/spasiba/data/wolves/wolvesadmix.vcf',
        loc='/Users/karltayeb/Research/spatial_prediction/spasiba/data/wolves/wolvesadmix_{node}.txt'
    output:
        directory('output/wolves/spasiba/wolvesadmix_{node}')
    params:
        out = 'output/wolves/spasiba/wolvesadmix_{node}/spasiba'
    shell:
        "mkdir -p {params.out} \n"
        "python /Users/karltayeb/Research/spatial_prediction/spasiba/scripts/spasiba.py --vcf {input.vcf} --sample_data {input.loc} --out {params.out}"