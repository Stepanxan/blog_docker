from app import app
from flask import render_template, url_for, request
from flask_login import login_required
from sqlalchemy import and_

from models.models import Posts



@app.route('/', methods=["GET"])
def main_page():
    post = Posts.query.all()
    return render_template('main.html', post=post)


@app.route('/about')
@login_required
def about():
    print(url_for('about'))
    return render_template("about.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_404.html'),404


@app.route("/post:<post_id>")
def post_detail_main(post_id):
    detail = Posts.query.get(post_id)
    return render_template("post_detail_main.html", detail=detail)


@app.route("/all_post/", methods=["GET", "POST"])
def all_post():
    post = Posts.query
    page = request.args.get("page")
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = post.paginate(page=page, per_page=4)
    return render_template("all_post.html", post=post, pages=pages)


@app.route("/all_post/categor_post", methods=["GET", "POST"])
def categor_post():
    conditions = []
    if request.args.get('categor'):
        conditions.append(Posts.categor.like(request.args['categor']))

    if_search = Posts.query.filter(and_(*conditions))
    post_categor = if_search.all()

    return render_template("post_categor.html", post_categor=post_categor, conditions=conditions)
