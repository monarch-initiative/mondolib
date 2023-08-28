"""Main python file."""
import pandas as pd


def demo():
    """Define API."""
    print("Hello, World!")


def validate(input: str, output: str):
    """Validate."""
    df = pd.read_csv(input, sep="\t", index_col=None)
    mondo_df = df.loc[df["subject"].str.startswith("MONDO:")]
    mondo_df.to_csv(output, sep="\t", index=False)


def update():
    """Update ontology file."""
    pass


if __name__ == "__main__":
    demo()
