from flask import Flask, Blueprint, render_template, url_for
import mysql.connector
from src.config import SQL_CREDENTIALS

budget_page = Blueprint('budget_page', __name__)

@budget_page.route('/budget')
def teste():
    page_title = "Fazenda - Budget Control"

    ganho = 300
    despesa = 500
    saldo = ganho - despesa

    valores = [page_title, ganho, despesa, saldo]

    return render_template("budget_page.html", valores = valores)
