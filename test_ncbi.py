from services.ncbi import search_gene, get_gene_info

gene_id = search_gene("BRCA1")
print("Gene ID for BRCA1:", gene_id)

if gene_id:
    info = get_gene_info(gene_id)
    print("Gene Info:", info)