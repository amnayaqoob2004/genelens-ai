import streamlit as st
import pandas as pd
import plotly.express as px
from services.ncbi import search_gene, get_gene_info, search_nucleotide, get_nucleotide_record
from bioinformatics.sequence_analysis import analyze_sequence

st.set_page_config(page_title="GeneLens AI", layout="wide")

st.title("🧬 GeneLens AI")
st.write("An AI-powered bioinformatics research explorer. Enter a gene symbol to begin.")

gene_symbol = st.text_input("Enter a gene symbol (e.g. BRCA1, TP53, EGFR, CFTR):")
search_clicked = st.button("Search")

if search_clicked:
    if not gene_symbol.strip():
        st.warning("Please enter a gene symbol before searching.")
    else:
        # ---- Gene Overview ----
        with st.spinner(f"Searching NCBI Gene for {gene_symbol}..."):
            gene_id = search_gene(gene_symbol)

        if gene_id is None:
            st.error(f"No gene found for '{gene_symbol}'. Please check the spelling and try again.")
        else:
            gene_info = get_gene_info(gene_id)

            if gene_info is None:
                st.error("Gene was found, but detailed information could not be retrieved. Please try again.")
            else:
                st.subheader("📋 Gene Overview")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Gene Symbol", gene_info["symbol"])
                    st.metric("Gene ID", gene_info["gene_id"])
                with col2:
                    st.metric("Organism", gene_info["organism"])
                    st.metric("Location", gene_info["location"])

                st.write("**Description:**", gene_info["description"])

                # ---- Nucleotide / GenBank ----
                st.divider()
                st.subheader("🧬 Nucleotide Record (GenBank)")

                with st.spinner("Fetching nucleotide record..."):
                    nucleotide_id = search_nucleotide(gene_symbol)

                if nucleotide_id is None:
                    st.warning("No nucleotide record found for this gene.")
                else:
                    nuc_record = get_nucleotide_record(nucleotide_id)

                    if nuc_record is None:
                        st.warning("Nucleotide record found, but details could not be retrieved.")
                    else:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Accession", nuc_record["accession"])
                        with col2:
                            st.metric("Organism", nuc_record["organism"])
                        with col3:
                            st.metric("Sequence Length", f"{nuc_record['length']:,} bp")

                        with st.expander("View full sequence"):
                            st.code(nuc_record["sequence"], language=None)

                        # ---- Sequence Analysis ----
                        st.subheader("📊 Sequence Analysis")

                        analysis = analyze_sequence(nuc_record["sequence"])

                        if analysis is None:
                            st.warning("Could not analyze this sequence.")
                        else:
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("A", f"{analysis['a_count']:,} ({analysis['a_percent']}%)")
                            with col2:
                                st.metric("T", f"{analysis['t_count']:,} ({analysis['t_percent']}%)")
                            with col3:
                                st.metric("G", f"{analysis['g_count']:,} ({analysis['g_percent']}%)")
                            with col4:
                                st.metric("C", f"{analysis['c_count']:,} ({analysis['c_percent']}%)")

                            st.metric("GC Content", f"{analysis['gc_percent']}%")

                            if analysis["ambiguous_count"] > 0:
                                st.caption(f"Note: {analysis['ambiguous_count']} ambiguous base(s) (e.g. 'N') were excluded from percentage calculations.")

                            # Bar chart of base composition
                            chart_data = pd.DataFrame({
                                "Base": ["A", "T", "G", "C"],
                                "Count": [analysis["a_count"], analysis["t_count"], analysis["g_count"], analysis["c_count"]],
                            })
                            fig = px.bar(chart_data, x="Base", y="Count", title="Base Composition", color="Base")
                            st.plotly_chart(fig, use_container_width=True)