rule download_ag:
    output:
        'output/ag3/manifest.tsv'
    run:
        shell("mkdir output/ag3")
        shell("gsutil cp gs://vo_agam_release/v3/manifest.tsv output/ag3/manifest.tsv")
        shell("mkdir output/ag3/metadata/")
        shell("gsutil -m rsync -r gs://vo_agam_release/v3/metadata/ output/ag3/metadata/")


rule prep_human_vcf:
    input:
        multiext("/project2/jnovembre/old_project/bpeter/eems_tib/subset/c1global1nfd", ".bed", ".bim", ".fam")
    output:
        'data/popres/global/c1global1nfd.vcf'
    params:
        sdir = '/project2/jnovembre/old_project/bpeter/eems_tib/subset/c1global1nfd'
        odir = 'data/popres/global/c1global1nfd'
    conda:
        '../envs/plink.yaml'
    shell:
        "plink --bfile {params.sdir} --recode vcf --out {params.odir}"




