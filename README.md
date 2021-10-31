# CB Bot for IRC 2.0
#### a modular bot using python 3.8+
an IRC Bot runs using multiprocessing power

### Dependencies:
- virtualenv (optional, avoid mix packages)
- ZODB (only if you need User module with DB)
- ZEO Server (fix concurrency problems for ZODB)
- IPython (ease debugging, optional)
- urllib3 for Weather (required if weather module is active)
- BeautifulSoup 4 (required if title module is active)

#### Please use Python 3.8+

### Setup virtualenv
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
(venv)foo@bar:~$ pip install zeo zodb urllib3 ipython tornado requests bs4
```

### After Setup:
    you need to create a fresh Database file
    go to cli/ folder and execute db_utils.py
```console
foo@bar:~$ cd <root dir>/cli/
foo@bar:~$ python3 db_utils
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
