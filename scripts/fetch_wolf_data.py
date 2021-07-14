import pkg_resources
import snakemake as snk

data_path = pkg_resources.resource_filename("feems", "data/")

input = ['{}wolvesadmix.{}'.format(data_path, ext) for ext in ['bed', 'bim', 'fam', 'coord']]
for i, o  in zip(input, snakemake.output):
    print('copying {} to {}'.format(i, o))
    snk.shell('cp {} {}'.format(i, o))