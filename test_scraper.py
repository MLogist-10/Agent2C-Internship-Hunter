from app.scraper.internshala import scrape_internshala

jobs = scrape_internshala(keywords=["python"], max_pages=1)

print(f"\nTotal: {len(jobs)} jobs\n")
for job in jobs[:5]:
    print(f"Title    : {job['title']}")
    print(f"Company  : {job['company']}")
    print(f"Location : {job['location']}")
    print(f"Stipend  : {job['stipend']}")
    print(f"URL      : {job['url']}")
    print("-" * 40)