import json
import sys

rank_maps = {
        "U": "Unclassified",
        "R2": "Kingdom",
        "P": "Phylum",
        "C": "Class",
        "O": "Order",
        "F": "Family",
        "G": "Genus",
        "S": "Species",
        }


def kraken_report_to_sankey(
    report_file,
    view_ranks={"U", "R2", "P", "C", "O", "F", "G", "S"},
    min_reads=1,
    abundance=0.5,
    include_unclassified=False
):
    nodes = {}
    links = []

    # stack holds only *kept* ancestors
    stack = []  # (depth, name)

    with open(report_file) as f:
        for line in f:
            if not line.strip():
                continue

            parts = line.rstrip().split("\t")
            if len(parts) < 6:
                continue

            rel_aub, clade_reads, _, rank, _, name = parts
            clade_reads = int(clade_reads)

            if clade_reads < min_reads:
                continue

            if rank == "U" and not include_unclassified:
                continue

            # indentation → depth
            stripped = name.lstrip()
            depth = (len(name) - len(stripped)) // 2
            name = stripped

            if rank == "U":
                nodes[name] = {
                    "name": name,
                    "value": clade_reads,
                    "rank": "Unclassified",
                    "percent": rel_aub
                }

                links.append({
                    "source": name,
                    "target": name,
                    "value": 1e-6,
                    "rel": rel_aub
                })
                continue

            # pop until parent depth
            while stack and stack[-1][0] >= depth:
                stack.pop()

            # only keep selected ranks
            if rank not in view_ranks:
                continue
            if float(rel_aub) <= abundance:
                continue

            nodes[name] = {
                    "name": name,
                    "value": clade_reads,
                    "rank": rank_maps[rank],
                    "percent": rel_aub
                    }

            if stack:
                parent_name = stack[-1][1]
                links.append({
                    "source": parent_name,
                    "target": name,
                    "value": clade_reads,
                    "rel": rel_aub
                })

            stack.append((depth, name))

    return {
        "nodes": list(nodes.values()),
        "links": links
    }


def main(filepath):
    sankey_data_1 = kraken_report_to_sankey(
        filepath,
        # min_reads=3000,
        abundance=0.9,
        include_unclassified=True
    )

    sankey_data_0_5 = kraken_report_to_sankey(
        filepath,
        # min_reads=3000,
        abundance=0.5,
        include_unclassified=True
    )

    sankey_data_0_1 = kraken_report_to_sankey(
        filepath,
        # min_reads=3000,
        abundance=0.1,
        include_unclassified=False
    )
    data_1 = json.dumps(sankey_data_1, indent=2)
    data_0_5 = json.dumps(sankey_data_0_5, indent=2)
    data_0_1 = json.dumps(sankey_data_0_1, indent=2)

    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()
        # print(html)

    html = html.replace("{{DATA_1}}", data_1)
    html = html.replace("{{DATA_0.5}}", data_0_5)
    html = html.replace("{{DATA_0.1}}", data_0_1)

    with open("report2.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python kraken2sankey.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    main(filepath)
