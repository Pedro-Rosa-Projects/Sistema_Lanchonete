from flask import Flask, Blueprint, render_template, url_for
import mysql.connector
from src.config import SQL_CREDENTIALS

stock_page = Blueprint('stock_page', __name__)

@stock_page.route('/stock')
def teste():
    return "<p> stock Page </p>"
