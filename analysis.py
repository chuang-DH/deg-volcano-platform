#analysis.py
#把 raw count matrix + control/treatment 欄位 → 丟進 PyDESeq2 →算出每個基因的 log2FC / pvalue / padj → 回傳成 DataFrame



import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

#算deg
def compute_deg_pydeseq2(
    count_df, #上傳的 Excel 讀進來的 DataFrame
    control_cols, #control 組 sample 欄位名稱（list）
    treat_cols, #treatment 組 sample 欄位名稱（list）
):
    """註解
    count_df:
        第一欄 = GeneID
        其餘欄位 = raw counts
    """

    # ===== counts: samples x genes =====DESeq2 規定：rows = samples，columns = genes
    counts = count_df[control_cols + treat_cols].T #全選，然後row和column互換
    counts.columns = count_df.iloc[:, 0] #GeneID取代，但GeneID未出現

    # ===== metadata =====#建立一個新的dataframe
    metadata = pd.DataFrame(   
        {
            "condition": (
                ["control"] * len(control_cols)
                + ["treatment"] * len(treat_cols)
            )
        },
        index=counts.index,
    )

    # ===== DESeq2 =====(independent filter)
    dds = DeseqDataSet(
        counts=counts,
        metadata=metadata,
        design_factors="condition",
    )

    dds.deseq2()

    stat_res = DeseqStats(
        dds,
        contrast=("condition", "treatment", "control"),
    )
    stat_res.summary()

    res = stat_res.results_df.copy()
    res.reset_index(inplace=True)
    res.rename(columns={"index": "GeneID"}, inplace=True)

    return res

