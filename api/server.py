from flask import Flask, jsonify, request, abort
from get_cerberus_data import get_chain_prices, CERBERUS_CHAINS

app = Flask(__name__)

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

    data = get_chain_prices(chain=chain, amount=amount)
    res = jsonify(data)

    # allow CORS
    res.headers.add('Access-Control-Allow-Origin', '*')
    res.headers.add('Access-Control-Allow-Methods', 'GET')
    res.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    res.headers.add('Access-Control-Allow-Credentials', 'true')

    return res


if __name__ == '__main__':
    app.run(debug=True)
