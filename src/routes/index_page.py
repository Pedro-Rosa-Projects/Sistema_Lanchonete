from flask import Flask, Blueprint, render_template, url_for
import mysql.connector
from config import SQL_CREDENTIALS

index_page = Blueprint('index_page', __name__)

@index_page.route('/')
def teste():
    return "<p> index Page </p>"
