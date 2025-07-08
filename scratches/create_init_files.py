import csv
import json

from pathlib import Path

from classify_neurons.utils import mk_time_stamp_str, write_json

root = Path(r"C:\Data\EM\DATA")

sorting_fn = root.joinpath("HumanNeuronClassification/SortingCells.csv")
with open(sorting_fn, 'r') as file:
    reader = csv.DictReader(file)
    sorting_data = [row for row in reader]

dl = []
pl = []
gl = []
pn = []
excluded = []
for row in sorting_data:
    if float(row['too_cut']) > 0:
        excluded.append(int(row['segment_id']))
    if int(row['deep']):
        dl.append(int(row['segment_id']))
    elif int(row['pl']):
        pl.append(int(row['segment_id']))
    elif int(row['gl']):
        gl.append(int(row['segment_id']))
    elif row['pn']:
        pn.append(int(row['segment_id']))

IN_fn = root.joinpath("HumanNeuronClassification", 'debug','IN', f'{mk_time_stamp_str()}_neuron_classification.json')
data = {str(i-1): seg for i, seg in enumerate([dl, pl, gl])}
write_json(data, IN_fn)

IN_fn = root.joinpath("HumanNeuronClassification", 'debug','PN', f'{mk_time_stamp_str()}_neuron_classification.json')
data = {str(-1): pn}
write_json(data, IN_fn)