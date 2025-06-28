from flask import Flask, jsonify, request
from pytrends.request import TrendReq
import os

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

# Mapping ISO country codes to pytrends supported region slugs
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

    if geo not in valid_regions:
        return jsonify({
            "error": f"Region '{geo}' is not supported. Choose from: {list(valid_regions.keys())}"
        }), 400

    region = valid_regions[geo]

    try:
        trending_searches = pytrends.trending_searches(pn=region)
        keywords = trending_searches[0].tolist()
        return jsonify({
            "geo": geo,
            "region": region,
            "trending_keywords": keywords
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
