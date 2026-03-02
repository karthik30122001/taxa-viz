# Taxa-Viz

Taxa-Viz is a lightweight tool for visualizing **Kraken/MPA taxonomic classification outputs** as an interactive Sankey diagram.

It lets you explore how read abundance flows across taxonomic ranks — and focus on specific taxa of interest.

---

## What It Does

* Parses Kraken / MPA taxonomy reports
* Generates an interactive Sankey diagram
* Preserves abundance proportions
* Supports dynamic filtering
* Allows lineage highlighting from a user-provided list

---

## Interactive Features

### Abundance Filtering

* Set a minimum abundance percentage
* Instantly remove low-abundance taxa from the view

### Rank Filtering

* Filter by specific taxonomic ranks
* Combine rank and abundance filters in any way

### Lineage Highlighting

* Provide a `list.txt` file containing taxa of interest
* Highlight specific lineages in the Sankey plot
* Quickly inspect targeted organisms within the full classification

---

## Why Use It?

Kraken reports are dense and text-heavy.
Taxa-Viz makes them easier to explore visually.

Use it to:

* Identify dominant taxa
* Explore taxonomic structure
* Focus on specific organisms
* Generate clean visual summaries

---

## Input

* Kraken `.mpa.txt` or compatible taxonomy report
* Optional `list.txt` file for highlighting specific taxa

---

## Output

* Interactive Sankey visualization (HTML)
* Real-time filtering and lineage highlighting

---

