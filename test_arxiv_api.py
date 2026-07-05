import arxiv

client = arxiv.Client()

search = arxiv.Search(
    query="quantum machine learning",
    max_results=5,  
    sort_by=arxiv.SortCriterion.SubmittedDate  
)

for paper in client.results(search):
    print(f"Title: {paper.title}")
    print(f"Published: {paper.published.date()}")
    print(f"Abstract URL: {paper.entry_id}")  
    print(f"PDF URL: {paper.pdf_url}")        
    print("-" * 50)
