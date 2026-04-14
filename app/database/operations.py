from app.database.db import get_connection

def clean_field(value):
    if not value:
        return ""
    return str(value).strip().replace("\n", " ").replace("\r", " ")

def insert_job(job):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT OR IGNORE INTO jobs
        (title, company, location, stipend, duration, url, source, keyword)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """, (
            clean_field(job.get("title")),
            clean_field(job.get("company")),
            clean_field(job.get("location")),
            clean_field(job.get("stipend")),
            clean_field(job.get("duration")),
            clean_field(job.get("url")),
            clean_field(job.get("source")),
            clean_field(job.get("keyword")),
        ))
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(f"Insert error: {e}")
        return 0
    finally:
        conn.close()



def insert_jobs(jobs):
    inserted = 0
    for job in jobs:
        inserted += insert_job(job)
    print(f"Inserted {inserted} new_jobs. {len(jobs) - inserted} duplicates skipped.")

def get_all_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY scraped_at DESC")
    jobs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jobs

def get_unscored_jobs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE ai_score = 0")
    jobs = [dict(row) for row in cursor.featchall()]
    conn.close()
    return jobs

def update_ai_score(job_id, score, reason):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE jobs SET ai_score = ?, ai_reason = ? WHERE id = ?
""", (score, reason, job_id))
    conn.commit()
    conn.close()

def mark_applied(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET applied = 1 WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
