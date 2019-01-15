# Installation Process

First of all, you need to follow the commands described in this [Dockerfile](https://github.com/Vectorscient/vectorscient_toolkit/blob/master/Dockerfile).
You need to install the `vskit` package and _all_ its requirements, including `NLTK` and `jenks`.
Then you need to create a configuration file with extension like this one:
```
[database]
username=vectorscient
password=vectorscient456
host=104.154.252.194
engine=mysql

[domain]
host=vantenta.com

[data]
root=%(HOME)s/transfer/vskit_legacy/data
nltk=%(NLTK_DATA_PATH)s
location_db=%(root)s/ipdata.bin

[febrl]
python=
script=
mode=link
config=

[analytics]
proto_scheme=https
module=API
method=Live.getLastVisitsDetails
period=day
format=JSON

[sentiment]
default=Simple

[sentry]
dsn=https://b22d455173454927a6193856f5b461d3:50dc67bd1eb24c3db9f67e60f52a8fb9@sentry.vantena.com/4

[gcloud]
bq_private_key=%(GOOGLE_APPLICATION_CREDENTIALS)s

[debug]
test_run=true
patch_ip_address=true
```
You can put it into `/usr/local/etc/vskit.cfg`. Then, you'll need to setup a couple of environment variables (put then into `~/.bashrc`, for example):
```
export VS_CONFIG_PATH="/usr/local/etc/vskit.cfg"
export GOOGLE_APPLICATION_CREDENTIALS="/home/vantena/transfer/creds/bq.json"
export NLTK_DATA_PATH="/home/vantena/nltk_data"
```
After these steps, the CLV code should be ready and you can invoke the following command:
```
(venv) $ python -m vskit --drop-if-exists --create-if-not-exists clv --output-dataset <DATASET> --output-table <TABLE> 
``` 

Finally, you need to setup a Jupyter notebook with Surefit clustering process implementation from [this repo](https://github.com/devforfu/surefit_clustering).
For this purpose, setup additional dependencies at first:
```
$ source activate ./venv
$ conda install -p venv/ nb_conda
$ pip install ipython
```

Then follow this guide to setup [the notebook](http://jupyter-notebook.readthedocs.io/en/stable/public_server.html) and its password on the server. 
After these steps completed, you should be able to navigate into notebook's URL, enter the password and 
invoke one cell after another pressing `Shift + Enter`.  
