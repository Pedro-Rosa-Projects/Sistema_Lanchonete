from flask import Flask, Blueprint, render_template, url_for

index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def teste():
    page_title = "Fazenda - Início"
    return render_template("index.html", page_title = page_title)
