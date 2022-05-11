from flaskdraw.models import User
import bcrypt
from flask_bcrypt import generate_password_hash


    
def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email and hashed_password are correctly defined
    """
    user = User(username='pdbar',email='pdbartsch@gmail.com', password='FlaskIsAwesome')
    hashed_password = generate_password_hash(user.password).decode(
            "utf-8"
        )
    assert user.username == 'pdbar'
    assert user.email == 'pdbartsch@gmail.com'
    assert hashed_password != user.password

