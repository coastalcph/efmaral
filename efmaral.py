#!/usr/bin/env python3

from cyalign import align, ibm_print_prob
from gibbs import ibm_print

import sys, argparse, random

parser = argparse.ArgumentParser(
    description='efmaral: efficient Markov Chain word alignment')
parser.add_argument(
    '-r', '--reverse', dest='reverse',
    action='store_true', help='Align in the reverse direction')
parser.add_argument(
    '--null-prior', dest='null_prior', default=0.2, metavar='X',
    type=float, help='Prior probability of NULL alignment')
parser.add_argument(
    '--lexical-alpha', dest='lex_alpha', default=1e-3, metavar='X',
    type=float, help='Dirichlet prior parameter for lexical distributions')
parser.add_argument(
    '--null-alpha', dest='null_alpha', default=1e-3, metavar='X',
    type=float, help='Dirichlet prior parameter for NULL word distribution')
parser.add_argument(
    '--seed', dest='seed', default=None,
    type=int, help='Random seed')
parser.add_argument(
    '-n', '--samplers', dest='n_samplers', default=2, metavar='N',
    type=int, help='Number of independent samplers')
parser.add_argument(
    '-l', '--length', dest='length', default=1.0, metavar='X',
    type=float, help='Relative number of sampling iterations')
parser.add_argument(
    '-i', '--input', dest='inputs', type=str, nargs='+',
    metavar='filename',
    help='Input (either one fast_align-format file, or two Europarl-style)')
parser.add_argument(
    '--probabilities', action='store_true',
    help='Output alignment probabilities together with the alignments')

args = parser.parse_args()

seed = random.randint(0, 0x7ffffff) if args.seed is None else args.seed

if len(args.inputs) not in (1, 2):
    raise ValueError('Only one or two input files allowed!')

alignments_list, sent_ps_list = align(args.inputs, args.n_samplers, args.length,
            args.null_prior, args.lex_alpha, args.null_alpha,
            args.reverse, seed)

print('Writing alignments...', file=sys.stderr)

if args.probabilities:
    ibm_print_prob(alignments_list, sent_ps_list, args.reverse)
else:
    ibm_print(alignments_list, args.reverse, sys.stdout.fileno())
