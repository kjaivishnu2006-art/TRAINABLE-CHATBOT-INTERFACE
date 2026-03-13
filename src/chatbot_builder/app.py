"""
Flask API for Trainable ChatBot Builder
Provides REST endpoints for managing chatbot training data
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
class Config:
    """Flask configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///chatbot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# ===============================================
# Database Models
# ===============================================

class ChatBot(db.Model):
    """ChatBot project model"""
    __tablename__ = 'chatbots'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_trained = db.Column(db.Boolean, default=False)
    
    # Relationships
    intents = db.relationship('Intent', backref='chatbot', lazy=True, cascade='all, delete-orphan')
    entities = db.relationship('Entity', backref='chatbot', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'language': self.language,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_trained': self.is_trained,
            'intent_count': len(self.intents),
            'entity_count': len(self.entities)
        }


class Intent(db.Model):
    """Intent model"""
    __tablename__ = 'intents'
    
    id = db.Column(db.Integer, primary_key=True)
    chatbot_id = db.Column(db.Integer, db.ForeignKey('chatbots.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    utterances = db.relationship('Utterance', backref='intent', lazy=True, cascade='all, delete-orphan')
    responses = db.relationship('Response', backref='intent', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('chatbot_id', 'name', name='unique_chatbot_intent'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'utterances': [u.to_dict() for u in self.utterances],
            'responses': [r.to_dict() for r in self.responses],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Utterance(db.Model):
    """User utterance/training example model"""
    __tablename__ = 'utterances'
    
    id = db.Column(db.Integer, primary_key=True)
    intent_id = db.Column(db.Integer, db.ForeignKey('intents.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text
        }


class Response(db.Model):
    """Bot response model"""
    __tablename__ = 'responses'
    
    id = db.Column(db.Integer, primary_key=True)
    intent_id = db.Column(db.Integer, db.ForeignKey('intents.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text
        }


class Entity(db.Model):
    """Entity definition model"""
    __tablename__ = 'entities'
    
    id = db.Column(db.Integer, primary_key=True)
    chatbot_id = db.Column(db.Integer, db.ForeignKey('chatbots.id'), nullable=False)
    entity_id = db.Column(db.String(100), nullable=False)  # e.g., "entity.name"
    entity_type = db.Column(db.String(50), nullable=False)  # NAME, DATE, LOCATION, etc.
    description = db.Column(db.Text)
    examples = db.Column(db.JSON, default=list)  # List of examples
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('chatbot_id', 'entity_id', name='unique_chatbot_entity'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'description': self.description,
            'examples': self.examples
        }


# ===============================================
# API Routes
# ===============================================

# Health Check
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'API is running'}), 200


# ===============================================
# ChatBot Endpoints
# ===============================================

@app.route('/api/chatbots', methods=['GET'])
def get_chatbots():
    """Get all chatbots"""
    try:
        chatbots = ChatBot.query.all()
        return jsonify([cb.to_dict() for cb in chatbots]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chatbots', methods=['POST'])
def create_chatbot():
    """Create a new chatbot"""
    try:
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        # Check if chatbot already exists
        existing = ChatBot.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Chatbot with this name already exists'}), 409
        
        chatbot = ChatBot(
            name=data['name'],
            description=data.get('description', ''),
            language=data.get('language', 'en')
        )
        
        db.session.add(chatbot)
        db.session.commit()
        
        return jsonify(chatbot.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/chatbots/<int:chatbot_id>', methods=['GET'])
def get_chatbot(chatbot_id):
    """Get specific chatbot with all intents and entities"""
    try:
        chatbot = ChatBot.query.get(chatbot_id)
        if not chatbot:
            return jsonify({'error': 'Chatbot not found'}), 404
        
        result = chatbot.to_dict()
        result['intents'] = [i.to_dict() for i in chatbot.intents]
        result['entities'] = [e.to_dict() for e in chatbot.entities]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chatbots/<int:chatbot_id>', methods=['PUT'])
def update_chatbot(chatbot_id):
    """Update chatbot"""
    try:
        chatbot = ChatBot.query.get(chatbot_id)
        if not chatbot:
            return jsonify({'error': 'Chatbot not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            chatbot.name = data['name']
        if 'description' in data:
            chatbot.description = data['description']
        if 'language' in data:
            chatbot.language = data['language']
        if 'is_trained' in data:
            chatbot.is_trained = data['is_trained']
        
        db.session.commit()
        
        return jsonify(chatbot.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/chatbots/<int:chatbot_id>', methods=['DELETE'])
def delete_chatbot(chatbot_id):
    """Delete chatbot"""
    try:
        chatbot = ChatBot.query.get(chatbot_id)
        if not chatbot:
            return jsonify({'error': 'Chatbot not found'}), 404
        
        db.session.delete(chatbot)
        db.session.commit()
        
        return jsonify({'message': 'Chatbot deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===============================================
# Intent Endpoints
# ===============================================

@app.route('/api/chatbots/<int:chatbot_id>/intents', methods=['POST'])
def create_intent(chatbot_id):
    """Create intent for chatbot"""
    try:
        chatbot = ChatBot.query.get(chatbot_id)
        if not chatbot:
            return jsonify({'error': 'Chatbot not found'}), 404
        
        data = request.get_json()
        
        if not data or not data.get('name'):
            return jsonify({'error': 'Intent name is required'}), 400
        
        intent = Intent(
            chatbot_id=chatbot_id,
            name=data['name'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium')
        )
        
        db.session.add(intent)
        db.session.flush()
        
        # Add utterances
        for utterance_text in data.get('utterances', []):
            utterance = Utterance(intent_id=intent.id, text=utterance_text)
            db.session.add(utterance)
        
        # Add responses
        for response_text in data.get('responses', []):
            response = Response(intent_id=intent.id, text=response_text)
            db.session.add(response)
        
        db.session.commit()
        
        return jsonify(intent.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Intent with this name already exists for this chatbot'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/intents/<int:intent_id>', methods=['GET'])
def get_intent(intent_id):
    """Get specific intent"""
    try:
        intent = Intent.query.get(intent_id)
        if not intent:
            return jsonify({'error': 'Intent not found'}), 404
        
        return jsonify(intent.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intents/<int:intent_id>', methods=['PUT'])
def update_intent(intent_id):
    """Update intent"""
    try:
        intent = Intent.query.get(intent_id)
        if not intent:
            return jsonify({'error': 'Intent not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            intent.name = data['name']
        if 'description' in data:
            intent.description = data['description']
        if 'priority' in data:
            intent.priority = data['priority']
        
        # Update utterances if provided
        if 'utterances' in data:
            Utterance.query.filter_by(intent_id=intent_id).delete()
            for utterance_text in data['utterances']:
                utterance = Utterance(intent_id=intent_id, text=utterance_text)
                db.session.add(utterance)
        
        # Update responses if provided
        if 'responses' in data:
            Response.query.filter_by(intent_id=intent_id).delete()
            for response_text in data['responses']:
                response = Response(intent_id=intent_id, text=response_text)
                db.session.add(response)
        
        db.session.commit()
        
        return jsonify(intent.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/intents/<int:intent_id>', methods=['DELETE'])
def delete_intent(intent_id):
    """Delete intent"""
    try:
        intent = Intent.query.get(intent_id)
        if not intent:
            return jsonify({'error': 'Intent not found'}), 404
        
        db.session.delete(intent)
        db.session.commit()
        
        return jsonify({'message': 'Intent deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===============================================
# Entity Endpoints
# ===============================================

@app.route('/api/chatbots/<int:chatbot_id>/entities', methods=['POST'])
def create_entity(chatbot_id):
    """Create entity for chatbot"""
    try:
        chatbot = ChatBot.query.get(chatbot_id)
        if not chatbot:
            return jsonify({'error': 'Chatbot not found'}), 404
        
        data = request.get_json()
        
        if not data or not data.get('entity_id') or not data.get('entity_type'):
            return jsonify({'error': 'entity_id and entity_type are required'}), 400
        
        entity = Entity(
            chatbot_id=chatbot_id,
            entity_id=data['entity_id'],
            entity_type=data['entity_type'],
            description=data.get('description', ''),
            examples=data.get('examples', [])
        )
        
        db.session.add(entity)
        db.session.commit()
        
        return jsonify(entity.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Entity with this ID already exists for this chatbot'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/entities/<int:entity_id>', methods=['GET'])
def get_entity(entity_id):
    """Get specific entity"""
    try:
        entity = Entity.query.get(entity_id)
        if not entity:
            return jsonify({'error': 'Entity not found'}), 404
        
        return jsonify(entity.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/entities/<int:entity_id>', methods=['PUT'])
def update_entity(entity_id):
    """Update entity"""
    try:
        entity = Entity.query.get(entity_id)
        if not entity:
            return jsonify({'error': 'Entity not found'}), 404
        
        data = request.get_json()
        
        if 'entity_id' in data:
            entity.entity_id = data['entity_id']
        if 'entity_type' in data:
            entity.entity_type = data['entity_type']
        if 'description' in data:
            entity.description = data['description']
        if 'examples' in data:
            entity.examples = data['examples']
        
        db.session.commit()
        
        return jsonify(entity.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/entities/<int:entity_id>', methods=['DELETE'])
def delete_entity(entity_id):
    """Delete entity"""
    try:
        entity = Entity.query.get(entity_id)
        if not entity:
            return jsonify({'error': 'Entity not found'}), 404
        
        db.session.delete(entity)
        db.session.commit()
        
        return jsonify({'message': 'Entity deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===============================================
# Export/Import Endpoints
# ===============================================

@app.route('/api/chatbots/<int:chatbot_id>/export', methods=['GET'])
def export_chatbot(chatbot_id):
    """Export chatbot as JSON"""
    try:
        chatbot = ChatBot.query.get(chatbot_id)
        if not chatbot:
            return jsonify({'error': 'Chatbot not found'}), 404
        
        export_data = {
            'metadata': {
                'name': chatbot.name,
                'description': chatbot.description,
                'language': chatbot.language,
                'created_date': chatbot.created_at.isoformat(),
                'version': '1.0.0'
            },
            'intents': [i.to_dict() for i in chatbot.intents],
            'entities': [e.to_dict() for e in chatbot.entities],
            'statistics': {
                'total_intents': len(chatbot.intents),
                'total_utterances': sum(len(i.utterances) for i in chatbot.intents),
                'total_responses': sum(len(i.responses) for i in chatbot.intents),
                'total_entities': len(chatbot.entities)
            }
        }
        
        return jsonify(export_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chatbots/<int:chatbot_id>/import', methods=['POST'])
def import_chatbot(chatbot_id):
    """Import chatbot data from JSON"""
    try:
        chatbot = ChatBot.query.get(chatbot_id)
        if not chatbot:
            return jsonify({'error': 'Chatbot not found'}), 404
        
        data = request.get_json()
        
        # Import intents
        for intent_data in data.get('intents', []):
            intent = Intent(
                chatbot_id=chatbot_id,
                name=intent_data['name'],
                description=intent_data.get('description', ''),
                priority=intent_data.get('priority', 'medium')
            )
            db.session.add(intent)
            db.session.flush()
            
            # Add utterances and responses
            for utterance_text in intent_data.get('utterances', []):
                utterance = Utterance(intent_id=intent.id, text=utterance_text)
                db.session.add(utterance)
            
            for response_text in intent_data.get('responses', []):
                response = Response(intent_id=intent.id, text=response_text)
                db.session.add(response)
        
        # Import entities
        for entity_data in data.get('entities', []):
            entity = Entity(
                chatbot_id=chatbot_id,
                entity_id=entity_data['entity_id'],
                entity_type=entity_data['entity_type'],
                description=entity_data.get('description', ''),
                examples=entity_data.get('examples', [])
            )
            db.session.add(entity)
        
        db.session.commit()
        
        return jsonify({'message': 'Chatbot imported successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ===============================================
# Statistics Endpoint
# ===============================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        stats = {
            'total_chatbots': ChatBot.query.count(),
            'total_intents': Intent.query.count(),
            'total_utterances': Utterance.query.count(),
            'total_responses': Response.query.count(),
            'total_entities': Entity.query.count(),
            'trained_chatbots': ChatBot.query.filter_by(is_trained=True).count()
        }
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===============================================
# Error Handlers
# ===============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ===============================================
# CLI Commands
# ===============================================

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized successfully!')


@app.cli.command()
def drop_db():
    """Drop all database tables"""
    if input('Are you sure? (y/n): ').lower() == 'y':
        db.drop_all()
        print('Database dropped!')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
