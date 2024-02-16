# aktos_take_home
A take home assignment by Aktos

Video walkthrough.
 - [PART ONE](https://www.loom.com/share/5c7b96dcdc3b4f12a3315f5ad1657307?sid=2b3d0ab6-23cf-4b37-ab75-3a5de38b9fa3)
  - [PART TWO](https://www.loom.com/share/9fe1f336acdd4995937e2b97aa0e5626?sid=ee875e5a-2cfc-4d91-9600-e75b63511d61)


[![Aktos API Pylint](https://github.com/Iamdavidonuh/aktos_take_home/actions/workflows/pylint.yaml/badge.svg)](https://github.com/Iamdavidonuh/aktos_take_home/actions/workflows/pylint.yaml)
[![Aktos API tests](https://github.com/Iamdavidonuh/aktos_take_home/actions/workflows/test.yaml/badge.svg)](https://github.com/Iamdavidonuh/aktos_take_home/actions/workflows/test.yaml)

## Sections
- [Aktos Take Home](#aktos_take_home)
  - [Installation](#installation)
    - [Without Docker](#setup-without-docker)
    - [Using Docker](#setup-with-docker)
  - [Running the tests](#running-the-tests)
  - [Loading Consumer data](#loading-consumer-data)
  - [API Endpoint](#api)
  - [Notes](#notes)
    - [Assumptions and Considerations](#assumptions-and-cosiderations)
    - [Pagination](#pagination)



## Installation

#### Clone the repo


```bash
git clone https://github.com/Iamdavidonuh/aktos_take_home.git
```
#### Configure Settings

- Copy the settings file

    ```bash
    cp aktos_take_home/aktos/settings/default.py aktos_take_home/aktos/settings/local_settings.py
    ```

    

### Setup Without Docker

#### Poetry Dependency Manager
* Install and Configure Poetry
    ```bash
    curl -sSL https://install.python-poetry.org | python3 - --version 1.7.0
    ```
* Disable virutalenv creation by default
    ```bash
    poetry config virtualenvs.create false 
    ```

#### Creating a virutal environment

```bash
pip3 install virtualenv
```

- Setup virtual environment

    ```bash
    virtualenv -p python3.11 .virtualenv
    ```

- Activate virutalenv

    ```bash
    source .virtualenv/bin/activate
    ```

- Install requirements

    ```bash
    poetry install
    ```
#### Run migrations before starting the server

```python
python manage.py migrate
```


### Setup With Docker

- Start up 
```bash
 make up
```

- Using production settings
    - In project root, create .env file from .env.example file
    ```bash
    cp .env.example .env
    ```
    - update settings as needed


## Running the tests
- ```bash
    python manage.py test
    ```

## Loading Consumer data
Loading csv data into the database can be down via two methods, django commands and api endpoint.
- Using django commands: use the `python manage.py load_consumers --path "path_to_csv_file"`

    Example: while in root dir
    
    ```bash
    python manage.py load_consumers --path ./collector/fixtures/data/consumers_balances.csv
    ```

- Using API endpoint: Send a post request to `api/upload-consumers`. Visit Swagger docs for more info

## API Endpoint
- Swagger docs can be found at: `127.0.0.1:8000/docs/swagger`
- Deployed at: http://34.125.127.214/docs/swagger 
    
    Note: The database on prod is clean, you'd have to upload csv via the `upload-consumers` endpoint to get data

## Notes

### ASSUMPTIONS AND CONSIDERATIONS
- Since no information was provided, it is assumed that `client_reference_no` is unqiue, so the system regenerates a new `ID` for you.

- Duplicates: i considered the possibility of duplicate data and how to handle them. I chose to ignore them and a record will be considered duplicate when:  `client_ref_no` and other fields (`balance, status, consumer name, consumer address, ssn`) matches.

### PAGINATION
I Chose `CursorPagination`
It provides a cursor (usually an encoded value representing the last seen record) is used to fetch the next set of results. I went with this choice because the records on this database can easily grow and become very large, hence the need for a faster type of pagination


#### PROS:
- Suitable for large datasets where the total number of records is unknown or potentially very large.
- Provides more predictable performance, especially with large datasets, as it avoids the need to skip records.
- Better scalability since it doesn't rely on offset calculations, making it suitable for databases with large numbers of records.
- Ensures consistent results even if data is inserted or deleted during pagination.

#### CONS:
- Complexity: Implementing cursor-based pagination can be more complex than other pagination methods, especially when dealing with more complex querysets or relationships between models.

- Limited usability: CursorPagination is most suitable for ordered querysets, where each record can be uniquely identified by a cursor.

- Less intuitive: The concept of cursors may be less intuitive, especially to those who are more familiar with traditional page-based pagination.

- Cursor stability: Cursors are sensitive to changes in the underlying dataset. If records are added, deleted, or modified between paginated requests, it can potentially lead to unexpected results or duplicates.