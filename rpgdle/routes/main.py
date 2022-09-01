from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from rpgdle.extensions import db
from rpgdle.models import User, Doodle, Participation, Post

import datetime

main = Blueprint("main", __name__)

@main.route("/")
def index():
    answerers = {}
    if (current_user.is_authenticated):
        print(current_user)
        own_groups = current_user.groups
        print("OWN GROUPS:")
        print(own_groups)
        own_groups = own_groups.split(",")
        print(own_groups)
    else:
        return render_template("main.html")
    doodles = Doodle.query.order_by(Doodle.created.desc()).all()
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
    group_doodles=[]
    for d in doodles:
        names = []
        print("checking Doodle:")
        print(d.name)
        g = d.groups
        print(g)
        print(type(d.groups))
        ### THIS IS NOT WORKING!!!!! ONLY THE FIRST IS SOMEHOW CHECKED ###
        if (g):
            g = g.split(",")
            print("doodle groups:")
            print(g)
        else:
            print("no groups for doodle");


        if ( g and ( set(own_groups) & set(g) or set(g) & set(own_groups))):
            print("COMMON GROUP FOUND =")
            print(set(own_groups) & set(g))
            group_doodles.append(d)
        else:
            print("NO COMMON GROUP for ")
            print(set(own_groups))
            print(set(g))
            print(d)
            #doodles.remove(d);
            #print("removed")
            continue
        uid = Participation.query.filter_by(doodle_id=d.id).with_entities(Participation.user_id).distinct().all()
        for id in uid:
            names.append(User.query.filter_by(id=id[0]).first().name)
            answerers[d.id] = names
    print(answerers)
    print("ANSWERERS:")
    #print(answerers)
    context = {"doodles": group_doodles, "answerers": answerers}
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
        creator = User.query.filter_by(id=doodle.creator).first()
        if (creator):
            creator = creator.name
        else:
            creator = "Deleted user"
        #""".filter_by(admin=False)"""
        users = [u.serialize() for u in User.query.all()]
        correct_users = []
        if (current_user):
            own_groups = current_user.groups
            print(own_groups)
            if len(own_groups.split(",")) < 1:
                t = own_groups
                own_groups = []
                own_groups[0] = t
            else:
                own_groups = own_groups.split(",")
            print("current user, looping users against")
            for u in users:
                print(u)
                g = u["groups"]
                print(g)
                if (g):
                    g = g.split(",")
                    print("user groups:")
                    print(g)
                else:
                    print("no groups for doodle");

                if ( g and ( set(own_groups) & set(g) or set(g) & set(own_groups))):
                    print("COMMON GROUP FOUND =")
                    print(set(own_groups))
                    print(set(own_groups) & set(g))
                    correct_users.append(u)
                else:
                    print("NO COMMON GROUP for ")
                    print(set(own_groups))
                    print(set(g))
                    continue

        participations = [p.serialize() for p in Participation.query.filter_by(doodle_id=doodle.id).all()]
        posts = [o.serialize() for o in Post.query.filter_by(doodle_id=doodle.id).order_by(Post.created.desc()).all()]
        print(participations)
        print(User.query.filter_by(admin=False).all())
        print(users)
        print(posts)
        context = {"doodle": doodle, "creator": creator, "users":correct_users, "participations":participations, "posts":posts}
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
        name = name.replace(" ", "-")
        description = request.form["description"]
        dates = request.form["dates"]
        groups = request.form.to_dict(flat=False)["groups"]
        groups_string=""
        for g in groups:
            groups_string+=(g+",")
        if groups_string[-1] == ",":
            groups_string = groups_string[:-1]
        print("groups string:")
        print(groups_string)
        creator = current_user.id
        old = False
        created = datetime.datetime.now()
        doodle = Doodle(name=name, description = description, groups = groups_string, dates = dates, old=old, creator = creator, created = created)
        #user = User(name=name, unhashed_password=unhashed_password, admin=False)
        db.session.add(doodle)
        db.session.commit()
        return redirect(url_for("main.index"))
    else: #GET
        groups = current_user.groups.split(",")
        print("SEnding current users group to create: ")
        print(groups)
        context = {"groups": groups}
        return render_template("create.html", **context)


@main.route("/users", methods=["GET", "POST"])
@login_required
def users():
    if request.method == "POST":
        print("Size of form: ", len(request.form))
        print(request.form)
        for action in request.form:
            print(action)
            target = action.split("-")[1]
            print(action.split("-")[0])
            print(target)
            target_user = User.query.filter_by(id=target).first()
            print(target_user)
            if action.split("-")[0] == "groups" and target_user:
                groups = request.form["groups-"+target]
                if len(groups)!=0:
                    print("New groups from form:")
                    print(groups)
                    print("Existing groups for user:")
                    print(target_user.groups)
                    if len(groups) != 0:
                        print("ADDING GROUP!")
                        if len(target_user.groups)!=0:
                            groups+=","
                        groups+=target_user.groups
                        target_user.groups = groups
                    print("NEW GROUPS:")
                    print(target_user.groups)
            if action.split("-")[0] == "promote" and target_user:
                print("PROMOTING ", target_user.name)
                target_user.admin = True
            if action.split("-")[0] == "ungroup" and target_user:
                print("UNGROUPING ", target_user.name)
                target_user.groups = ""
            if action.split("-")[0] == "delete" and target_user:
                print("DELETING ", target_user.name)
                db.session.delete(target_user)
            print("Commiting")
            db.session.commit()
            groups = "";
    users = User.query.all()
    context = {"users": users}
    return render_template("users.html", **context)
