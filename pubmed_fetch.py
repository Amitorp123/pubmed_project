

import requests        # Fetch Research Papers from PubMed
import csv             # Save Data to a CSV File
import typer
import sys
import xml.etree.ElementTree as ET


# Step1 Fetch Research Papers and details from PubMed
# Step2 Filter Non-Academic Authors
# Step3 Save Data to a CSV File
# Step4 Build a Command-Line Interface


app = typer.Typer()



#  Function to fetch paper IDs
def fetch_papers(query: str, debug: bool = False):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 5  
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        paper_ids = data.get("esearchresult", {}).get("idlist", [])
        if debug:
            typer.echo(f"[DEBUG] Fetched {len(paper_ids)} paper IDs: {paper_ids}")
        return paper_ids

    typer.echo("Error fetching data")
    return []



#  Function to fetch paper details
def fetch_paper_details(paper_id: str, debug: bool = False):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "xml"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        root = ET.fromstring(response.content)

        title_element = root.find(".//ArticleTitle")
        title = title_element.text if title_element is not None else "Unknown"

        pub_year = root.find(".//PubDate/Year")
        pub_month = root.find(".//PubDate/Month")
        pub_day = root.find(".//PubDate/Day")

        if pub_year is None:
            pub_year = root.find(".//ArticleDate/Year")
        if pub_month is None:
            pub_month = root.find(".//ArticleDate/Month")
        if pub_day is None:
            pub_day = root.find(".//ArticleDate/Day")

        pub_date = (
            f"{pub_year.text} {pub_month.text} {pub_day.text}"
            if pub_year is not None and pub_month is not None and pub_day is not None
            else "Unknown"
        )

        authors = []
        affiliations = []
        non_academic_authors = []

        for author in root.findall(".//Author"):
            last_name = author.find("LastName")
            initials = author.find("Initials")
            affiliation = author.find(".//AffiliationInfo/Affiliation")

            full_name = f"{last_name.text} {initials.text}" if last_name is not None and initials is not None else "Unknown Author"
            author_affiliation = affiliation.text if affiliation is not None else "Not Provided"

            authors.append(full_name)
            affiliations.append(author_affiliation)

            if is_non_academic(author_affiliation):
                non_academic_authors.append(full_name)

        email_element = root.find(".//AffiliationInfo/Note")
        email = email_element.text if email_element is not None and "@" in email_element.text else "Not Provided"

        if debug:
            typer.echo(f"[DEBUG] Paper {paper_id}: {title}, {pub_date}, Non-Academic Authors: {non_academic_authors}")

        return {
            "id": paper_id,
            "title": title,
            "date": pub_date,
            "non_academic_authors": ", ".join(non_academic_authors) if non_academic_authors else "None",
            "affiliations": ", ".join(set(affiliations)) if affiliations else "Not Provided",
            "email": email
        }

    return None




#  Function to check if an affiliation is non-academic
def is_non_academic(affiliation):
    non_academic_keywords = ["Pharmaceutical", "Biotech", "Company", "Inc", "Ltd", "Diagnostics", "Medical Center"]
    return any(keyword in affiliation for keyword in non_academic_keywords)



#  Function to save results to CSV
def save_to_csv(papers, filename: str):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non-Academic Author(s)", "Company Affiliations", "Corresponding Author Email"])

        for paper in papers:
            writer.writerow([paper["id"], paper["title"], paper["date"], paper["non_academic_authors"], paper["affiliations"], paper["email"]])

    typer.echo(f"Results saved to {filename}")




#  CLI Command
@app.command()
def get_papers_list(query: str, file: str = "output.csv", debug: bool = False):

    #""" Fetch research papers from PubMed based on a search query.#"""
    paper_ids = fetch_papers(query, debug)
    
    if not paper_ids:
        typer.echo("No research papers found for the given query.")
        raise typer.Exit()

    papers = []
    for pid in paper_ids:
        details = fetch_paper_details(pid, debug)
        if details:
            papers.append(details)

    save_to_csv(papers, file)

if __name__ == "__main__":
    app()


def main():
    app()
