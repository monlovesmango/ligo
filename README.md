# create virtual environment
```
python3 -m venv .venv
```
```
source .venv/bin/activate
```

# install dependencies
```
pip install -r ./requirements.txt 
```

# load gwplot.py
``` 
python -i gwplot.py```

```

# start it up
```
fetch_data()
set_time_limits()
plot_data()
```

# delete saved data
to delete timeseries data that has been saved delete the file `src/data.txt`