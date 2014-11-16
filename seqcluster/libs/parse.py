import argparse
import sys


def parse_cl(in_args):
    sub_cmds = {"prepare": add_subparser_prepare,
                "cluster": add_subparser_cluster,
                "explore": add_subparser_explore,
                "collapse": add_subparser_collapse,
                "stats": add_subparser_stats}
    parser = argparse.ArgumentParser(description="small RNA analysis")
    sub_cmd = None
    if len(in_args) > 0 and in_args[0] in sub_cmds:
        subparsers = parser.add_subparsers(help="seqcluster supplemental commands")
        sub_cmds[in_args[0]](subparsers)
        sub_cmd = in_args[0]
    else:
        print "use prepare cluster explore collapse stats"
        sys.exit(0)
    args = parser.parse_args()

    assert sub_cmd is not None
    kwargs = {"args": args,
                  sub_cmd: True}
    return kwargs


def add_subparser_explore(subparsers):
    parser = subparsers.add_parser("explore", help="explore data")
    parser.add_argument("-j", "--json", dest="json", required=1,
            help="json file from seqcluster")
    parser.add_argument("-n", "--names", dest="names", required=1,
            help="comma-separeted id clusters"),
    parser.add_argument("-r", "--reference", dest="ref", required=1,
            help="reference fasta file with index"),
    parser.add_argument("-o", "--out", dest="out", required=1,
            help="dir of output files")
    parser.add_argument("-d", "--debug", action="store_true",
                       dest="debug", help="max verbosity mode", default=False)
    return parser


def add_subparser_prepare(subparsers):
    parser = subparsers.add_parser("prepare", help="prepare data")
    parser.add_argument("-c", "--conf", dest="dir", required=1,
            help="file with config file:1st column:path_to_fasta_file ; 2nd column:name")
    parser.add_argument("-o", "--out", dest="out", required=1,
            help="output dir")
    parser.add_argument("-l", "--minl", dest="minl", required=0,
            help="minimum length", default=18)
    parser.add_argument("-u", "--maxl", dest="maxl", required=0,
            help="maximum length", default=35)
    parser.add_argument("-e", "--minc", dest="minc", required=0,
            help="minimum counts", default=10)
    parser.add_argument("-d", "--debug", action="store_true",
                       dest="debug", help="max verbosity mode", default=False)
    return parser


def add_subparser_cluster(subparsers):
    parser = subparsers.add_parser("cluster", help="cluster data")
    parser.add_argument("-a", "--afile", dest="afile", required=1,
                      help="aligned file in bed/sam format")
    parser.add_argument("-m", "--ma", dest="ffile", required=1,
                      help="matrix file with sequences and counts for each sample")
    parser.add_argument("-g", "--gtf",
                       dest="gtf", help="annotate with gtf_file. It will use the 3rd column as the tag to annotate" +
                       "\nchr1    source  intergenic      1       11503   .       +       .       ")
    parser.add_argument("-b", "--bed",
                       dest="bed", help="annotate with bed_file. It will use the 4rd column as the tag to annotate" +
                       "\nchr1    157783  157886  snRNA   0       -")
    parser.add_argument("-o", "--out",
                       dest="out", help="output dir", required=1)
    parser.add_argument("-i", "--index",
                       dest="index", help="reference fasta")
    parser.add_argument("-d", "--debug", action="store_true",
                       dest="debug", help="max verbosity mode", default=False)
    parser.add_argument("-s", "--show", action="store_true",
                       dest="show", help="no show sequences", default=False)
    parser.add_argument("--split", action="store_true",
                       dest="split", help="split cluster if low sequences sharing", default=False)
    parser.add_argument("--similar",
                       dest="similar", help="threshold to consider two clusters identicals", default=0.8)
    parser.add_argument("--min_seqs",
                       dest="min_seqs", help="threshold to consider a cluster as valid", default=10)
    return parser


def add_subparser_stats(subparsers):
    parser = subparsers.add_parser("stats", help="stats data")
    parser.add_argument("-j", "--json", dest="json", required=0,
            help="json file from seqcluster")
    parser.add_argument("-m", "--ma", dest="ma", required=0,
            help="seqs.ma from prepare"),
    parser.add_argument("-a", "--sam", dest="sam", required=0,
            help="aligned file")
    parser.add_argument("-d", "--debug", action="store_true",
                       dest="debug", help="max verbosity mode", default=False)
    parser.add_argument("-o", "--out",
                       dest="out", help="output dir", required=1)
    return parser


def add_subparser_collapse(subparsers):
    parser = subparsers.add_parser("collapse", help="collapse data")
    parser.add_argument("-f", "--fastq", dest="fastq", required=1,
                        help="fastq file"),
    parser.add_argument("-d", "--debug", action="store_true",
                        dest="debug", help="max verbosity mode", default=False)
    parser.add_argument("-o", "--out",
                        dest="out", help="output file", required=1)
    return parser
