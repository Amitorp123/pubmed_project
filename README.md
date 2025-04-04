﻿# PubMed Project

# PubMed Research Paper Fetcher

## 📌 Project Description
This is a **CLI tool** that fetches **research papers from PubMed** based on a user-specified query.  
It identifies papers with **non-academic authors (pharmaceutical/biotech companies)** and saves the results in a CSV file.

The tool extracts important details such as:

1. Title
2. Publication Date
3. Non-Academic Authors
4. Company Affiliations
5.Corresponding Author Email
This project uses Python, Poetry, requests, and Typer to create an easy-to-use CLI.


## 🛠️ Installation

### **1. Clone the Repository**
--> git clone https://github.com/yourusername/pubmed_project.git
--> cd pubmed_project

2. Install Dependencies using Poetry
Make sure you have Poetry installed. Then, run:
--> poetry install


<!-- Usage Instructions -->
To fetch research papers from PubMed, use the following command:
Run the CLI tool using:
--> poetry run get-papers-list "machine learning" --file "papers.csv" --debug 
OR (any research paper name and saved as any name of ur choice)
--> poetry run get-papers-list "cancer research" --file "cancer_papers.csv" --debug


🔹 Command-line Arguments
Argument	            Description
QUERY	        Search term for fetching papers from PubMed
-h, --help	    Display usage instructions
-d, --debug	    Print debug information during execution
-f, --file	    Specify the output filename (default: output.csv)

This command will save the extracted research paper details into a CSV file.



📂 Project Structure
pubmed_project/
│── pubmed_fetch.py        # Main script for fetching research papers
│── pyproject.toml         # Poetry dependency file
│── poetry.lock            # Poetry lock file
│── README.md              # Documentation


📦 Dependencies
This project uses:
    Python 3.8+
    Poetry for dependency management
    Requests for API calls
    Typer for CLI interactions


<!-- How the Project Works -->
1. Fetches top 5 research papers from PubMed based on the search term.
2. Extracts title, publication date, authors, affiliations, and emails.
3. Filters out non-academic authors (working at "Inc.", "Ltd.", etc.).
4. Saves results in a CSV file for easy access.


📑 Example Output
The CSV file contains:
PubmedID, Title, Publication Date, Non-Academic Authors, Company Affiliations, Corresponding Author Em

<!-- Planned Future Improvements -->
o Support for fetching more than 5 papers.
o Ability to filter by year, journal, or author.
o Export to JSON format.


🔄 Version Control
Ensure all changes are committed:
--> git add .
--> git commit -m "Initial commit"
--> git push origin main


<!-- Tool used to build the program -->
 I consulted an LLM (ChatGPT) to refine my implementation, debug issues, and ensure adherence to best practices. Attached are screenshots or a document of the conversation for reference.
 

<!-- Developer Information -->
This project was developed by Protima Kumbhakar.
For queries or improvements, feel free to contribute!
