# app.py
import os
import time

import pymysql
from flask import Flask, jsonify

app = Flask(__name__)


def connect_db():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

@app.get("/")
def index():
    last_error = None

    for _ in range(10):
        try:
            with connect_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS visits (
                            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                        )
                        """
                    )
                    cursor.execute("INSERT INTO visits () VALUES ()")
                    conn.commit()
                    cursor.execute("SELECT COUNT(*) AS count FROM visits")
                    row = cursor.fetchone()


            return jsonify(
                message="Flask connected to MySQL through the Compose network",
                db_host=os.environ["DB_HOST"],
                visits=row["count"],
            )
        except Exception as error:
            last_error = error
            time.sleep(2)

    return jsonify(error=str(last_error)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


@app.route("/health")
def health():
    data = dict(status="healthy")
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

