from flask import Flask, Blueprint, render_template, url_for
import mysql.connector
from config import SQL_CREDENTIALS

sales_page = Blueprint('sales_page', __name__)

@sales_page.route('/sales')
def teste():
    page_title = "Fazenda - Início"
    return render_template("sales_page.html", page_title = page_title)
