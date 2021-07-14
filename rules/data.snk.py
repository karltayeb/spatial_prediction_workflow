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








