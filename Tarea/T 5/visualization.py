
from libraries import px


# ===============================
# PRINT TABLES
# ===============================
def print_ratios(altman):

    print("\n=== Altman Ratios ===")
    print(altman.ratios_matrix())


def print_z_scores(altman):

    print("\n=== Altman Z-Scores ===")
    print(altman.z_scores_df())


# ===============================
# PLOT
# ===============================
'''
def z_score_plot(z_df, title="Altman Z-Scores"):

    z_df = z_df.reset_index()
    z_df = z_df.sort_values("Z-Score")

    fig = px.bar(
        z_df,
        x="Ticker",
        y="Z-Score",
        color="Z-Score",
        color_continuous_scale=px.colors.sequential.Viridis,
        title=title
    )

    fig.update_layout(coloraxis_showscale=False)
    fig.show()
'''    

from libraries import plt


def z_score_plot(z_df, title="Altman Z-Scores"):

    z_df = z_df.reset_index()
    z_df = z_df.sort_values("Z-Score")

    colors = []

    for z in z_df["Z-Score"]:
        if z < 1.81:
            colors.append("#ba1e1e")
        elif z < 2.99:
            colors.append("#b4c2c3")
        else:
            colors.append("#6fee8b")

    plt.figure(figsize=(10,6))

    plt.bar(
        z_df["Ticker"],
        z_df["Z-Score"],
        color=colors
    )

    plt.axhline(1.8, linestyle="--", color = "#ba1e1e")
    plt.axhline(3, linestyle="--", color = "#1c682c")

    plt.title(title)
    plt.ylabel("Z-Score")
    plt.xlabel("Ticker")
    plt.legend(["Unsafe", "Safe"])
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()