from services.ncbi import search_gene, get_gene_info, search_nucleotide, get_nucleotide_record
from bioinformatics.sequence_analysis import analyze_sequence

gene_id = search_gene("BRCA1")
print("Gene ID for BRCA1:", gene_id)

if gene_id:
    info = get_gene_info(gene_id)
    print("Gene Info:", info)

nucleotide_id = search_nucleotide("BRCA1")
print("Nucleotide ID for BRCA1:", nucleotide_id)

if nucleotide_id:
    nuc_record = get_nucleotide_record(nucleotide_id)
    print("Accession:", nuc_record["accession"])
    print("Organism:", nuc_record["organism"])
    print("Length:", nuc_record["length"])

    analysis = analyze_sequence(nuc_record["sequence"])
    print("Sequence Analysis:", analysis)