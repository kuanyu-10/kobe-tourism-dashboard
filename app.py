import pandas as pd
from flask import Flask, jsonify, render_template, request

df = pd.read_csv("tourism_data.csv")

total_visitors = df["visitors"].sum()

area_ranking = (
    df.groupby("area")["visitors"]
    .sum()
    .sort_values(ascending=False)
)

spot_ranking = (
    df.groupby("spot")["visitors"]
    .sum()
    .sort_values(ascending=False)
)

monthly_visitors = (
    df.groupby("month")["visitors"]
    .sum()
    .reset_index()
)

last_month = monthly_visitors.iloc[-2]["visitors"]

current_month = monthly_visitors.iloc[-1]["visitors"]

growth_rate = (
    (current_month - last_month)
    / last_month
    * 100
)

area_visitors = (
    df.groupby("area")["visitors"]
    .sum()
    .reset_index()
    .sort_values("visitors", ascending=False)
)

spot_visitors = (
    df.groupby("spot")["visitors"]
    .sum()
    .reset_index()
    .sort_values("visitors", ascending=False)
)

kpi_data = {
    "total_visitors": f"{int(total_visitors):,}人",
    "growth_rate": f"+{growth_rate:.1f}%",
    "top_area": area_ranking.idxmax(),
    "top_spot": spot_ranking.idxmax()
}

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", kpi_data=kpi_data)

@app.route("/api/kpi")
def api_kpi():

    area = request.args.get("area", "all")

    filtered_df = df

    if area != "all":
        filtered_df = df[df["area"] == area]

    total_visitors = filtered_df["visitors"].sum()

    top_spot = (
        filtered_df.groupby("spot")["visitors"]
        .sum()
        .idxmax()
    )

    return jsonify({
        "total_visitors": f"{int(total_visitors):,}人",
        "top_spot": top_spot
    })

@app.route("/api/monthly-visitors")
def api_monthly_visitors():
    area = request.args.get("area", "all")

    filtered_df = df

    if area != "all":
        filtered_df = df[df["area"] == area]

    monthly_data = (
        filtered_df.groupby("month")["visitors"]
        .sum()
        .reset_index()
    )

    return jsonify(
        monthly_data.to_dict(orient="records")
    )

@app.route("/api/area-visitors")
def api_area_visitors():
    return jsonify(area_visitors.to_dict(orient="records"))

@app.route("/api/spot-visitors")
def api_spot_visitors():
    return jsonify(spot_visitors.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)