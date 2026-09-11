import os
import certifi
from Bio import Entrez
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