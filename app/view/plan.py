# -*- coding: utf-8 -*-
"""plan views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.utils import flash_errors

blueprint = Blueprint("plan", __name__, url_prefix="/plan", static_folder="../static")


@blueprint.route("/")
@login_required
def index():
    """List members."""
    return render_template("plan/members.html")


from app.forms.plan import PlanForm
from app.services.PlanServices import PlanServices
from app.models.plan import Plan


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """List members."""

    form = PlanForm(request.form)
    if form.validate_on_submit():
        model = PlanServices.crate(form)

        return redirect(url_for("plan.lists", _id=model.id))
    else:
        flash_errors(form)

    return render_template("plan/lists.html", form=form)


@blueprint.route("/lists/<int:_id>")
@login_required
def lists(_id):
    """List members."""

    form = PlanForm(request.form)
    model = PlanServices.filter_by(_id)

    form.name.data = model.name
    form.initial_quotas.data = model.initial_quotas
    form.price_top.data = model.price_top
    form.price_bottom.data = model.price_bottom
    form.increase_rate.data = model.increase_rate
    form.reduce_rate.data = model.reduce_rate
    form.start_price.data = model.start_price

    resp = PlanServices.compute(model)

    profit_margin = round(resp["profit_margin"] *100, 1)
    amount_money = resp["amount_money"]
    data = resp["data"]
    profit = resp["profit"]

    return render_template("plan/lists.html", form=form, profit=profit,
                           profit_margin=profit_margin, amount_money=int(amount_money), data=data)