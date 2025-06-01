from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import uuid
import time

app = Flask(__name__)
CORS(app, origins=["https://mchmgwtg.manus.space"], supports_credentials=True )

# In-memory storage for podcasts and users
podcasts = {}
users = {}

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to AI-Generated Podcast Club API",
        "status": "running"
    })

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 204
    
    data = request.json
    user_id = str(uuid.uuid4())
    new_user = {
        "id": user_id,
        "username": data.get('username', ''),
        "email": data.get('email', '')
    }
    users[data.get('username', '')] = new_user
    
    return jsonify({
        "message": "Registration successful",
        "user": new_user,
        "token": f"demo-jwt-token-{user_id}"
    }), 201

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 204
    
    data = request.json
    username = data.get('username', '')
    
    if username in users:
        user = users[username]
    else:
        # Demo mode - create user if not exists
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "username": username,
            "email": f"{username}@example.com"
        }
        users[username] = user
    
    return jsonify({
        "message": "Login successful",
        "user": user,
        "token": f"demo-jwt-token-{user['id']}"
    }), 200

@app.route('/api/podcasts/demo', methods=['GET'])
def get_demo_podcasts():
    return jsonify({
        "podcasts": [
            {
                "id": 1,
                "title": "The Future of AI",
                "description": "Exploring the latest developments in artificial intelligence",
                "topic": "Artificial Intelligence",
                "tone": "educational",
                "duration": 600,
                "status": "completed",
                "created_at": "2025-05-21T10:00:00",
                "audio_url": "/api/podcasts/1/audio"
            },
            {
                "id": 2,
                "title": "Space Exploration in 2025",
                "description": "The latest missions and discoveries in space",
                "topic": "Space Exploration",
                "tone": "exciting",
                "duration": 900,
                "status": "completed",
                "created_at": "2025-05-20T15:30:00",
                "audio_url": "/api/podcasts/2/audio"
            }
        ]
    })

@app.route('/api/podcasts', methods=['GET'])
def get_podcasts():
    return jsonify({
        "podcasts": list(podcasts.values()) + get_demo_podcasts().json["podcasts"]
    })

@app.route('/api/podcasts', methods=['POST'])
def create_podcast():
    data = request.json
    podcast_id = str(uuid.uuid4())
    new_podcast = {
        "id": podcast_id,
        "title": data.get('title', f"Podcast about {data.get('topic', 'Technology')}"),
        "description": data.get('description', ''),
        "topic": data.get('topic', 'Technology'),
        "tone": data.get('tone', 'conversational'),
        "duration": int(data.get('duration', 10)) * 60,
        "status": "completed",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "audio_url": f"/api/podcasts/{podcast_id}/audio"
    }
    podcasts[podcast_id] = new_podcast
    
    return jsonify({
        "message": "Podcast created successfully",
        "podcast": new_podcast
    }), 201

@app.route('/api/podcasts/<podcast_id>', methods=['GET'])
def get_podcast(podcast_id):
    if podcast_id in podcasts:
        return jsonify(podcasts[podcast_id])
    elif podcast_id.isdigit() and int(podcast_id) <= 2:
        demo_podcasts = get_demo_podcasts().json["podcasts"]
        return jsonify(demo_podcasts[int(podcast_id) - 1])
    else:
        return jsonify({"error": "Podcast not found"}), 404

@app.route('/api/podcasts/<podcast_id>/audio', methods=['GET'])
def get_podcast_audio(podcast_id):
    return jsonify({"message": "Audio stream would be here"}), 200
