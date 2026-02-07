import json
from importlib.resources import files


def load_template():
    return files("taxa_viz").joinpath("template.html")


def render_html(data_1, data_0_5, data_0_1, output, list=[]):
    data_1 = json.dumps(data_1, indent=2)
    data_0_5 = json.dumps(data_0_5, indent=2)
    data_0_1 = json.dumps(data_0_1, indent=2)

    with open(load_template(), "r", encoding="utf-8") as f:
        html = f.read()
        # print(html)
    html = html.replace("{{DATA_1}}", data_1)
    html = html.replace("{{DATA_0.5}}", data_0_5)
    html = html.replace("{{DATA_0.1}}", data_0_1)
    html = html.replace("{{PATH}}", str(list))

    with open(output, "w") as f:
        f.write(html)
