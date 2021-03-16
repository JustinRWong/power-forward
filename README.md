# Power Forward

## Starting the Virtual Environment

Follow this as a reference: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/


To get started with running the venv for Power Forward, run the following command:
```
virtualenv power-forward-app-env
source power-forward-app-env/bin/activate
pip install -r requirements.txt
chmod +x start_local.sh
./start_local.sh
```


## Starting the app

### Locally
```
source power-forward-app-env/bin/activate

ls
Procfile		__pycache__		power-forward-app-env	src			static
README.md		app.py			requirements.txt	start_local.sh		templates

pip install requirements.txt

./start_local.sh
```

### Live (Production)
Visit http://power-forward.herokuapp.com/
