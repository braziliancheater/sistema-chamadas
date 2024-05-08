from flask import Blueprint

@app.route("/")
def index():
    return '<p>Index Pagina Principal<p>'