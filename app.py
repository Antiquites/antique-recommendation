import flask
from flask import request, jsonify
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
original = pd.read_csv('arts_crafts3.csv')

# set first column to index
df = pd.read_csv('arts_crafts_result.csv', index_col=0)
# set columns and index names
df.columns.name = df.index.name
df.index.name = df.index[0]
# remove first row of data
df = df.iloc[1:]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/antique/api/user', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        userId = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    # check if user exists
    if userId not in original['userId'].values:
        return 'user not found', 404

    # get already purchased, rated items
    rated = original[original['userId'] == userId]['title'].to_list()

    # get recommended items for users by sorting items Descending by rating
    recommended = df.loc[userId].sort_values(ascending=False).index

    # filter the recommended items and remove already rated items
    recommended_filtered = [i for i in recommended if i not in rated][:3]

    # return filtered recommendation
    return jsonify(recommended_filtered)


app.run()
