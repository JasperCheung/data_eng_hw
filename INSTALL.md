To run this project:
## Docker
1. Start the docker container by using `docker-compose up --build -d`
    - This will build the image, start the container in the background, and the container should contain three tables: users, initial, and marketing
## Python Setup 
** Note ** you can just skip the virtualenv if you have the packages downloaded globally.
1.  Make sure you have Python3 and associated tools installed:
    ```shell
    python3 --version
    pip3 --version
    virtualenv --version
    ```

2.  Create a virtualenv from the top level `numina-graph` directory: `virtualenv -p python3 {envname}`

3.  Activate the virtualenv: `source {envname}/bin/activate`.

4.  Install the project Python requirements: `pip install -r requirements.txt`

## Loading the data and grabbing the answers
1. to load the data in the database run `python load_data.py`
    -  ** Notes **: running load data clears the tables everytime before populating, also you can delete all the files in the `clean` directory to test what happens in a intial state.
2. to get the answers run `python answers.py`
