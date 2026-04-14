from flask import Blueprint, render_template
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "Internship Hunter is alive. Hahaha.."
