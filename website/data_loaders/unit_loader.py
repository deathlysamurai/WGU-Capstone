from ..models import Unit

def load_units(app, db):
    with app.app_context():
        for unit in units:
            db.session.add(unit)
        db.session.commit()
        print('Units created.')

units = [
    Unit(name='Ounce', abbreviation='oz'),
    Unit(name='Each', abbreviation='ea'),
    Unit(name='Pound', abbreviation='lb'),
    Unit(name='Gram', abbreviation='g'),
    Unit(name='Slice', abbreviation='sl'),
]