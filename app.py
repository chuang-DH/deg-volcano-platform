#app.py

import streamlit as st
import pandas as pd
import time
import io

from analysis import compute_deg_pydeseq2
from volcano import plot_volcano


#----------------標題-------------

st.set_page_config(layout="wide")
st.title("🧬 Differential Expression Volcano Platform")

# ===== Upload =====
count_file = st.file_uploader(
    "Upload raw count matrix (Excel)",
    type=["xlsx"],
    help="First column = GeneID, other columns = raw counts"  #滑鼠移上去的?提示
)

#-------------------有上傳檔案後才繼續-------------------------

if count_file:
    count_df = pd.read_excel(count_file)



#-----------------為底下選取做準備------------------------
    st.subheader("Select sample columns")

    all_cols = list(count_df.columns)   #list取出所有欄位名稱
    

#================多功能下拉選項(勾選control和Treatment欄位)========
    control_cols = st.multiselect(
        "Control samples",
        all_cols[1:]
    )
    treat_cols = st.multiselect(
        "Treatment samples",
        all_cols[1:]
    )

    
    
# ===== Volcano options =====
    
    st.subheader("Volcano plot options") #副標題


    use_padj = st.checkbox(
        "Use adjusted p-value (FDR, padj)",
        value=True,
        help="Recommended for RNA-seq differential expression analysis"
    )
#是否用 padj(FDR)，預設為打勾




#==============滑桿(自主調整區間)============================

    pval_th = st.slider(
        "Significance threshold",
        min_value=0.001,
        max_value=0.1,
        value=0.05,
        step=0.001
    )

    log2fc_th = st.slider(
        "log2FC threshold",
        min_value=0.5,
        max_value=3.0,
        value=1.0,
        step=0.1
    )




# ===== Run ===============================
#raw counts 變成 DEG 統計結果 → 再把統計結果變成火山圖 + 可用的 DEG 表 → 告訴使用者跑完了

    if st.button("Run DESeq2 analysis"):
        if not control_cols or not treat_cols:
            st.error("Please select both control and treatment samples.")
        else:
            with st.spinner("Running PyDESeq2...", show_time=True):
                time.sleep(10)  #success
                deg_df = compute_deg_pydeseq2(
                    count_df,
                    control_cols,
                    treat_cols
                )

                fig, result_df, summary = plot_volcano(
                    deg_df,
                    use_padj=use_padj,
                    pval_th=pval_th,
                    log2fc_th=log2fc_th
                )

            st.success("Analysis completed!")

 


# ===== Summary =====
            st.subheader("DEG summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Up-regulated", summary["Up"])
            col2.metric("Down-regulated", summary["Down"])
            col3.metric("Not significant", summary["Not Sig"])

 # ===== Plot & table =====
            st.pyplot(fig)
            st.dataframe(result_df)
            buffer = io.BytesIO()
            result_df.to_excel(buffer, index=False)
            buffer.seek(0)

           #要匯出excel要先設置一個buffer
            st.download_button(
                "Download DEG table(CSV)",
                result_df.to_csv(index=False),
                file_name="DEG_result.csv"
            )


            st.download_button(
                "Download DEG table(Excel)",
                buffer,
                file_name="DEG_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"   
            )#檔案的身分證 application應用程式檔, vnd.openxmlformats微軟 Office 的 OpenXML 格式, spreadsheetml.sheetExcel 試算表


