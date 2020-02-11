"""A slightly more portable wrapper for minidot plots."""

import argparse
import sys
from subprocess import call
import pysam
import os

parser = argparse.ArgumentParser()
parser.add_argument("minidotr", help="path to minidot.R [minidot.R]", default="minidot.R")
parser.add_argument("output", help="output name and format, prefix of all tmp files [minidot.pdf]", default="minidot.pdf")
parser.add_argument("fasta", help="fasta files", nargs='+')
parser.add_argument("--mapper", help="path to binary [minimap2]", default="minimap2")
parser.add_argument("--mode", help="mapper mode [asm10]", default="asm10")
parser.add_argument("--tmp", help="path to temporary location [/tmp]", default="/tmp")

parser.add_argument("--width", help="plot width (cm) [20]", default='20')
parser.add_argument("--thick", help="line thickness (px) [2]", default='2')
parser.add_argument("--title", help="plot title [None]")
parser.add_argument("--no-self", help="drop self-self mappings from resulting plot [False]", action='store_true', default=False)
parser.add_argument("--strip", help="remove facets, axes and junk [False]", action='store_true', default=False)
parser.add_argument("--identity", help="minimum identity for plot (0.0 - 1.0) [0]", default='0.0')
parser.add_argument("--alen", help="minimum length to plot an alignment [0]", default='0.0')
parser.add_argument("--ignore-missing", help="don't do anything if an input file is missing", action='store_true', default=False)
parser.add_argument("--drop-contains", help="drop sequences if their name contains one or more words from a comma delimited list", default="")

args = parser.parse_args()

if len(args.drop_contains) > 0:
    args.drop_contains = args.drop_contains.split(',')

prefix = '.'.join(args.output.split('.')[:-1])+'.'

#TODO Check the binaries (whatever)

# Index the FASTA and create the required LEN file
super_fasta = open(prefix+'fa', "w")
tlen = open(prefix+"tlen", "w")
for fasta in args.fasta:
    join_seq = []
    basename = os.path.basename(fasta).split('.')[0]
    try:
        fasta_fh = pysam.FastaFile(fasta)
        for reference in fasta_fh.references:
            if sum([word in reference for word in args.drop_contains]):
                print("Dropping %s as it appears in the --drop-contains list." % reference)
                continue
            seq = fasta_fh.fetch(reference=reference)
            join_seq.append(seq)
            tlen.write("%s\t%s\n" % (basename, len(seq)))
    except OSError as e:
        if args.ignore_missing:
            pass
        else:
            raise e
    super_fasta.write(">%s\n%s\n" % (basename, "".join(join_seq)))

super_fasta.close()
tlen.close()

paf = open(prefix+"paf", "w")
call([args.mapper, '-x', args.mode, '--no-long-join', '--dual=yes', '-P', prefix+'fa', prefix+'fa'], stdout=paf)
paf.close()

Rargs = ["-i", prefix+'paf', "-l", prefix+'tlen', '-o', args.output]
if args.no_self:
    Rargs.append('--no-self')
if args.strip:
    Rargs.append('--strip')
if args.title:
    Rargs.extend(['--title', args.title])
if args.width:
    Rargs.extend(['--width', args.width])
if args.thick:
    Rargs.extend(['--thick', args.thick])
if args.identity:
    Rargs.extend(['--identity', args.identity])
if args.alen:
    Rargs.extend(['--alen', args.alen])

print(Rargs)
call([args.minidotr] + Rargs)
