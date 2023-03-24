# Feed Me Better API

## Overview

Recipe Generation API is a RESTful API built using Flask that allows users to get recipe recommendations based on their preferences. The API uses Firebase as the database to store user preferences and favorite recipes.

## Endpoints

The API supports the following endpoints:

### Get User Preferences
```bash
GET /preferences/<user_id>/preferences
```

This endpoint returns the user preferences for the specified user ID. The preferences include information about the user's dietary restrictions, medical conditions, and allergens.

### Update User Preferences

```bash
POST /preferences/<user_id>/preferences
```

This endpoint updates the user preferences for the specified user ID. The request body should contain a JSON object with the updated preferences.

### Get bookmarked Recipe Informations

```bash
GET /preferences/<user_id>/favorites
```

This endpoint returns recipe bookmarked by the user. The recommendations are generated using machine learning algorithms and are personalized for each user.

### Add Favorite Recipe

```bash
POST /user/<user_id>/favorites`
```
This endpoint adds a favorite recipe for the specified user ID. The request body should contain a JSON object with the recipe details.

### Delete Favorite Recipe

```bash
DELETE /user/<user_id>/favorites/<recipe_id>
```

This endpoint deletes a favorite recipe for the specified user ID and recipe ID.

## Authentication

The API uses Firebase Authentication to authenticate users.

## Firestore and Firebase Storage Rules

The Firestore and Firebase Storage rules are as follows:

### Firestore Rules

```lua
service cloud.firestore {
  match /databases/{database}/documents {
    match /preferences/{user_id} {
      allow read, write: if request.auth.uid == user_id;
      match /preferences/{user_id}/favorites {
        allow read, write: if request.auth.uid == user_id;
         match /preferences/{user_id}/favorites/{recipe_id} {
        allow read, write: if request.auth.uid == user_id;
        }
      } 
    }
  }
}
```

### Firebase Storage Rules

```lua
service firebase.storage {
  match /b/{bucket}/o {
    match /{userId}/favorites_recipe/{recipeId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
} 
```

## Developer Information

This API is developed and maintained by Abhishek Pandey. If you have any questions or concerns, please contact Abhishek Pandey at [abhishekpandeyite@gmail.com](mailto:abhishekpandeyite@gmail.com) or call him at +91-9650374556.

## Legal Information

This API is the property of Abhishek Pandey. All rights reserved. Unauthorized copying, modification, distribution, or use of this API is strictly prohibited. By using this API, you agree to the terms and conditions set forth in the LICENSE file included in this repository.