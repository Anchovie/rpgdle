from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from rpgdle.extensions import db
from rpgdle.models import User, Doodle, Participation

import datetime

main = Blueprint("main", __name__)

@main.route("/")
def index():
    doodles = Doodle.query.all()
    context = {"doodles": doodles}
    return render_template("main.html", **context)

@main.route("/session/<string:doodle_name>", methods=["GET", "POST"])
@login_required
def session(doodle_name):
    if request.method == "POST":
        print("Dates from form")
        print(request.form["dates"])

        doodle_id = Doodle.query.filter_by(name=doodle_name).first().id
        dates = request.form["dates"]
        if ("deleteFlag" in request.form):
            print("delete = ", request.form["deleteFlag"])
            doodle = Doodle.query.filter_by(id = doodle_id).first()
            db.session.delete(doodle)
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            print("no delete")
        user_id = current_user.id
        dateArr = dates.strip(" ").split(",")
        status = ""
        print(dateArr)
        existing_participations = Participation.query.filter_by(doodle_id=doodle_id).filter_by(user_id=user_id).all()
        print("existing participation for this doodle and user:")
        print(existing_participations)
        ret = Participation.query.filter_by(doodle_id=doodle_id).filter_by(user_id=user_id).delete()
        print(ret)
        existing_participations = Participation.query.filter_by(doodle_id=doodle_id).filter_by(user_id=user_id).all()
        print(existing_participations)
        for d in dateArr:
            print(d)
            if "?" in d:
                status = "maybe"
                d=d.replace("?","")
            else:
                status = "okay"
            print(d)
            p = Participation.query.filter_by(doodle_id=doodle_id).filter_by(user_id=user_id).filter_by(date=d).first()
            print("checking for existing participation p =", p)
            if p is None and d:
                participation = Participation(user_id=user_id, doodle_id=doodle_id, date=d, status = status)
                db.session.add(participation)
                print("added")
        db.session.commit()
        return redirect(url_for("main.session",doodle_name=doodle_name))
    else: #GET
        doodle = Doodle.query.filter_by(name=doodle_name).first()
        print("GET START doodle:")
        print(doodle)
        if (not doodle):
            print(doodle)
            return redirect(url_for("main.index"))
        creator = User.query.filter_by(id=doodle.creator).first().name

        users = [u.serialize() for u in User.query.filter_by(admin=False).all()]
        participations = [p.serialize() for p in Participation.query.filter_by(doodle_id=doodle.id).all()]
        print(participations)
        print(User.query.filter_by(admin=False).all())
        print(users)
        context = {"doodle": doodle, "creator": creator, "users":users, "participations":participations}
        return render_template("doodle.html", **context)

@main.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        dates = request.form["dates"]
        creator = current_user.id
        old = False
        created = datetime.datetime.now()
        doodle = Doodle(name=name, description = description, dates = dates, old=old, creator = creator, created = created)
        #user = User(name=name, unhashed_password=unhashed_password, admin=False)
        db.session.add(doodle)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("create.html")


@main.route("/users")
@login_required
def users():
    users = User.query.filter_by(admin=False).all()
    context = {"users": users}

    return render_template("users.html", **context)
