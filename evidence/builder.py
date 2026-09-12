def build_evidence(gene_symbol, gene_info=None, nuc_record=None, sequence_analysis=None,
                    protein_record=None, pubmed_articles=None):
    """
    Combine all retrieved data into a single structured evidence object.
    Any piece that wasn't found (None or empty) is clearly marked as 'not found',
    rather than being silently omitted.
    """

    evidence = {
        "query": gene_symbol,
        "gene": None,
        "nucleotide": None,
        "sequence_analysis": None,
        "protein": None,
        "pubmed_articles": [],
    }

    # ---- Gene section ----
    if gene_info:
        evidence["gene"] = {
            "symbol": gene_info.get("symbol", "Not available"),
            "gene_id": gene_info.get("gene_id", "Not available"),
            "organism": gene_info.get("organism", "Not available"),
            "location": gene_info.get("location", "Not available"),
            "description": gene_info.get("description", "Not available"),
        }

    # ---- Nucleotide section ----
    if nuc_record:
        evidence["nucleotide"] = {
            "accession": nuc_record.get("accession", "Not available"),
            "organism": nuc_record.get("organism", "Not available"),
            "length": nuc_record.get("length", "Not available"),
        }

    # ---- Sequence analysis section ----
    if sequence_analysis:
        evidence["sequence_analysis"] = {
            "length": sequence_analysis.get("length"),
            "gc_percent": sequence_analysis.get("gc_percent"),
            "a_percent": sequence_analysis.get("a_percent"),
            "t_percent": sequence_analysis.get("t_percent"),
            "g_percent": sequence_analysis.get("g_percent"),
            "c_percent": sequence_analysis.get("c_percent"),
            "ambiguous_count": sequence_analysis.get("ambiguous_count"),
        }

    # ---- Protein section ----
    if protein_record:
        evidence["protein"] = {
            "accession": protein_record.get("accession", "Not available"),
            "organism": protein_record.get("organism", "Not available"),
            "length": protein_record.get("length", "Not available"),
            "description": protein_record.get("description", "Not available"),
        }

    # ---- PubMed section ----
    if pubmed_articles:
        for article in pubmed_articles:
            evidence["pubmed_articles"].append({
                "pmid": article.get("pmid", "Not available"),
                "title": article.get("title", "Not available"),
                "authors": article.get("authors", "Not available"),
                "year": article.get("year", "Not available"),
                "abstract": article.get("abstract", "Not available"),
            })

    return evidence