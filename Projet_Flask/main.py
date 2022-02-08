 # Librairie(s) utilisée(s)
import flask
import MySQLdb.cursors
from flask import url_for
from flask_mysqldb import MySQL
import re
# Création d’un objet application web Flask
app = flask.Flask(__name__)
# Créer une secret cle pour ne pas avoir une erreur
app.secret_key = "AZERTY"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_db'] = "Projet_Flask"
mysql = MySQL(app)
# pour générer une page web dynamique
@app.route("/", methods=['GET', 'POST'])
def connection():
	msg_error = ""
	if flask.request.method == "POST" and  "nom" in flask.request.form and "motdepasse" in flask.request.form:
		nom = flask.request.form["nom"]
		motdepasse = flask.request.form["motdepasse"]
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * users WHERE nom = %s AND motdepasse = %s", (nom,motdepasse,))
		utilisateur = cursor.fetchone()
		if utilisateur :
			flask.session["log"] = True
			flask.session["id"] = user["id"]
			flask.session["nom"] = user["nom"]
			return flask.redirect("/home")
		else:
			msg_error = "Oualalal il y a un problème, essaye de recommencer !"
	return flask.render_template("connection.html", msg=msg_error)

@app.route('deconnection')
def deconnection():
	flask.session.pop("log", None)
	flask.session.pop("id", None)
	flask.session.pop("nom", None)
	return flask.redirect(url_for('connection'))

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
	msg_error = ""
	if flask.request.method == "POST" and  "nom" in flask.request.form and "motdepasse" in flask.request.form:
		nom = flask.request.form["nom"]
		motdepasse = flask.request.form["motdepasse"]
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE nom = %s", (num,))
		user = cursor.fetchone()
		if user:
			msg_error = "nom d'utilisateur deja pris prend en un autre !"
		elif not re.match(r"[a-zA-Z0-9]", nom):
			msg_error = "ton pseudo ne doit comporter que des lettres ou des chiffres"
		elif not re.match(r"[a-zA-Z0-9]", motdepasse):
			msg_error = "ton mot de passe ne doit comporter que des lettres ou des chiffres"
		else:
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute("INSERT INTO users VALUES(NULL, %s, %s", (nom,motdepasse,))
			mysql.connection.commit()
			return flask.redirect(url_for('connection'))
	return flask.render_template("inscription.html", msg=msg_error)

@app.route('/accueil')
def accueil():
	if "log" in flask.session:
		nom = flask.session["nom"]
		return flask.render_template('accueil.html', nom=nom)
	else:
		return flask.redirect(url_for("connection"))
if __name__ == "__name__":
	app.run(host="0.0.0.0", port=1664, debug=True)
