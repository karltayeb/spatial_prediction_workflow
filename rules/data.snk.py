rule download_ag:
    output:
        'output/ag3/manifest.tsv'
    run:
        shell("mkdir output/ag3")
        shell("gsutil cp gs://vo_agam_release/v3/manifest.tsv output/ag3/manifest.tsv")
        shell("mkdir output/ag3/metadata/")
        shell("gsutil -m rsync -r gs://vo_agam_release/v3/metadata/ output/ag3/metadata/")


rule get_popres_data:
    """
    just copy popres data to data repo
    """
    input:
        multiext('/project2/jnovembre/old_project/bpeter/eems_tib/subset/c1global1nfd', '.bed', '.bim', '.fam')
    output:
        multiext('data/popres/c1global1nfd', '.bed', '.bim', '.fam')
    run:
        source = '/project2/jnovembre/old_project/bpeter/eems_tib/subset/c1global1nfd'
        for i, o  in zip(input, output):
            print('copyin {} to {}'.format(i, o))
            shell('cp {} {}'.format(i, o))

rule popres_vcf:
    input:
        multiext("data/popres/c1global1nfd", ".bed", ".bim", ".fam")
    output:
        'data/popres/c1global1nfd.vcf'
    params:
        d = 'data/popres/c1global1nfd'
    conda:
        '../envs/plink.yaml'
    shell:
        "plink --bfile {params.d} --recode vcf --out {params.d}"

rule get_wolf_data:
    """
    just copy popres data to data repo
    """
    output:
        multiext('data/wolves/wolvesadmix', '.bed', '.bim', '.fam', '.coord')
    conda:
        '../envs/feems.yaml'
    script:
        '../scripts/fetch_wolf_data.py'

rule wolf_vcf:
    input:
        multiext("data/wolves/wolvesadmix", ".bed", ".bim", ".fam")
    output:
        'data/wolves/wolvesadmix.vcf'
    params:
        d = 'data/wolves/wolvesadmix',
    conda:
        '../envs/plink.yaml'
    shell:
        "plink --bfile {params.d} --recode vcf --dog --out {params.d}"


rule split_coords:
    input: 'data/{prefix}.coord'
    output: expand('data/{prefix}.{split}.coord', split=range(10), allow_missing=True)
    run:
        import numpy as np
        import pandas as pd
        from copy import deepcopy

        np.random.seed(0)
        meta = pd.read_csv(input[0], delim_whitespace=True, header=None)

        print(meta.shape)
        def mask_meta(meta, mask):
            meta2 = deepcopy(meta)
            meta2.iloc[mask, :2] = np.nan
            return meta2

        n = int(meta.shape[0] / 10)
        gen_mask = lambda: np.random.choice(meta.shape[0], n, replace=False)
        [mask_meta(meta, gen_mask()).to_csv(
            output[i], sep='\t', index=None) for i in range(len(output))];



