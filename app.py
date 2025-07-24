from flask import Flask, request, jsonify, render_template, send_from_directory
from apscheduler.schedulers.background import BackgroundScheduler
from aliver import keep_alive
import json
from tabulator import tabulate
import os
from analysis import generate_res_files
from analysis_2 import generate_res2_files

app = Flask(__name__)
generate_res_files()
generate_res2_files()


# Setting up Schedulars
scheduler = BackgroundScheduler()
scheduler.add_job(
    id="aliver",
    func=keep_alive,
    args=(None,),
    trigger="interval",
    seconds=10 * 60,
)

# Global variables to store data
data_2024 = []
t_list = {
    "round": [],
    "institute": [],
    "program": [],
    "quota": [],
    "category": [],
}


try:
    with open("dat_2024.json", "r") as json_file_2:
        data_2024 = json.load(json_file_2)

    # Analysis - create sets for unique values
    t_set = {
        "round": set(),
        "institute": set(),
        "program": set(),
        "quota": set(),
        "category": set(),
    }

    for item in data_2024:
        # Cleanup
        item.pop("seat_gender", None)
        item.pop("remark", None)

        # Set Detection
        t_set["round"].add(item["round"])
        t_set["institute"].add(item["institute"])
        t_set["program"].add(item["program"])
        t_set["quota"].add(item["quota"])
        t_set["category"].add(item["category"])

    # Convert sets to lists
    for t in t_set:
        t_list[t] = list(t_set[t])

    print(f"Data loaded successfully. Total records: {len(data_2024)}")

except FileNotFoundError:
    print("Error: dat_2024.json file not found")
except Exception as e:
    print(f"Error loading data: {str(e)}")


