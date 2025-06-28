from flask import Flask, jsonify, request
from pytrends.request import TrendReq

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

@app.route('/')
def home():
    return jsonify({"status": "running"})

@app.route('/trending', methods=['GET'])
def get_trending():
    geo = request.args.get('geo', default='US')  # e.g., 'IN' for India, 'US', 'GB', etc.
    try:
        trending_searches = pytrends.trending_searches(pn=geo)
        keywords = trending_searches[0].tolist()
        return jsonify({"geo": geo, "trending_keywords": keywords})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
