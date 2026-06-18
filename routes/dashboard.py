from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect

from core.report_service import ReportService

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/")
def home():
    return redirect("/v3")

@dashboard_bp.route(
    "/v3",
    methods=["GET", "POST"]
)
def index_v3():

    result = None

    if request.method == "POST":

        try:

            day = int(
                request.form.get("day")
            )

            month = int(
                request.form.get("month")
            )

            year = int(
                request.form.get("year")
            )

            result = ReportService.build(
                day,
                month,
                year
            )

        except Exception as e:

            raise e

    return render_template(
        "templates_v3/index.html",
        result=result
    )