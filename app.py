from flask import Flask, render_template
from sqlalchemy import create_engine, MetaData
import json
import time

app = Flask(__name__)

engine = create_engine("sqlite:///:memory:")
metadata = MetaData()

@app.route("/", methods = ["GET"])
def index():
    labels = ["Timestamp", "Hash", "Signature"]
    with open("blockChain.json") as f:
        data = json.loads(f.read())

    data_array = map(lambda x: [
        (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x[1]["time"])), "Unix epoch time: " + x[1]["time"]),
        (x[1]["hash"], "Hash"),
        ("%s ... %s" % (x[1]["sig"][:5], x[1]["sig"][-5:]), x[1]["sig"])
    ], sorted(data.items(), key=lambda x: x[0]))

    return render_template("index.html", labels=labels, data=data_array)

if __name__ == "__main__":
    app.run("0.0.0.0", port=80)