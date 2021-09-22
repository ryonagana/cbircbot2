# CB IRCBot 2.0
a modular bot using python 3.7+
and the sucessor of [cbircbot](https://github.com/ryonagana/cbircbot)

### Dependencies:
- virtualenv (optional)
- ZODB (only if you need User module)
- ZEO Server (fix concurrency problems)
- IPython (ease debugging)
- urllib3 for Weather
- Python Version 3.7+ (can run on 3.6 but not recommended)

###Setup virtualenv
```console
foo@bar:~$ virtualenv --python=python3 venv
foo@bar:~$ source venv/bin/activate
```
### Install Dependencies
```console
(venv)foo@bar:~$ pip install -r requirements.txt 
```
## If dependencies go wrong
```console
(venv)foo@bar:~$ pip install zeo zodb urllib3 ipython tornado  
```

### After Setup:
    you need to create a fresh Database file
    go to cli/ folder and execute db_utils.py

```console
foo@bar:~$ python3 db_utils.py
```
- Choose option 1 - Create a Fresh Database
- then you need ZEO server running


```console
foo@bar:~$ ./run_zeo.sh
```


### Edit file run.sh 

```console
foo@bar:~$ cp run.sh_skel run.sh
```

```console
foo@bar:~$ vim run.sh
```

# Run
```console
foo@bar:~$ ./run.sh
```
