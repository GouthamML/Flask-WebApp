import os
from flask import Flask, render_template, request, redirect, url_for, session, escape, send_from_directory
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired
from werkzeug import secure_filename


app=Flask(__name__)
mysql=MySQL(app)