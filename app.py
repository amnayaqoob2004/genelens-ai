import streamlit as st
from services.ncbi import search_gene, get_gene_info

st.set_page_config(page_title="GeneLens AI", layout="wide")

st.title("🧬 GeneLens AI")
st.write("An AI-powered bioinformatics research explorer. Enter a gene symbol to begin.")

# Text input for the gene symbol
gene_symbol = st.text_input("Enter a gene symbol (e.g. BRCA1, TP53, EGFR, CFTR):")

# Search button
search_clicked = st.button("Search")

if search_clicked:
    if not gene_symbol.strip():
        st.warning("Please enter a gene symbol before searching.")
    else:
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