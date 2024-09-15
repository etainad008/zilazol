from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from get_cerberus_data import get_chain_prices, CERBERUS_CHAINS
from process_cerberus_data import prices_to_dict
from db import get_unique_names

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

@app.route('/api/prices', methods=['GET'])
def get_prices():
    chain = request.args.get("chain", None)
    amount = request.args.get("amount", "1")

    if not chain or chain not in CERBERUS_CHAINS.keys():
        abort(400, description="Invalid chain")

    if not amount.isdigit():
        abort(400, description="Amount must be a number")

    amount = int(amount)
    if amount < 1:
        abort(400, description="Amount equal or greater than 1")

    names = get_unique_names(
        [prices_to_dict(prices) for chain_name in CERBERUS_CHAINS.keys() for prices in get_chain_prices(chain_name, 1)],
        10
    )

    res = jsonify(names)

    # allow CORS
    res.headers.add('Access-Control-Allow-Origin', '*')
    res.headers.add('Access-Control-Allow-Methods', 'GET')
    res.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    res.headers.add('Access-Control-Allow-Credentials', 'true')

    return res


if __name__ == '__main__':
    app.run(debug=True)
