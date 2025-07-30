# SocialSphere Backend

## Overview

SocialSphere Backend is a robust and scalable social media platform backend built with Django and Django REST Framework. It provides a comprehensive set of features for user management, content creation (posts and comments), interactions (likes, replies, pinning), and a sophisticated user relationship system including following, blocking, and private profiles with follow requests.

This project is designed to be the backbone for a modern social application, offering a clean API and an extensible architecture.

-----

## Features

### User Management

  * **Custom User Model**: Extends Django's `AbstractBaseUser` with email as the primary authentication field.
  * **User Registration**: Secure user registration with password hashing.
  * **User Profiles**: Customizable user profiles with personal information (bio, picture, phone number) and privacy settings.

### Content Management

  * **Posts**: Users can create, view, update, and delete posts, including text content, images, and files.
  * **Comments**: Users can comment on posts and reply to existing comments, forming discussion threads.
  * **Likes**: A generic liking system allows users to like both posts and comments.
  * **Pinning**: Users can "pin" posts and comments to highlight important content, with a filter to display pinned items first.

### User Relationships

  * **Following/Followers**: Users can follow and unfollow other users.
  * **Private Profiles**: Support for private profiles where follow requests are required.
  * **Follow Requests**: Users can send, accept, decline, and undo follow requests.
  * **Blocking**: Users can block other users, preventing any interaction and mutual following.
  * **Mutual Followers**: Functionality to identify mutual followers between users.

### API Endpoints

A well-structured RESTful API is provided, covering all functionalities:

  * User authentication (token-based).
  * User registration.
  * CRUD operations for Posts and Comments.
  * Liking and unliking posts/comments.
  * Toggling pin status for posts/comments.
  * Managing user profiles (viewing, updating).
  * Handling user relationships: follow, unfollow, block, unblock, accept/decline follow requests, undo requests.

### Permissions & Security

  * **IsAuthenticated**: Ensures only authenticated users can access certain endpoints.
  * **IsAuthor**: Restricts update/delete operations on posts and comments to their respective authors.
  * **Profile Permissions**: Handles access to private profiles based on follow status.
  * **Relationship Permissions**: Custom permissions (`NotIdentical`, `NotBlocked`, `StateNotAlreadySet`, `NotAlreadyBlocked`, `IsRequested`, `AlreadyBlocked`) enforce robust business logic for user interactions.

-----

## Getting Started

### Prerequisites

  * Python 3.13+
  * Django 5.x+
  * Django REST Framework 3.15.2+
  * Pillow (for image handling)
  * `djangorestframework-simplejwt` (for token authentication)
  * `rest-framework-generic-relations` (for generic foreign keys)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/AliAfkhamii/SocialSphere-Backend.git
    cd SocialSphere-Backend
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```


4.  **Set up your Django settings:**
    Create a `.env` file or configure your `settings.py` with necessary environment variables, especially `SECRET_KEY`, database configurations, and any media/static file settings.

    ```python
    # In settings.py (or loaded from .env)
    # SECRET_KEY = 'your_secret_key_here'
    # AUTH_USER_MODEL = 'accounts.User'
    # PINNED_POST_LIMIT = 5 # Example setting
    # PINNED_COMMENT_LIMIT = 3 # Example setting
    ```

5.  **Run database migrations:**

    ```bash
    python manage.py makemigrations accounts posts profiles
    python manage.py migrate
    ```

6.  **Create a superuser (optional, for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/`.

-----

## API Endpoints

Below is a summary of the main API endpoints. Full documentation can be generated using tools like drf-yasg or Postman collections.

### Authentication & Users

  * `POST /accounts/token/`: Obtain JWT token.
  * `POST /accounts/token/refresh/`: Refresh JWT token.
  * `POST /accounts/register/`: Register a new user.
  * `GET /profile/me/`: Retrieve current user's profile.
  * `PUT /profile/me/`: Update current user's profile.
  * `GET /profile/<int:id>/`: Retrieve a user's profile by ID.
  * `PUT /profile/<int:id>/`: Update a user's profile by ID (requires `IsOwner` permission).

### Posts

  * `GET /posts/`: List all posts by the authenticated user, ordered by pinned status.
  * `POST /posts/`: Create a new post.
  * `GET /posts/<int:id>/`: Retrieve a specific post.
  * `PUT /posts/<int:id>/`: Update a specific post (requires `IsAuthor`).
  * `DELETE /posts/<int:id>/`: Delete a specific post (requires `IsAuthor`).
  * `GET /profiles/<int:id>/posts/`: List posts by a specific user.
  * `POST /posts/<int:id>/toggle_pin/`: Toggle pin status for a post.

### Comments

  * `GET /posts/<int:id>/comments/`: List comments for a specific post, ordered by pinned status.
  * `POST /posts/<int:id>/comments/`: Create a new comment on a post.
  * `GET /comments/<int:id>/`: Retrieve a specific comment.
  * `PUT /comments/<int:id>/`: Update a specific comment (requires `IsAuthor`).
  * `DELETE /comments/<int:id>/`: Delete a specific comment (requires `IsAuthor`).
  * `GET /comments/<int:id>/replies/`: List replies for a specific comment.
  * `POST /comments/<int:id>/replies/`: Create a new reply to a comment.
  * `POST /comments/<int:id>/toggle_pin/`: Toggle pin status for a comment.

### Likes

  * `GET /posts/<int:id>/likes/`: List users who liked a specific post.
  * `POST /posts/<int:id>/likes/`: Toggle like status for a post.
  * `GET /comments/<int:id>/likes/`: List users who liked a specific comment.
  * `POST /comments/<int:id>/likes/`: Toggle like status for a comment.

### User Actions (Follow/Block) - accessed via `/profile/<int:id>/<action>/`

  * `POST /profile/<int:id>/follow/`: Follow a user.
  * `POST /profile/<int:id>/unfollow/`: Unfollow a user.
  * `POST /profile/<int:id>/block/`: Block a user.
  * `POST /profile/<int:id>/unblock/`: Unblock a user.
  * `POST /profile/<int:id>/undo_request/`: Undo a follow request.
  * `POST /profile/<int:id>/accept/`: Accept a follow request.
  * `POST /profile/<int:id>/decline/`: Decline a follow request.

-----

## Contributing

Contributions are welcome\! Please feel free to open issues or submit pull requests.

-----

## License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

-----