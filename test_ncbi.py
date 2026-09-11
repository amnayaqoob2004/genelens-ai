from services.ncbi import search_gene

gene_id = search_gene("BRCA1")
print("Gene ID for BRCA1:", gene_id)