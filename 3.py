''' data = { id: {
                  name:{
                        'identity': 'alignment'
                        }
                 }
            }



'''


import re
input_file = "marvel_dc_characters.csv"
import plotly
import plotly.graph_objs as go
import pprint



def parse_id(v):
    if not re.match(r"\d{6}", v):
        raise ValueError("'ID' must be a number with 6 digits")
    return int(v)

def parse_name(v):
    if not re.match(r".*", v):
        raise ValueError("'Name' must be a string")
    return v

def parse_identity(v):
    if not re.match(r"(Secret)|(Public)", v):
        raise ValueError("'Identity' must be a string 'Secret' or 'Public'")
    return v

def parse_alignment(v):
    if not re.match(r"(Neutral)|(Good)|(Bad)", v):
        raise ValueError("'Identity' must be a string 'Neutral' or 'Good' or 'Bad'")
    return v


data = dict()


def main():
    current_line = 0
    with open(input_file, mode="r", encoding="utf-8") as file:
        header = [col.strip().upper() for col in file.readline().strip().split(",")]
        print(header)
        for line in file:
            try:
                current_line += 1
                if not line.strip() == "":
                    new_line = re.split(r",", line, 1)
                    id = parse_id(new_line[0])
                    new_line = re.split(r",", new_line[1], 1)
                    name = parse_name(new_line[0])
                    new_line = re.split(r",", new_line[1], 1)
                    identity = parse_identity(new_line[0])
                    new_line = re.split(r",", new_line[1], 1)
                    alignment = parse_alignment(new_line[0])
                    if id not in data:
                        data[id] = dict()
                    if name not in data[id]:
                        data[id][name] = dict()
                    if identity not in data[id][name]:
                        data[id][name][identity] = dict()
                    data[id][name][identity] = alignment
            except ValueError as err:
                print("Error in line {0}: {1}!".format(current_line, err.args[0]))
main()


pprint.pprint(data)

z = 0
q = 0
r = 0

for id in data:
    for name in data[id]:
        for identity in data[id][name]:
            if data[id][name][identity] == 'Bad':
                z += 1
            elif data[id][name][identity] == 'Good':
                q += 1
            elif data[id][name][identity] == 'Neutral':
                r += 1

list1 = []
list1.append(z)
list1.append(q)
list1.append(r)

figure = { "data" : [
        {
            "x": ['Bad', 'Good', 'Neutral'],
            "y": list1,
            "type": "scatter",
            "name": "P1",
        },
        {
            "x": ['Bad', 'Good', 'Neutral'],
            "y": list1,
            "type": "bar",
            "name": "P1",
            "xaxis": "x2",
            "yaxis": "y2"
        },
        {
            "labels": ['Bad', 'Good', 'Neutral'],
            "values": list1,
            "type": "pie",
            "name": "P2",
            'domain': {'x': [0, 0.45], 'y': [0.55, 1]},
        }
    ],
    "layout" : go.Layout(
            xaxis=dict(domain=[0, 0.45]), yaxis=dict(domain=[0, 0.45]),
            xaxis2=dict(domain=[0.55, 1]), yaxis2=dict(domain=[0, 0.45], anchor='x2'))}
plotly.offline.plot(figure, filename="plot.html")

