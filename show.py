from flask import jsonify, render_template, request, Flask
from networkx.readwrite import json_graph
from pymotifcluster.clusterwindow import shuffle_sequence, nmer_knn, knn_to_graph
import re



app = Flask(__name__)

# DUMMY database

database = {'Opt1': [1, 2, 3, 4, 5],
            'Opt2': [10, 20, 30, 40]}


@app.context_processor
def inject_database():
    """ Exposes the database file so it can be read in the html templates """
    return dict(database=database)
    # TODO make this the backend to add the default network data


@app.route('/')
def base():
    """ Exposes the base html after rendering the template """
    return render_template('base.html', database=database)


def parseSequences(string):
    sequences = [x.strip() for x in string.split('\n')]
    validsequences = re.compile(r'[ACDEFGHIKLMNPQRSTVWY]').search

    if len(sequences) < 2:
            return(sequences[0])

    assert all([bool(validsequences(seq)) for seq in sequences]), \
        ("Not all chacters provided are suported"
         " in the current distance metric (not aminoacids)")
    return sequences

# Tests that it actually throws an error when encountering unsupported chars
# And not otherwise
def test_parseSequences():
    with pytest.raises(AssertionError):
        parseSequences("OOOJOJO\n OOJOJO")

    parseSequences("")


@app.route('/getNetwork', methods=['POST'])
def getNetwork():
    fg = parseSequences(request.form.get('foregroundSequences'))
    bg = request.form.get('backgroundSequences')
    nn = int(request.form.get('NN'))
    ns = int(request.form.get('NmerSize'))
    nd = int(request.form.get('NmerSize'))
    ad = request.form.get('decoys')

    jsonobj = clus_windows(
        fg_sequence=fg, bg_sequences=bg,
        nmer_size=ns, k=nn,
        ndecoys=nd, adddecoys=ad)
    return render_template('netwokonly.html', jsonobj=jsonobj)
    # return jsonify('got it')


def clus_windows(fg_sequence, bg_sequences, nmer_size, k, ndecoys, adddecoys):
    sequences = []
    group = []

    sequences.extend(fg_sequence)
    group.extend(['fg']*len(fg_sequence))

    if adddecoys == 'True':
        # This is requred because the form submits the word True instread of
        # the bool value
        decoys = [shuffle_sequence(x) for x in fg_sequence*ndecoys]
        sequences.extend(decoys)
        group.extend(['decoys']*len(decoys))

    if bg_sequences and bg_sequences[0] is not '':
        sequences.extend(bg_sequences)
        group.extend(['bg']*len(fg_sequence))

    foo = nmer_knn(sequences, nmer_size=nmer_size, k=k)
    G = knn_to_graph(foo, sequences)
    G.add_nodes_from([x for x, y in enumerate(group) if y == 'fg'], group=1)
    G.add_nodes_from([x for x, y in enumerate(group) if y == 'decoys'], group=2)
    G.add_nodes_from([x for x, y in enumerate(group) if y == 'bg'], group=3)

    return json_graph.node_link_data(G)


if __name__ == "__main__":
    app.run()
