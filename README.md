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


📌 Notes

Large data files (e.g. count tables) are ignored via .gitignore

This project is for educational and research use



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
