Example of using Flask to connect html and python.
==================================================


This program is fairly simple, we have a database in our python side (its actually a dictionary ... bear with me).
And it generates an html that dynamically changes the options once is selected.

.. image:: sample.gif
   :align: center

This was more of a learning exercise for me (which took some sweet time ...) but since it was done ...
why not document it a little better and publish it.

Here is a little explaination of the flow of data that happens (using the amazing mermaid.js)

.. image:: diagram.mermaid.png
   :align: center


How to run
----------

.. code:: shell

    git clone https://github.com/jspaezp/flask-db-sample
    pip install Flask
    set FLASK_APP=views.py
    set FLASK_DEBUG=1
    flask run

