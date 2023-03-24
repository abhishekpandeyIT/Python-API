from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase app
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# API endpoint to get user preferences


@app.route('/preferences/<user_id>', methods=['GET'])
def get_user_preferences(user_id):
    doc_ref = db.collection('user_preference').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return jsonify(doc.to_dict())
    else:
        return jsonify({'error': 'User not found'})

# API endpoint to update user preferences


@app.route('/preferences/<user_id>', methods=['POST'])
def update_user_preferences(user_id):
    doc_ref = db.collection('user_preference').document(user_id)
    doc_data = request.get_json()
    doc_ref.set(doc_data)
    return jsonify({'message': 'Preferences updated successfully'})


@app.route('/preferences/<user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    # Get the user favorites data from Firestore
    doc_ref = db.collection("user_preference").document(user_id)
    favorites_ref = doc_ref.collection("favorites_recipe")
    favorites = []
    for fav in favorites_ref.stream():
        favorites.append(fav.to_dict())

    # Return the user favorites data as a JSON response
    response = {'favorites': favorites}
    return jsonify(response), 200


@app.route('/preferences/<user_id>/favorites', methods=['POST'])
def add_user_favorite(user_id):
    # Get the request body JSON data
    request_data = request.get_json()

    # Add the user favorite data to Firestore
    doc_ref = db.collection("user_preference").document(user_id)
    favorites_ref = doc_ref.collection("favorites_recipe")
    favorite_doc_ref = favorites_ref.document()
    favorite_doc_ref.set(request_data)
    favorite_id = favorite_doc_ref.id

    # Return success message with the generated favorite recipe ID
    response = {'message': 'User favorite recipe added successfully.',
                'favorite_id': favorite_id}
    return jsonify(response), 200


@app.route('/preferences/<user_id>/favorites/<recipe_id>', methods=['DELETE'])
def delete_user_favorite(user_id, recipe_id):
    # Delete the user favorite data from Firestore
    doc_ref = db.collection("user_preference").document(user_id)
    favorites_ref = doc_ref.collection("favorites_recipe")
    favorites_ref.document(recipe_id).delete()

    # Return success message
    response = {'message': 'User favorite deleted successfully.'}
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
