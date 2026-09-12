
from services.ncbi import search_pubmed, get_pubmed_articles

pmids = search_pubmed("BRCA1", max_results=3)
print("PMIDs found:", pmids)

articles = get_pubmed_articles(pmids)
for article in articles:
    print("\n---")
    print("Title:", article["title"])
    print("Authors:", article["authors"])
    print("Year:", article["year"])
    print("PMID:", article["pmid"])
    print("Abstract snippet:", article["abstract"][:150])