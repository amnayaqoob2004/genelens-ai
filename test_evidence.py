from services.ncbi import (
    search_gene, get_gene_info,
    search_nucleotide, get_nucleotide_record,
    search_protein, get_protein_record,
    search_pubmed, get_pubmed_articles,
)
from bioinformatics.sequence_analysis import analyze_sequence
from evidence.builder import build_evidence

gene_symbol = "BRCA1"

gene_id = search_gene(gene_symbol)
gene_info = get_gene_info(gene_id) if gene_id else None

nucleotide_id = search_nucleotide(gene_symbol)
nuc_record = get_nucleotide_record(nucleotide_id) if nucleotide_id else None
sequence_analysis = analyze_sequence(nuc_record["sequence"]) if nuc_record else None

protein_id = search_protein(gene_symbol)
protein_record = get_protein_record(protein_id) if protein_id else None

pmids = search_pubmed(gene_symbol, max_results=3)
pubmed_articles = get_pubmed_articles(pmids)

evidence = build_evidence(
    gene_symbol=gene_symbol,
    gene_info=gene_info,
    nuc_record=nuc_record,
    sequence_analysis=sequence_analysis,
    protein_record=protein_record,
    pubmed_articles=pubmed_articles,
)

import json
print(json.dumps(evidence, indent=2))