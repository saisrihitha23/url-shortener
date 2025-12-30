from flask import Flask, request, redirect, jsonify
from datetime import datetime, timedelta
import hashlib
import string
import random

app = Flask(__name__)

# In-memory storage (replace with DB in production)
url_store = {}

def generate_hash(url):
    """Generate deterministic hash-based short id"""
    return hashlib.md5(url.encode()).hexdigest()[:6]

def random_alias(length=6):
    """Fallback random alias generator"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def is_expired(entry):
    return entry["expires_at"] and datetime.utcnow() > entry["expires_at"]

@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "url is required"}), 400

    original_url = data["url"].strip()
    custom_alias = data.get("alias")
    ttl_minutes = data.get("ttl")   # optional expiration time

    # Generate alias
    short_id = custom_alias or generate_hash(original_url)

    # Avoid overwriting other URLs if alias already exists
    if short_id in url_store and url_store[short_id]["url"] != original_url:
        return jsonify({"error": "alias already in use"}), 409

    expires_at = None
    if ttl_minutes:
        expires_at = datetime.utcnow() + timedelta(minutes=int(ttl_minutes))

    url_store[short_id] = {
                "url": original_url,
                "created_at": datetime.utcnow(),
                "expires_at": expires_at,
                "clicks": 0,
                "last_accessed": None
            }

    return jsonify({
        "short_url": f"/{short_id}",
        "alias": short_id,
        "expires_at": expires_at.isoformat() if expires_at else None
    })

@app.route("/<short_id>")
def redirect_url(short_id):
    entry = url_store.get(short_id)

    if not entry:
        return jsonify({"error": "short url not found"}), 404

    if is_expired(entry):
        return jsonify({"error": "link has expired"}), 410

    entry["clicks"] += 1
    entry["last_accessed"] = datetime.utcnow()

    return redirect(entry["url"], code=302)

@app.route("/stats/<short_id>")
def stats(short_id):
    entry = url_store.get(short_id)

    if not entry:
        return jsonify({"error": "short url not found"}), 404

    return jsonify({
        "url": entry["url"],
        "created_at": entry["created_at"].isoformat(),
        "expires_at": entry["expires_at"].isoformat() if entry["expires_at"] else None,
        "clicks": entry["clicks"],
        "last_accessed": entry["last_accessed"].isoformat() if entry["last_accessed"] else None
    })

if __name__ == "__main__":
    app.run(debug=True)
