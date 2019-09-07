import random
from flask import Flask, jsonify, request
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
Swagger(app)

@app.route('/api/<string:language>/', methods=['GET'])
@swag_from('index.yml')
def index(language):

    # try:
    #     validate(data, 'awesome', 'index.yml', root=__file__)
    # except ValidationError as e:
    #     return "Validation Error: %s" % e, 400

    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic",
        "simple", "powerful", "amazing",
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )


app.run(debug=True)