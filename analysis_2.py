import json
import os
from tabulator import tabulate

with open("dat_2024.json", "r") as json_file:
    data_2024 = json.load(json_file)

category_set = set()

for dat in data_2024:
    category_set.add(dat["category"])

print(category_set)


def _gen_html(cat_fil):

    current = []

    for dat in data_2024:

        if cat_fil == dat["category"]:
            current.append(dat)

    current.sort(key=lambda x: x["cr"], reverse=False)

    courses = {}
    seen_colleges = []

    for curr in current:
        institute_name = curr["institute"]
        if institute_name not in seen_colleges:
            seen_colleges.append(institute_name)
            courses[institute_name] = {}

        courses[institute_name][curr["program"]] = {
            "cr": curr["cr"],
            "round": curr["round"],
        }

    data = []

    for institute_name in courses:
        programs = courses[institute_name]
        for program_name in programs:
            data.append(
                {
                    "institute": institute_name,
                    "program": program_name,
                    "cr": programs[program_name]["cr"],
                    "round": programs[program_name]["round"],
                }
            )

    data.sort(key=lambda x: x["cr"], reverse=False)

    datax = tabulate(data, dump=True, width=75)

    os.makedirs("res2", exist_ok=True)
    with open(f"res2/{cat_fil}.html", "w") as fl:
        fl.write(f"<pre>{datax}\n{'github.com/git-divy'}</pre>")


def generate_res2_files():
    for cat in category_set:
        _gen_html(cat_fil=cat)
    print(len(category_set), "res2 files generated.")
