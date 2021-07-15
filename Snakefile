#!python
configfile: "config.yaml"

include: "rules/data.snk.py"
include: "rules/locator.snk.py"
include: "rules/feems.snk.py"

rule none:
    input: 'Snakefile'
    run: print("drift-workflow")
