import os
import certifi
from Bio import Entrez, SeqIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fix for Windows SSL certificate issues:
# Point Python to certifi's trusted certificate bundle
os.environ["SSL_CERT_FILE"] = certifi.where()

# NCBI requires an email address to identify who is using their API
Entrez.email = os.getenv("NCBI_EMAIL")


def search_gene(gene_symbol, organism="Homo sapiens"):
    """
    Search NCBI Gene database for a gene symbol (e.g. 'BRCA1').
    Returns the NCBI Gene ID as a string, or None if not found.
    """
    query = f"{gene_symbol}[Gene Name] AND {organism}[Organism]"

    try:
        handle = Entrez.esearch(db="gene", term=query, retmax=1)
        record = Entrez.read(handle)
        handle.close()

        id_list = record.get("IdList", [])
        if not id_list:
            return None

        return id_list[0]

    except Exception as e:
        print(f"Error searching NCBI Gene: {e}")
        return None


def get_gene_info(gene_id):
    """
    Fetch detailed information about a gene using its NCBI Gene ID.
    Returns a dictionary with gene details, or None if not found.
    """
    try:
        handle = Entrez.esummary(db="gene", id=gene_id)
        record = Entrez.read(handle)
        handle.close()

        summary = record["DocumentSummarySet"]["DocumentSummary"][0]

        gene_info = {
            "gene_id": gene_id,
            "symbol": summary.get("Name", "Not available"),
            "description": summary.get("Description", "Not available"),
            "organism": summary.get("Organism", {}).get("ScientificName", "Not available"),
            "location": summary.get("MapLocation", "Not available"),
        }

        return gene_info

    except Exception as e:
        print(f"Error fetching gene info: {e}")
        return None


def search_nucleotide(gene_symbol, organism="Homo sapiens"):
    """
    Search NCBI Nucleotide database for a gene symbol.
    Returns a nucleotide record ID (string), or None if not found.
    """
    query = f"{gene_symbol}[Gene Name] AND {organism}[Organism] AND biomol_mrna[PROP]"

    try:
        handle = Entrez.esearch(db="nucleotide", term=query, retmax=1, sort="relevance")
        record = Entrez.read(handle)
        handle.close()

        id_list = record.get("IdList", [])
        if not id_list:
            return None

        return id_list[0]

    except Exception as e:
        print(f"Error searching NCBI Nucleotide: {e}")
        return None


def get_nucleotide_record(nucleotide_id):
    """
    Fetch a nucleotide/GenBank record's details using its ID.
    Returns a dictionary with accession, organism, length, and sequence,
    or None if not found.
    """
    try:
        handle = Entrez.efetch(db="nucleotide", id=nucleotide_id, rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")
        handle.close()

        nucleotide_info = {
            "accession": record.id,
            "organism": record.annotations.get("organism", "Not available"),
            "length": len(record.seq),
            "sequence": str(record.seq),
        }

        return nucleotide_info

    except Exception as e:
        print(f"Error fetching nucleotide record: {e}")
        return None


def search_protein(gene_symbol, organism="Homo sapiens"):
    """
    Search NCBI Protein database for a gene symbol.
    Returns a protein record ID (string), or None if not found.
    """
    query = f"{gene_symbol}[Gene Name] AND {organism}[Organism] AND refseq[filter]"

    try:
        handle = Entrez.esearch(db="protein", term=query, retmax=1, sort="relevance")
        record = Entrez.read(handle)
        handle.close()

        id_list = record.get("IdList", [])
        if not id_list:
            return None

        return id_list[0]

    except Exception as e:
        print(f"Error searching NCBI Protein: {e}")
        return None


def get_protein_record(protein_id):
    """
    Fetch a protein record's details using its ID.
    Returns a dictionary with name, accession, organism, length,
    description, and sequence, or None if not found.
    """
    try:
        handle = Entrez.efetch(db="protein", id=protein_id, rettype="gb", retmode="text")
        record = SeqIO.read(handle, "genbank")
        handle.close()

        protein_info = {
            "name": record.description,
            "accession": record.id,
            "organism": record.annotations.get("organism", "Not available"),
            "length": len(record.seq),
            "description": record.description,
            "sequence": str(record.seq),
        }

        return protein_info

    except Exception as e:
        print(f"Error fetching protein record: {e}")
        return None


def search_pubmed(gene_symbol, max_results=5):
    """
    Search PubMed for papers related to a gene symbol.
    Returns a list of PMIDs (strings), or an empty list if none found.
    """
    query = f"{gene_symbol}[Gene Name]"

    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="relevance")
        record = Entrez.read(handle)
        handle.close()

        return record.get("IdList", [])

    except Exception as e:
        print(f"Error searching PubMed: {e}")
        return []


def get_pubmed_articles(pmid_list):
    """
    Fetch details for a list of PubMed IDs.
    Returns a list of dictionaries with title, authors, publication date,
    PMID, and abstract snippet. Skips articles that fail to parse.
    """
    if not pmid_list:
        return []

    articles = []

    try:
        handle = Entrez.efetch(db="pubmed", id=pmid_list, rettype="abstract", retmode="xml")
        records = Entrez.read(handle)
        handle.close()

        for paper in records.get("PubmedArticle", []):
            try:
                medline = paper["MedlineCitation"]
                article = medline["Article"]

                title = article.get("ArticleTitle", "Title not available")

                author_list = article.get("AuthorList", [])
                authors = []
                for author in author_list:
                    last_name = author.get("LastName", "")
                    initials = author.get("Initials", "")
                    if last_name:
                        authors.append(f"{last_name} {initials}".strip())
                authors_str = ", ".join(authors) if authors else "Authors not available"

                pub_date_info = article.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
                year = pub_date_info.get("Year", "Date not available")

                pmid = str(medline["PMID"])

                abstract_sections = article.get("Abstract", {}).get("AbstractText", [])
                abstract = " ".join(str(section) for section in abstract_sections) if abstract_sections else "Abstract not available"

                articles.append({
                    "title": str(title),
                    "authors": authors_str,
                    "year": year,
                    "pmid": pmid,
                    "abstract": abstract,
                })

            except Exception as e:
                print(f"Skipping one article due to parsing error: {e}")
                continue

        return articles

    except Exception as e:
        print(f"Error fetching PubMed articles: {e}")
        return []