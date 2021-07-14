import pkg_resources
data_path = pkg_resources.resource_filename("feems", "data/")

input = ['{}wolvesadmix.{}'.format(data_path, ext) for ext in ['bed', 'bim', 'fam']]
for i, o  in zip(input, output):
    print('copying {} to {}'.format(i, o))
    shell('cp {} {}'.format(i, o))