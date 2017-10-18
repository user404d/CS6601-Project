import argparse
from .circuit import generate


class Options:
    pass


options = Options()

parser = argparse.ArgumentParser(
    prog="SMC Threshold Dotproduct",
    description="Generate threshold based dotproduct circuit.",
)

parser.add_argument("domain_size", metavar="R", type=int)
parser.add_argument("dimensions", metavar="D", type=int)
parser.add_argument("threshold", metavar="T", type=int)

parser.parse_args(namespace=options)

generate(options.domain_size, options.dimensions, options.threshold)
