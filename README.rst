Using flask to give a gui to my peptide clustering package
==========================================================


This program is fairly simple, given the set of peptides and the parameters, it 
calls the clustering package internally and returns a json with the network of 
the clustered peptides, which is then visualized using D3.js

This was more of a learning exercise for me (which took some sweet time ...) 

Here is a little explaination of the flow of data that happens (using the amazing mermaid.js)

.. image:: diagram.mermaid.png
   :align: center

How to run
----------

.. code:: shell

    # It requires having the clustering package installed... 
    # For instructions on that go to ...
    # 

    git clone https://github.com/jspaezp/flask-db-sample
    set FLASK_DEBUG=1 # optional ....
    python3 ./show.py

TODO
====

- Curently there is a bug where newlines make the query crash


