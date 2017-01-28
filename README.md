SIStema
=======

Web service for easy Summer Informatic School creation

Most relevant issues are [here](https://github.com/andgein/SIStema/milestone/2)

## Install

    $ git clone git@github.com:andgein/SIStema.git
    $ cd SIStema/
    $ virtualenv -p python3 venv
    $ source ./venv/bin/activate
    $ sudo apt install libmysqlclient-dev
    $ pip install -Ur src/requirements.txt

Ask someone to make you a database dump of the main SIStema instance:

    $ python src/web/manage.py dumpdata > db.json

Then load it locally:

    $ python src/web/manage.py loaddata db.json
