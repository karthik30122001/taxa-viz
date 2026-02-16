import argparse
import sys

from taxa_viz.mpa2sankey import mpa_to_sankey
from taxa_viz.generate_report import render_html
# from taxa_viz.kraken_to_sankey import kraken_to_sankey


def load_highlights(args):
    if args.highlight_list:
        with open(args.highlight_list) as fh:
            return [
                line.strip()
                for line in fh
                if line.strip()
            ]

    return []


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="taxa-viz",
        description="Generate interactive Sankey plots from taxonomic classifier outputs",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Input format",
    )

    # ---- Kraken subcommand ----
    # kraken = subparsers.add_parser(
    #     "kraken",
    #     help="Convert Kraken/Bracken/MPA-style report to Sankey",
    # )
    # kraken.add_argument(
    #     "input",
    #     help="Kraken report file",
    # )
    # kraken.add_argument(
    #     "-o",
    #     "--output",
    #     default="sankey.html",
    #     help="Output HTML file (default: sankey.html)",
    # )
    #
    # ---- MetaPhlAn subcommand ----
    metaphlan = subparsers.add_parser(
        "metaphlan",
        help="Convert MetaPhlAn output to Sankey",
    )
    metaphlan.add_argument(
        "input",
        help="MetaPhlAn output file",
    )
    metaphlan.add_argument(
        "-o",
        "--output",
        default="sankey.html",
        help="Output HTML file (default: sankey.html)",
    )
    metaphlan.add_argument(
        "-l",
        "--highlight-list",
        metavar="FILE",
        help="File containing taxa to highlight (one per line)",
    )
    metaphlan.add_argument(
        "-c",
        "--consensus",
        action="store_true",
        default=False,
        help="Consensus plot for multi-sample files",
    )

    args = parser.parse_args()

    try:
        # if args.command == "kraken":
        #     nodes, edges = kraken_to_sankey(args.input)
        #
        if args.command == "metaphlan":
            data_1 = mpa_to_sankey(args.input, min_percent=4.9, consensus=args.consensus)
            data_0_5 = mpa_to_sankey(args.input, min_percent=0.9, consensus=args.consensus)
            data_0_1 = mpa_to_sankey(args.input, min_percent=0.49, consensus=args.consensus)

        else:
            parser.error("Unknown command")

        # Render HTML (centralised here or in a helper)
        list = load_highlights(args)
        render_html(data_1, data_0_5, data_0_1, args.output, list)

    # except FileFormatError as e:
    #     print(f"File format error: {e}", file=sys.stderr)
    #     sys.exit(2)
    #
    # except ValidationError as e:
    #     print(f"Validation error: {e}", file=sys.stderr)
    #     sys.exit(3)

    except Exception as e:
        # Truly unexpected error
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(99)


if __name__ == "__main__":
    main()
