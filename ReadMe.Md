# Simple Data Exporter from SAP HANA

This is my first project in Python attempting to get data from our SAP HANA Database using the [hdbcli](https://pypi.org/project/hdbcli/)  to connect to our SAP HANA instance.

The script can be configured with a `.env` file to support default server & port arguments, to feed `argpase`
```yaml
SERVER={$SERVER}
PORT={$PORT}
```


```python
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server" , help = "Server URL",default=default_url, dest = "server", type=str)
parser.add_argument("-p", "--port" , help = "Port",default=default_port, dest = "port")
parser.add_argument("-u", "--username", help = "Username", dest = "username", type=str)
parser.add_argument("-P","--Password", help = "Password", dest = "password")
args = parser.parse_args()
```
Additionally the `main()` function can be configured with the variables to automatically log in.
```python
    server = ""
    port = ""
    user_name = ""
    password = ""
```

The function also leverages the ability to read the query from an input file, or to manually enter a query. Lastly, the data can be printed to the console or written to `.csv`.