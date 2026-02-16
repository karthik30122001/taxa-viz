import pandas as pd
import json

from taxa_viz.consensus import mpa_consensus
# from taxa_viz.errors import ValidationError

RANK_MAP = {
    "k__": "Kingdom",
    "p__": "Phylum",
    "c__": "Class",
    "o__": "Order",
    "f__": "Family",
    "g__": "Genus",
    "s__": "Species"
}


def get_rank(taxon):
    prefix = taxon[:3]
    return RANK_MAP.get(prefix, "Unknown")


def validate_dataframe(filepath, consensus):
    data = pd.read_csv(filepath, delimiter="\t")
    if len(data.columns) < 3:
        data.columns = ['classification', 'reads_count']
        data = add_relative_abundance(data)

        return data

    elif consensus:
        df = mpa_consensus(data)
        return df
    else:
        try:
            data.columns = [
                    'classification', 'reads_count', 'relative_abundance'
                    ]
            return data
        except Exception as e:
            raise Exception(
                f"Failed to parse input file: {e}"
            ) from e


def add_relative_abundance(dataframe):
    kingdom_only = dataframe[
        dataframe["classification"].str.count(r"\|") == 0
    ]
    total_reads = kingdom_only['reads_count'].sum()
    dataframe['relative_abundance'] = (dataframe['reads_count'] / total_reads * 100)
    return dataframe


def mpa_to_sankey(filepath, max_depth=None, min_percent=0.0, consensus=False):
    """
    Build Sankey nodes and edges with:
      - percent driving flow width
      - count stored for tooltips

    """
    df = validate_dataframe(filepath, consensus)
    rows = list(df.itertuples(index=False, name=None))
    nodes = []
    edges = []

    for path, count, percent in rows:
        if percent <= min_percent:
            continue

        parts = path.split("|")
        nodes.append(
                {
                    "name": parts[-1][3:],
                    "rank": get_rank(parts[-1]),
                    "percent": percent,
                    "value": percent
                    }
                )

        if max_depth is not None:
            parts = parts[:max_depth]

        if len(parts) > 1:
            edges.append({
                'source': parts[-2][3:],
                'target': parts[-1][3:],
                'rel': count,
                'value': percent
                })

    return {
        "nodes": nodes,
        "links": edges
    }


if __name__ == "__main__":

    data = pd.read_csv("CS1_lane1_db2.kraken2.mpa.txt", delimiter="\t")
# print(data.head())

    rows = list(data.itertuples(index=False, name=None))
    print(rows[:5])

    data_1 = json.dumps(mpa_to_sankey("CS1_lane1_db2.kraken2.mpa.txt", min_percent=4.9), indent=2)
    data_0_5 = json.dumps(mpa_to_sankey("CS1_lane1_db2.kraken2.mpa.txt", min_percent=0.9), indent=2)
    data_0_1 = json.dumps(mpa_to_sankey("CS1_lane1_db2.kraken2.mpa.txt", min_percent=0.49), indent=2)

    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()
        # print(html)

    html = html.replace("{{DATA_1}}", data_1)
    html = html.replace("{{DATA_0.5}}", data_0_5)
    html = html.replace("{{DATA_0.1}}", data_0_1)

    with open("LR_consensus.mpa.html", "w") as f:
        f.write(html)
