from app.database.db import init_db
from app.database.operations import insert_jobs, get_all_jobs
from app.scraper.internshala import scrape_internshala

init_db()

jobs = scrape_internshala(keywords=["python"], max_pages=1)
insert_jobs(jobs)

all_jobs = get_all_jobs()
print(f"\nTotal in database: {len(all_jobs)}")
for job in all_jobs[:3]:
    print(f"{job['title']} — {job['company']} — {job['stipend']}")

print("\nSample job data:")
for k, v in jobs[0].items():
    print(f"  {k}: {repr(v)}")