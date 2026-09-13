import streamlit as st
import pandas as pd
import plotly.express as px
from services.ncbi import (
    search_gene, get_gene_info,
    search_nucleotide, get_nucleotide_record,
    search_protein, get_protein_record,
    search_pubmed, get_pubmed_articles,
)
from bioinformatics.sequence_analysis import analyze_sequence
from evidence.builder import build_evidence
from services.ai import generate_research_brief, ask_genelens

st.set_page_config(page_title="GeneLens AI", layout="wide")

with st.sidebar:
    st.header("🧬 GeneLens AI")
    st.write("An AI-powered bioinformatics research explorer.")

    st.subheader("Try an example:")
    example_genes = ["BRCA1", "TP53", "EGFR", "CFTR"]
    for example in example_genes:
        if st.button(example, use_container_width=True):
            st.session_state["active_gene"] = example

    st.divider()
    st.caption("Data sources: NCBI Gene, Nucleotide, Protein, and PubMed.")
    st.caption("AI responses are grounded strictly in retrieved evidence and clearly labeled as fact vs. interpretation.")

st.title("🧬 GeneLens AI")
st.write("An AI-powered bioinformatics research explorer. Enter a gene symbol to begin.")

gene_symbol_input = st.text_input("Enter a gene symbol (e.g. BRCA1, TP53, EGFR, CFTR):")
search_clicked = st.button("Search")

if search_clicked:
    if not gene_symbol_input.strip():
        st.warning("Please enter a gene symbol before searching.")
        st.session_state["active_gene"] = None
    else:
        st.session_state["active_gene"] = gene_symbol_input.strip()

gene_symbol = st.session_state.get("active_gene")

if gene_symbol:
    with st.spinner(f"Searching NCBI Gene for {gene_symbol}..."):
        gene_id = search_gene(gene_symbol)

    if gene_id is None:
        st.error(f"No gene found for '{gene_symbol}'. Please check the spelling and try again.")
    else:
        gene_info = get_gene_info(gene_id)

        if gene_info is None:
            st.error("Gene was found, but detailed information could not be retrieved. Please try again.")
            st.stop()

        tab_gene, tab_nuc, tab_protein, tab_pubmed, tab_ai = st.tabs(
            ["📋 Gene Overview", "🧬 Nucleotide", "🧪 Protein", "📚 PubMed", "🤖 AI Brief & Ask"]
        )

        # ---- Gene Overview Tab ----
        with tab_gene:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Gene Symbol", gene_info["symbol"])
                st.metric("Gene ID", gene_info["gene_id"])
            with col2:
                st.metric("Organism", gene_info["organism"])
                st.metric("Location", gene_info["location"])
            st.write("**Description:**", gene_info["description"])

        # ---- Nucleotide Tab ----
        with tab_nuc:
            with st.spinner("Fetching nucleotide record..."):
                nucleotide_id = search_nucleotide(gene_symbol)

            nuc_record = None
            sequence_analysis = None

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

                    st.subheader("📊 Sequence Analysis")
                    sequence_analysis = analyze_sequence(nuc_record["sequence"])

                    if sequence_analysis is None:
                        st.warning("Could not analyze this sequence.")
                    else:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("A", f"{sequence_analysis['a_count']:,} ({sequence_analysis['a_percent']}%)")
                        with col2:
                            st.metric("T", f"{sequence_analysis['t_count']:,} ({sequence_analysis['t_percent']}%)")
                        with col3:
                            st.metric("G", f"{sequence_analysis['g_count']:,} ({sequence_analysis['g_percent']}%)")
                        with col4:
                            st.metric("C", f"{sequence_analysis['c_count']:,} ({sequence_analysis['c_percent']}%)")

                        st.metric("GC Content", f"{sequence_analysis['gc_percent']}%")

                        if sequence_analysis["ambiguous_count"] > 0:
                            st.caption(f"Note: {sequence_analysis['ambiguous_count']} ambiguous base(s) (e.g. 'N') were excluded from percentage calculations.")

                        chart_data = pd.DataFrame({
                            "Base": ["A", "T", "G", "C"],
                            "Count": [sequence_analysis["a_count"], sequence_analysis["t_count"], sequence_analysis["g_count"], sequence_analysis["c_count"]],
                        })
                        fig = px.bar(chart_data, x="Base", y="Count", title="Base Composition", color="Base")
                        st.plotly_chart(fig, use_container_width=True)

        # ---- Protein Tab ----
        with tab_protein:
            with st.spinner("Fetching protein record..."):
                protein_id = search_protein(gene_symbol)

            protein_record = None

            if protein_id is None:
                st.warning("No protein record found for this gene.")
            else:
                protein_record = get_protein_record(protein_id)

                if protein_record is None:
                    st.warning("Protein record found, but details could not be retrieved.")
                else:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Accession", protein_record["accession"])
                    with col2:
                        st.metric("Organism", protein_record["organism"])
                    with col3:
                        st.metric("Length", f"{protein_record['length']:,} aa")

                    st.write("**Description:**", protein_record["description"])

                    with st.expander("View full protein sequence"):
                        st.code(protein_record["sequence"], language=None)

        # ---- PubMed Tab ----
        with tab_pubmed:
            with st.spinner("Searching PubMed..."):
                pmids = search_pubmed(gene_symbol, max_results=5)

            pubmed_articles = []

            if not pmids:
                st.warning("No PubMed articles found for this gene.")
            else:
                pubmed_articles = get_pubmed_articles(pmids)

                if not pubmed_articles:
                    st.warning("Articles were found, but details could not be retrieved.")
                else:
                    for article in pubmed_articles:
                        with st.container(border=True):
                            st.markdown(f"**{article['title']}**")
                            st.caption(f"{article['authors']} · {article['year']} · PMID: {article['pmid']}")
                            st.write(article["abstract"][:400] + ("..." if len(article["abstract"]) > 400 else ""))
                            st.markdown(f"[View on PubMed](https://pubmed.ncbi.nlm.nih.gov/{article['pmid']}/)")

        # ---- AI Brief & Ask Tab ----
        with tab_ai:
            evidence = build_evidence(
                gene_symbol=gene_symbol,
                gene_info=gene_info,
                nuc_record=nuc_record,
                sequence_analysis=sequence_analysis,
                protein_record=protein_record,
                pubmed_articles=pubmed_articles,
            )
            st.session_state["evidence"] = evidence

            st.subheader("🤖 AI Research Brief")
            if st.button("Generate AI Research Brief"):
                with st.spinner("Generating evidence-grounded research brief..."):
                    brief = generate_research_brief(st.session_state["evidence"])
                st.session_state["brief"] = brief

            if "brief" in st.session_state and st.session_state.get("evidence", {}).get("query") == gene_symbol:
                st.markdown(st.session_state["brief"])

            st.divider()
            st.subheader("💬 Ask GeneLens")
            st.write("Ask a specific question about this gene, based only on the retrieved evidence above.")

            user_question = st.text_input("Your question:", key="user_question")
            ask_clicked = st.button("Ask")

            if ask_clicked:
                if not user_question.strip():
                    st.warning("Please type a question first.")
                else:
                    with st.spinner("Thinking..."):
                        answer = ask_genelens(st.session_state["evidence"], user_question)
                    st.session_state["last_answer"] = answer
                    st.session_state["last_question"] = user_question

            if "last_answer" in st.session_state and st.session_state.get("evidence", {}).get("query") == gene_symbol:
                st.markdown(f"**Q: {st.session_state['last_question']}**")
                st.markdown(st.session_state["last_answer"])