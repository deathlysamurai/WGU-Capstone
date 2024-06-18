from ..models import User
from werkzeug.security import generate_password_hash

def load_users(app, db): 
    with app.app_context():
        for user in users:
            db.session.add(user)
        db.session.commit()
        print('Users created.')

users = [
    User(username='admin', email='admin@admin.com', password=generate_password_hash('admin'), access=1, monMeal=1, wedMeal=1, friMeal=1),
    User(username='mathew', email='mathew@mathew.com', password=generate_password_hash('mathew'), access=0),
    User(username='autumn', email='autumn@autumn.com', password=generate_password_hash('autumn'), access=0),
]