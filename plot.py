import sys
import json
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def generate_plot(data):
    plot_type = data["plotVariables"]["type"].lower()
    plot_height = data["plotVariables"]["plotHeight"]
    plot_width = data["plotVariables"]["plotWidth"]
    title = data["plotVariables"]["title"]
    background_color = data["plotVariables"]["backgroundColor"] or "white"
    line_color = data["plotVariables"]["lineColor"] or "blue"
    text_color = data["plotVariables"]["textColor"] or "black"
    x_title = data["plotVariables"]["xTitle"]
    y_title = data["plotVariables"]["yTitle"]

    months = [item["month"] for item in data["data"]]
    temps = [int(item["temp"]) for item in data["data"]]

    if plot_height and plot_width:
        plt.figure(figsize=(int(plot_width), int(plot_height)))

    if plot_type == "line" or plot_type == "area":
        plt.plot(months, temps, color=line_color)
        if plot_type == "area":
            plt.fill_between(months, temps, color="skyblue", alpha=0.3)
    elif plot_type == "bar":
        plt.bar(months, temps, color=line_color)

    plt.title(title, color=text_color)
    plt.xlabel(x_title, color=text_color)
    plt.ylabel(y_title, color=text_color)
    plt.gca().set_facecolor(background_color)

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()

    return img_str


if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    base64_image = generate_plot(input_data)
    print(base64_image)