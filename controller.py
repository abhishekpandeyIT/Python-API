"""
This is a Flask application that interacts with Firestore to provide API endpoints for managing user preferences and favorites.

The following routes are available:

GET '/preferences/<user_id>':
    Retrieve user preferences based on the user ID.

POST '/preferences/<user_id>':
    Update user preferences based on the user ID.

GET '/preferences/<user_id>/favorites':
    Retrieve user favorites based on the user ID.

POST '/preferences/<user_id>/favorites':
    Add a user favorite recipe based on the user ID.

DELETE '/preferences/<user_id>/favorites/<recipe_id>':
    Delete a user favorite recipe based on the user ID and recipe ID.

"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)
# Adding cors to flask
CORS(app)

# Initialize Firebase app
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route('/preferences/<user_id>', methods=['GET'])
def get_user_preferences(user_id):
    """
    Retrieve user preferences based on the user ID.

    Args:
    user_id (str): A string representing the unique ID of the user.

    Returns:
    A JSON object representing the user preferences if found, or an error message if the user is not found.
    """

    doc_ref = db.collection('user_preference').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return jsonify(doc.to_dict())
    else:
        return jsonify({'error': 'User not found'})


@app.route('/preferences/<user_id>', methods=['POST'])
def update_user_preferences(user_id):
    """
    Update user preferences based on the user ID.

    Args:
    user_id (str): A string representing the unique ID of the user.

    Returns:
    A JSON object representing the success message if the preferences are updated successfully.
    """

    doc_ref = db.collection('user_preference').document(user_id)
    doc_data = request.get_json()
    doc_ref.set(doc_data)
    return jsonify({'message': 'Preferences updated successfully'})


@app.route('/preferences/<user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    """
    Retrieve user favorites based on the user ID.

    Args:
    user_id (str): A string representing the unique ID of the user.

    Returns:
    A JSON object representing the user favorites if found.
    """

    doc_ref = db.collection("user_preference").document(user_id)
    favorites_ref = doc_ref.collection("favorites_recipe")
    favorites = []
    for fav in favorites_ref.stream():
        favorites.append(fav.to_dict())

    response = {'favorites': favorites}
    return jsonify(response), 200


@app.route('/preferences/<user_id>/favorites', methods=['POST'])
def add_user_favorite(user_id):
    """
    Add a user favorite recipe based on the user ID.

    Args:
    user_id (str): A string representing the unique ID of the user.

    Returns:
    A JSON object representing the success message and the generated favorite recipe ID.
    """

    request_data = request.get_json()

    doc_ref = db.collection("user_preference").document(user_id)
    favorites_ref = doc_ref.collection("favorites_recipe")
    favorite_doc_ref = favorites_ref.document()
    favorite_doc_ref.set(request_data)
    favorite_id = favorite_doc_ref.id

    response = {'message': 'User favorite recipe added successfully.',
                'favorite_id': favorite_id}
    return jsonify(response), 200


@app.route('/preferences/<user_id>/favorites/<recipe_id>', methods=['DELETE'])
def delete_user_favorite_recipe(user_id, recipe_id):
    """
    API endpoint to delete user favorite.

    Args:
        user_id (str): The user ID for whom a favorite recipe is to be deleted.
        recipe_id (str): The favorite recipe ID to be deleted.

    Returns:
        A JSON response confirming the favorite recipe was deleted successfully.
    """

    doc_ref = db.collection("user_preference").document(user_id)
    favorites_ref = doc_ref.collection("favorites_recipe")
    favorites_ref.document(recipe_id).delete()

    response = {'message': 'User favorite recipe deleted successfully.'}
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
