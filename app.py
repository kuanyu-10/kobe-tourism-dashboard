import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template, request

df = pd.read_excel("kobe_spots.xlsx")

df["popularity_score"] = (
    (df["rating"] / 5)
    * np.log(df["review_count"] + 1)
)

kpi_data = {
    "total_spots": len(df),
    "avg_rating": round(df["rating"].mean(), 2),
    "top_spot": df.sort_values(
        "popularity_score",
        ascending=False
    ).iloc[0]["spot_name"],
    "recommended_spots": int((df["rating"] >= 4.5).sum())
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

    return jsonify({
        "total_spots": len(filtered_df),
        "avg_rating": round(filtered_df["rating"].mean(), 2),
        "top_spot": filtered_df.sort_values(
            "popularity_score",
            ascending=False
        ).iloc[0]["spot_name"],
        "recommended_spots": int((filtered_df["rating"] >= 4.5).sum())
    })

@app.route("/api/area-visitors")
def api_area_visitors():

    area_counts = (
        df.groupby("area")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    return jsonify(
        area_counts.to_dict(orient="records")
    )

@app.route("/api/spot-visitors")
def api_spot_visitors():

    area = request.args.get("area", "all")

    filtered_df = df

    if area != "all":
        filtered_df = df[df["area"] == area]

    top_spots = (
        filtered_df.sort_values(
            "popularity_score",
            ascending=False
        )
        [["spot_name", "popularity_score"]]
        .head(10)
    )

    return jsonify(
        top_spots.to_dict(orient="records")
    )

@app.route("/api/spot-table")
def api_spot_table():

    area = request.args.get("area", "all")

    filtered_df = df

    if area != "all":
        filtered_df = df[df["area"] == area]

    ranking_table = (
        filtered_df.sort_values(
            "popularity_score",
            ascending=False
        )
        [
            [
                "spot_name",
                "area",
                "category",
                "rating",
                "review_count",
                "popularity_score"
            ]
        ]
        .head(15)
    )

    return jsonify(
        ranking_table.to_dict(orient="records")
    )

@app.route("/api/category-spots")
def api_category_spots():

    area = request.args.get("area", "all")

    filtered_df = df

    if area != "all":
        filtered_df = df[df["area"] == area]

    category_counts = (
        filtered_df.groupby("category")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    return jsonify(
        category_counts.to_dict(orient="records")
    )

if __name__ == "__main__":
    app.run(debug=True)