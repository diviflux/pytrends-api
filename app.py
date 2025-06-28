from flask import Flask, jsonify, request
from pytrends.request import TrendReq
import os

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

# ISO to pytrends region map
valid_regions = {
    'US': 'united_states',
    'IN': 'india',
    'JP': 'japan',
    'GB': 'united_kingdom',
    'DE': 'germany',
    'FR': 'france',
    'BR': 'brazil',
    'AU': 'australia',
    'CA': 'canada'
}

@app.route('/')
def home():
    return jsonify({"status": "running"})

@app.route('/trending', methods=['GET'])
def get_trending():
    geo = request.args.get('geo', default='US').upper()
    region = valid_regions.get(geo, 'united_states')
    try:
        df = pytrends.trending_searches(pn=region)
        keywords = df[0].tolist()
        return jsonify({"geo": geo, "region": region, "trending_keywords": keywords})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