def filter_data(
    data: list,
    t_list: dict,
    max_results=25,
    page=1,
    round_l: list = None,
    institute: list = None,
    program: list = None,
    quota: list = None,
    category: list = None,
    rank: int = None,
):
    """Filter data based on provided criteria"""
    results = []

    if round_l is None:
        round_l = t_list["round"]

    if institute is None:
        institute = t_list["institute"]

    if program is None:
        program = t_list["program"]

    if quota is None:
        quota = t_list["quota"]

    if category is None:
        category = t_list["category"]

    for item in data:
        exp = (
            item["round"] in round_l
            and item["institute"] in institute
            and item["program"] in program
            and item["quota"] in quota
            and item["category"] in category
        )

        if rank is not None:
            rank_exp = rank < item["cr"]
        else:
            rank_exp = True

        if exp and rank_exp:
            results.append(item)

    results.sort(key=lambda x: x["cr"], reverse=False)

    # Pagination
    start_index = (page - 1) * max_results
    end_index = start_index + max_results
    paginated_results = results[start_index:end_index]

    return {
        "meta_data": {
            "total_results": len(results),
            "max_results": max_results,
            "current_page": page,
            "total_pages": (len(results) + max_results - 1) // max_results,
        },
        "results": paginated_results,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start")
def start():
    try:
        if scheduler.running:
            return "Scheduler is already running"

        scheduler.modify_job(job_id="aliver", args=(request.host_url,))
        scheduler.start()
        return f"Schedular has started."

    except Exception as e:
        return str(e)


@app.route("/api/data", methods=["POST"])
def get_filtered_data():
    """Main endpoint to get filtered data"""
    try:
        # Get JSON data from request body
        request_data = request.get_json()

        # Handle case where no JSON data is provided
        if request_data is None:
            request_data = {}

        # Get parameters from JSON body with defaults
        max_results = int(request_data.get("max_results", 25))
        page = int(request_data.get("page", 1))
        rank = request_data.get("rank")

        # Get list parameters
        round_l = request_data.get("round")
        institute = request_data.get("institute")
        program = request_data.get("program")
        quota = request_data.get("quota")
        category = request_data.get("category")

        if round_l is not None:
            round_l = [int(r) for r in round_l]

        # Filter data
        data_raw = filter_data(
            data=data_2024,
            t_list=t_list,
            max_results=max_results,
            page=page,
            round_l=round_l,
            institute=institute,
            program=program,
            quota=quota,
            category=category,
            rank=rank,
        )

        # return tabulate(data_raw["results"], width=80, dump=True)

        return jsonify(
            {
                "meta_data": data_raw["meta_data"],
                "results": tabulate(data_raw["results"], width=80, dump=True),
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/filters", methods=["GET"])
def get_available_filters():
    return jsonify(t_list)


@app.route("/res/<path:filename>")
def serve_res_files(filename):
    return send_from_directory("res", filename)


@app.route("/res/")
def list_res_files():

    css = """
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap");
        
        :root {
            --md-sys-color-primary: #d0bcff;
            --md-sys-color-primary-container: #4f378b;
            --md-sys-color-on-primary: #371e73;
            --md-sys-color-on-primary-container: #eaddff;
            --md-sys-color-surface: #10100f;
            --md-sys-color-on-surface: #e6e1e5;
            --md-sys-color-outline: #938f99;
            --md-sys-shape-corner-medium: 12px;
            --md-sys-elevation-level1: 0px 1px 2px 0px rgba(0, 0, 0, 0.3),
                0px 1px 3px 1px rgba(0, 0, 0, 0.15);
        }
        
        body {
            font-family: "Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background-color: var(--md-sys-color-surface);
            color: var(--md-sys-color-on-surface);
            padding: 24px;
            margin: 0;
            line-height: 1.5;
        }
        
        h2 {
            color: var(--md-sys-color-primary);
            font-size: 28px;
            font-weight: 400;
            margin-bottom: 24px;
            margin-top: 0;
        }
        
        a {
            color: var(--md-sys-color-primary);
            text-decoration: none;
            display: inline-block;
            width : 100px;
            margin: 8px 0;
            padding: 12px 16px;
            border-radius: var(--md-sys-shape-corner-medium);
            transition: all 0.2s cubic-bezier(0.2, 0, 0, 1);
            border: 1px solid var(--md-sys-color-outline);
        }
        
        a:hover {
            background-color: var(--md-sys-color-primary-container);
            color: var(--md-sys-color-on-primary-container);
            box-shadow: var(--md-sys-elevation-level1);
        }
    </style>
    """

    files = [f for f in os.listdir("res") if f.endswith(".html")]
    file_links = "".join([f'<a href="/res/{f}">{f[:-5]}</a><br>' for f in files])
    return f"{css}<h2>Institute wise Distribution Sorted by CR :</h2>{file_links}"


@app.route("/res2/<path:filename>")
def serve_res2_files(filename):
    return send_from_directory("res2", filename)


@app.route("/res2/")
def list_res2_files():

    css = """
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap");
        
        :root {
            --md-sys-color-primary: #d0bcff;
            --md-sys-color-primary-container: #4f378b;
            --md-sys-color-on-primary: #371e73;
            --md-sys-color-on-primary-container: #eaddff;
            --md-sys-color-surface: #10100f;
            --md-sys-color-on-surface: #e6e1e5;
            --md-sys-color-outline: #938f99;
            --md-sys-shape-corner-medium: 12px;
            --md-sys-elevation-level1: 0px 1px 2px 0px rgba(0, 0, 0, 0.3),
                0px 1px 3px 1px rgba(0, 0, 0, 0.15);
        }
        
        body {
            font-family: "Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background-color: var(--md-sys-color-surface);
            color: var(--md-sys-color-on-surface);
            padding: 24px;
            margin: 0;
            line-height: 1.5;
        }
        
        h2 {
            color: var(--md-sys-color-primary);
            font-size: 28px;
            font-weight: 400;
            margin-bottom: 24px;
            margin-top: 0;
        }
        
        a {
            color: var(--md-sys-color-primary);
            text-decoration: none;
            display: inline-block;
            width : 100px;
            margin: 8px 0;
            padding: 12px 16px;
            border-radius: var(--md-sys-shape-corner-medium);
            transition: all 0.2s cubic-bezier(0.2, 0, 0, 1);
            border: 1px solid var(--md-sys-color-outline);
        }
        
        a:hover {
            background-color: var(--md-sys-color-primary-container);
            color: var(--md-sys-color-on-primary-container);
            box-shadow: var(--md-sys-elevation-level1);
        }
    </style>
    """

    files = [f for f in os.listdir("res2") if f.endswith(".html")]
    file_links = "".join([f'<a href="/res2/{f}">{f[:-5]}</a><br>' for f in files])
    return f"{css}<h2>Program wise Distribution Sorted by CR :</h2>{file_links}"


if __name__ == "__main__":
    app.run()
