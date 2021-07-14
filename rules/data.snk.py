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
        multiext('/project2/jnovembre/old_project/bpeter/eems_tib/subset/c1global1nfd', '.bim', '.bam', '.fam')
    output:
        multiext('data/popres/global/c1global1nfd', '.bim', '.bam', '.fam')
    run:
        source = '/project2/jnovembre/old_project/bpeter/eems_tib/subset/c1global1nfd'
        for i, o  in zip(input, output):
            shell('mv {} {}'.format(i, o))


rule prep_vcf:
    input:
        multiext("data/{prefix}", ".bed", ".bim", ".fam")
    output:
        'data/{prefix}.vcf'
    params:
        sdir = 'data/{prefix}',
        odir = 'data/{prefix}'
    conda:
        '../envs/plink.yaml'
    shell:
        "plink --bfile {params.sdir} --recode vcf --out {params.odir}"




