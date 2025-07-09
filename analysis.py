import json
import os

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

    datax = ""
    datax += (
        "\n----------------------------------------------------------------------------------------------------------------\n"
    ) + "\n"
    for i, cour in enumerate(courses):
        datax += (f"[{str(i+1)}]" + " " + cour + "") + "\n"

        for prog in courses[cour]:
            ix = courses[cour][prog]
            datax += (
                "\t- "
                + prog
                + f"\n\t  {cat_fil} -> CR : "
                + str(ix["cr"])
                + " | ROUND : "
                + str(ix["round"])
            ) + "\n\n"
        datax += (
            "\n----------------------------------------------------------------------------------------------------------------\n"
        ) + "\n"

    note = f"""
    Note: This data is not 100% accurate. 
    A Institue may be ranked higher in this list if a student with lower rank has taken a college/program which generally closes at much higher rank. (or=cr)
    """
    os.makedirs("res", exist_ok=True)
    with open(f"res/{cat_fil}.html", "w") as fl:
        fl.write(f"<pre>{note}\n{datax}\n{'github.com/git-divy'}</pre>")


def generate_res_files():
    for cat in category_set:
        _gen_html(cat_fil=cat)
    print(len(category_set), "res files generated.")
