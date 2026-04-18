from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.database.db import init_db
from app.database.operations import get_all_jobs, mark_applied

main = Blueprint('main', __name__)

@main.route('/')
def index():
    init_db()
    jobs = get_all_jobs()
    filter_type = request.args.get('filter', 'all')
    if filter_type == 'top':
        jobs = [j for j in jobs if j['ai_score'] >= 8]
    elif filter_type == 'applied':
        jobs = [j for j in jobs if j['applied'] == 1]
    jobs = sorted(jobs, key=lambda x: x['ai_score'], reverse=True)
    return render_template('index.html', jobs=jobs)

@main.route('/apply/<int:job_id>')
def apply(job_id):
    mark_applied(job_id)
    flash('Marked as applied!', 'success')
    return redirect(url_for('main.index'))

@main.route('/scrape')
def scrape():
    from app.scraper.internshala import scrape_internshala
    from app.database.operations import insert_jobs
    jobs = scrape_internshala(keywords=["python", "machine learning", "ai"], max_pages=1)
    insert_jobs(jobs)
    flash(f'Scraped {len(jobs)} jobs.', 'success')
    return redirect(url_for('main.index'))

@main.route('/score')
def score():
    from app.agent.scorer import run_agent
    run_agent()
    flash('Agent finished scoring.', 'success')
    return redirect(url_for('main.index'))