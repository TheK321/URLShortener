from flask import Flask, request, jsonify, redirect, render_template
from models import create_short_link
from database import create_connection, check_database

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten_web', methods=['POST'])
def shorten_url_web():
    original_url = request.form['url']
    short_code = create_short_link(original_url)
    short_url = f"http://localhost:5000/{short_code}"
    return render_template('result.html', short_url=short_url)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json['url']
    short_code = create_short_link(original_url)
    short_url = f"http://localhost:5000/{short_code}"
    return jsonify({'short_url': short_url})

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Obtener la URL original correspondiente al código corto
            sql = "SELECT link FROM urls WHERE short_url = %s"
            cursor.execute(sql, (short_code,))
            result = cursor.fetchone()
            if result:
                original_url = result["link"]

                # Incrementar el contador de visitas
                sql = "UPDATE urls SET hits = hits + 1 WHERE short_url = %s"
                cursor.execute(sql, (short_code,))
                connection.commit()

                # Redirigir al enlace original
                return redirect(original_url)

            else:
                return jsonify(error='Enlace no encontrado'), 404

    finally:
        connection.close()

@app.route('/stats/<short_code>', methods=['GET'])
def get_link_stats(short_code):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Obtener el recuento de visitas del enlace
            sql = "SELECT hits FROM urls WHERE short_url = %s"
            cursor.execute(sql, (short_code,))
            result = cursor.fetchone()
            if result:
                visit_count = result[0]
                return jsonify(visit_count=visit_count)

            else:
                return jsonify(error='Enlace no encontrado'), 404

    finally:
        connection.close()

@app.route('/getUrls')
def get_urls():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM urls"
            cursor.execute(sql)
            data = cursor.fetchall()
            if data:
                return jsonify(data), 200
            return jsonify({"error": "No data found"}), 404
    finally:
        connection.close()



if __name__ == '__main__':
    check_database()
    app.run(host='0.0.0.0')
