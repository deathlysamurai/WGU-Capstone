from flask import render_template, Blueprint, request
from ...models import ACCESS, User, Food, Unit, Meal
from ...decorators import requires_access_level
from flask_login import current_user
import datetime

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def home():
    items = []
    report_date = datetime.datetime.now()
    report = False
    if request.method == 'POST':
        report = True
        report_type = request.form.get('report_type')
        table_title = "Report (" + report_type + ")"
        if report_type == "users":
            items = User.query.all()
            table_columns = User.table_columns(self=User())
        elif report_type == "foods":
            items = Food.query.all()
            table_columns = Food.table_columns(self=Food())
        elif report_type == "units":
            items = Unit.query.all()
            table_columns = Unit.table_columns(self=Unit())
        elif report_type == "meals":
            items = Meal.query.all()
            table_columns = Meal.table_columns(self=Meal())

    return render_template("admin/home.html", table_columns=table_columns, report=report, report_date=report_date, items=items, table_title=table_title, user=current_user, admin_route=True, page="admin_home")