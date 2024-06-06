from ...decorators import requires_access_level
from ...models import ACCESS, Unit
from flask_login import current_user
from flask import render_template, Blueprint, request, redirect, url_for, flash, json
from ... import db
from sqlalchemy import func

admin_units = Blueprint('admin_units', __name__)

@admin_units.route('/', methods=['GET'])
@requires_access_level(ACCESS['admin'])
def units():
    units = Unit.query.all()
    add_columns = Unit.add_columns(self=Unit())
    table_columns = Unit.table_columns(self=Unit())

    return render_template("admin/units.html", table_columns=table_columns, add_columns=add_columns, user=current_user, items=units, table_title="Units", admin_route=True, page="units")

@admin_units.route('/add-unit', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def add_unit():
    if request.method == 'POST':
        name = request.form.get('name')
        abbreviation = request.form.get('abbreviation')

        unit_name = Unit.query.filter(func.lower(Unit.name) == name.lower()).first()

        if unit_name:
            flash('Unit already exists', category='error')
        else:
            unit = Unit(name=name, abbreviation=abbreviation)
            db.session.add(unit)
            db.session.commit()
            flash('Unit created.', category='success')

    return redirect(url_for("admin_units.units"))

@admin_units.route('/delete-units', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def delete_units():
    if request.method == 'POST':
        unitIDs = json.loads(request.form.get('delete-items'))
        for unitID in unitIDs:
            unit = Unit.query.get_or_404(unitID)
            db.session.delete(unit)

        try:
            db.session.commit()
            flash("Units deleted successfully.", category='success')
        except:
            flash("Problem deleting units.", category='error')

    return redirect(url_for("admin_units.units"))

@admin_units.route('/update-units', methods=['POST'])
@requires_access_level(ACCESS['admin'])
def update_units():
    if request.method == 'POST':
        successful_units = 0
        update_units = json.loads(request.form.get('update-items'))
        for update_unit in update_units:
            unit = Unit.query.get_or_404(update_unit['id'])
            name = update_unit['name'] if unit.name != update_unit['name'] else None
            abbreviation = update_unit['abbreviation'] if unit.abbreviation != update_unit['abbreviation'] else None
            changed = False
            if name and name != '':
                unit.name = update_unit['name']
                changed = True
            if abbreviation and abbreviation != '':
                unit.abbreviation = update_unit['abbreviation']
                changed = True
            if changed:
                db.session.commit()
                successful_units += 1
        
        if(successful_units > 0):
            flash(str(successful_units)+" units updated successfully.", category="success")  

    return redirect(url_for("admin_units.units"))