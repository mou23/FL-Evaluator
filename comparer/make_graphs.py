import matplotlib.pyplot as plt

def plot_graph(df, project, metric):
    plt.figure(figsize=(10, 6))
    colors = ['green' if diff > 0 else 'red' for diff in df["difference"]]
    plt.bar(df["Technique"], df["difference"], color=colors)
    plt.xlabel("Technique")
    plt.ylabel("Percentage change (%)")
    plt.title(f"Percentage Change (Cleaned vs Baseline) for {project}")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(f"{project}_{metric}.png")