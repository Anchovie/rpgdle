from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from rpgdle.extensions import db
from rpgdle.models import User, Doodle, Participation, Post

import datetime

main = Blueprint("main", __name__)

@main.route("/")
def index():
    answerers = {}
    doodles = Doodle.query.all()
    user = User.query.filter_by(id=1).first()
    if (user):
        print("Elevating priviledges for found user with id = " , user.id)
        user.admin = True
        db.session.commit()
    """
    print(doodles)
    print(doodles[0].id)
    print(Participation.query.filter_by(doodle_id=doodles[0].id).all())
    print(Participation.query.filter_by(doodle_id=doodles[0].id).with_entities(Participation.user_id).all())
    print(Participation.query.filter_by(doodle_id=doodles[0].id).with_entities(Participation.user_id).distinct().all())
    """
    for d in doodles:
        names = []
        uid = Participation.query.filter_by(doodle_id=d.id).with_entities(Participation.user_id).distinct().all()
        for id in uid:
            names.append(User.query.filter_by(id=id[0]).first().name)
            answerers[d.id] = names
    print(answerers)
    print("ANSWERERS:")
    #print(answerers)
    context = {"doodles": doodles, "answerers": answerers}
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

        users = [u.serialize() for u in User.query""".filter_by(admin=False)""".all()]
        participations = [p.serialize() for p in Participation.query.filter_by(doodle_id=doodle.id).all()]
        posts = [o.serialize() for o in Post.query.filter_by(doodle_id=doodle.id).order_by(Post.created.desc()).all()]
        print(participations)
        print(User.query.filter_by(admin=False).all())
        print(users)
        print(posts)
        context = {"doodle": doodle, "creator": creator, "users":users, "participations":participations, "posts":posts}
        return render_template("doodle.html", **context)

@main.route("/createPost/<string:doodle_name>", methods=["GET", "POST"])
@login_required
def createPost(doodle_name):
    if request.method == "POST":
        content = request.form["comment"]
        doodle_id = Doodle.query.filter_by(name=doodle_name).first().id
        print("doodle id for the doodle ",doodle_name)
        print(doodle_id)
        post = Post(poster=current_user.id, poster_name = current_user.name, doodle_id=doodle_id, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("main.session",doodle_name=doodle_name))

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
