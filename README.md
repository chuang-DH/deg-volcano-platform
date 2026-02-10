# 🧬 Differential Expression Volcano Platform

A simple Streamlit-based platform for RNA-seq differential expression analysis
and volcano plot visualization.

## ✨ Features
- Upload raw count matrix (Excel)
- Differential expression analysis (PyDESeq2)
- Interactive volcano plot
- Export DEG result table


## 📁 Project Structure
analysis.py # differential expression calculation

volcano.py # volcano plot + gene classification

app.py # Streamlit UI




## License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 License.

Commercial use is not permitted without explicit permission from the author.



## Streamlit test 
https://deg-volcano-platform-6htpr5ugnf8ygqcwarfbe2.streamlit.app/


## Test step 
- 1. Upload raw count matrix (Excel) 3x control and 3x treatment 
- 2. select sample column (select Control samples 3x and treatment samples 3x)
- 3. check Use adjusted p-value(FDR, padj)  
- 4. Adjust stick settings of Significance threshold(0.05) and log2FC threshold(1)
- 5. Run Deseq2 analysis(around 1m30s. depend on data size)
- 6. output volcano plot and calculated column 



## note: 

- 1. Test status shows “Too low / Not tested” because the PyDESeq2 model automatically filters out low-count genes to avoid influencing FDR estimation.
- 2. log2FC threshold(1) contain 1 and -1



## References

[1] Love, M. I., Huber, W., & Anders, S. (2014).
"Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2."
Genome Biology, 15(12), 1–21.
https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0550-8

[2] Zhu, A., Ibrahim, J. G., & Love, M. I. (2019).
"Heavy-tailed prior distributions for sequence count data: removing the noise and preserving large differences."
Bioinformatics, 35(12), 2084–2092.
https://academic.oup.com/bioinformatics/article/35/12/2084/5159452

[3] Muzellec, B., Teleńczuk, M., Cabeli, V., & Andreux, M. (2023).
"PyDESeq2: a python package for bulk RNA-seq differential expression analysis."
Bioinformatics.
https://doi.org/10.1093/bioinformatics/btad547



Differential expression analysis is performed using PyDESeq2 [3],
which re-implements the DESeq2 model [1,2] in Python.
