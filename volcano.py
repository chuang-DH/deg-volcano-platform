# volcano.py
# 設計理念：
# - 不 drop 掉任何基因
# - DESeq2 沒檢定的基因標記為 Too low / Not tested
# - 火山圖只畫被檢定過的基因

import numpy as np
import matplotlib.pyplot as plt


def plot_volcano(
    df,
    use_padj=True,
    pval_th=0.05,
    log2fc_th=1.0,
):
    df = df.copy()

    # ===== column alignment =====
    df = df.rename(columns={
        "log2FoldChange": "log2FC",
        "pvalue": "p_value",
        "padj": "padj",
    })

    p_col = "padj" if use_padj else "p_value"

    # ===== Test status =====
    df["TestStatus"] = "Tested"
    df.loc[df[p_col].isna() | df["log2FC"].isna(), "TestStatus"] = "Too low / Not tested"

    # ===== -log10(p)（只對被檢定的算）=====
    df["-log10(p)"] = np.nan
    tested_mask = df["TestStatus"] == "Tested"
    df.loc[tested_mask, "-log10(p)"] = -np.log10(
        df.loc[tested_mask, p_col].replace(0, 1e-300)
    )

    # ===== Regulation =====
    def classify(row):
        if row["TestStatus"] != "Tested":
            return "Too low"

        if row[p_col] < pval_th:
            if row["log2FC"] > log2fc_th:
                return "Up"
            elif row["log2FC"] < -log2fc_th:
                return "Down"
        return "Not Sig"

    df["Regulation"] = df.apply(classify, axis=1)

    # ===== clip for plotting =====
    df["log2FC_clipped"] = df["log2FC"].clip(-10, 10)

    # ===== summary（不把 Too low 算進 DEG）=====
    summary = df[df["TestStatus"] == "Tested"]["Regulation"].value_counts().to_dict()
    for k in ["Up", "Down", "Not Sig"]:
        summary.setdefault(k, 0)

    summary["Too low / Not tested"] = (df["TestStatus"] != "Tested").sum()

    # ===== colors =====
    colors = {
        "Up": "red",
        "Down": "blue",
        "Not Sig": "gray",
    }

    # ===== plot only tested genes =====
    fig, ax = plt.subplots(figsize=(9, 7))

    plot_df = df[df["TestStatus"] == "Tested"]

    for g in ["Up", "Down", "Not Sig"]:
        sub = plot_df[plot_df["Regulation"] == g]
        ax.scatter(
            sub["log2FC_clipped"],
            sub["-log10(p)"],
            c=colors[g],
            s=20,
            alpha=0.7,
            label=g,
        )

    ax.axhline(-np.log10(pval_th), linestyle="--")
    ax.axvline(log2fc_th, linestyle="--")
    ax.axvline(-log2fc_th, linestyle="--")

    ax.set_xlabel("log2(Fold Change)")
    ax.set_ylabel(f"-log10({'padj' if use_padj else 'p-value'})")
    ax.set_title("Volcano Plot")
    ax.legend()
    ax.grid(True)

    # index 整理（給匯出用）
    df = df.reset_index(drop=True)

    return fig, df, summary
