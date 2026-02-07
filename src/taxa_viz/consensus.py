import pandas as pd
from skbio.stats import subsample_counts

df = pd.read_csv("LR_combined.mpa.txt", delimiter="\t")
print(df.head())
print(df.iloc[:, 1:].sum().min())
low = df.iloc[:, 1:].sum().min()


# print(df.iloc[:, 1].sum())
# print(subsample_counts(df.iloc[:, 1], low).sum())
# CS1 = pd.Series(subsample_counts(df.iloc[:, 1], low, seed=6969))
#
# CS2 = pd.Series(subsample_counts(df.iloc[:, 2], low, seed=6969))
#
# CS3 = pd.Series(subsample_counts(df.iloc[:, 3], low, seed=6969))
samples = []
for col in df.iloc[:, 1:].columns:
    sample = pd.Series(subsample_counts(df[col], low, seed=6969))
    samples.append(sample)


# subsampled_df = df.iloc[:, 0]
subsampled_df = pd.concat([df.iloc[:, 0], *samples], axis=1)
print(subsampled_df.sort_values(1, ascending=False).head())

print(subsampled_df.dtypes)
# print(subsampled_df.iloc[:, 1:].apply(lambda s: s.mean(), axis=1).head())

subsampled_df = subsampled_df.rename(
    columns={subsampled_df.columns[0]: "taxon"}
).set_index("taxon")

subsampled_df['reads_consensus'] = subsampled_df.mean(axis=1).round().astype(int)


kingdom_only = subsampled_df[
    subsampled_df.index.str.count(r"\|") == 0
]
total_reads = kingdom_only['reads_consensus'].sum()


subsampled_df['relative_abundance'] =(subsampled_df['reads_consensus'] / total_reads * 100)

print(subsampled_df.sort_values('relative_abundance', ascending=False).head())

subsampled_df[['reads_consensus', 'relative_abundance']].to_csv("LR_consensus.mpa.txt", sep="\t", header=True)


