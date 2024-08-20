# AD_HON: sequence anomaly detection based on higher-order networks


This repository provides the implementation of HON for EHR sequences. 


## Env setup
This code requires the packages listed in requirements.txt.
An virtual environment is recommended to run this code

On macOS and Linux:  

```
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip install -r ./environment/requirements.txt
deactivate
```

Reference: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

An alternative is to create a conda environment:

```

    conda create -f ./environment/environment.yml
    conda activate adhon
```

Reference: https://docs.conda.io/en/latest/miniconda.html

## Experiment
The detail of the methods are proposed in the following papers:
- [Anomaly Detection in Sequential Health Care Data using Higher-Order Network Representation](https://www.osti.gov/biblio/1649358)
- [Adaptive Anomaly Detection for Dynamic Clinical Event Sequences](https://ieeexplore.ieee.org/abstract/document/9378080)

### Data sample

Data sample has been provided for testing under directory: './data/sample.csv'.

### Example
```shell script
# Build higher order network
cd Tensor_HON
python TensorHON.py

# visualize network
python VisualGraph.py # detect abnormal sequences
```