from flask import render_template, url_for, flash, redirect,request,abort
from blog.forms import RegistrationForm, LoginForm,UpdateForm,new_post,update_post
from blog import app,db,bcrypt,LoginManager
from blog.model import User,Post
from flask_login import login_user,current_user,logout_user,login_required
import os
import secrets

def save_image(form_image):
    _,fl_ext=os.path.splitext(form_image.filename)
    fl_name= secrets.token_hex(8)
    img_fl_name=fl_name+fl_ext
    img_fl= os.path.join(app.root_path,'static/images/',img_fl_name)
    form_image.save(img_fl)
    return img_fl_name




# post = [
#
#     {"name": "Salim",
#      "age":"30",
#      "married": "yes",
#      "address": "Narimadakeel wandoor malappurem kerala"
#      },
#     {
#         "name": "saleem",
#         "age": "30",
#         "married": "no",
#         "address": "Narimadakeel wandoor malappurem kerala"
#
#     }]

@app.route("/home")
@app.route("/")
def home():

    page=request.args.get('page',1,type=int)
    post = Post.query.paginate(page=page,per_page=3)

  #  image=User.
    #print (image_file_name.image_file)
    return render_template("home.html",post=post)

@app.route("/about")
def about():
    return render_template("about.html",title="about")

@app.route("/register",methods=('GET','POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    print(form.email.errors)

    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,
                    password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        flash('Account has created for {}'.format(form.username.data),'success')
        return redirect(url_for('home'))


    return render_template("register.html",title="register",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
       username=User.query.filter_by(username=form.username.data).first()
       if not username:
          flash("invalid user or password", 'danger')
       elif username.username and bcrypt.check_password_hash(username.password,form.password.data):
          login_user(username,remember=form.remember.data)
          next_page=request.args.get('next')
          flash("Logged in",'success')
          return  redirect(next_page) if next_page else redirect(url_for('home'))
       else:
          flash("invalid user or password", 'danger')
           # print(bcrypt.check_password_hash(email.password,form.password.data))
    return render_template("login.html",title="Log in",form=form)

@app.route("/logout")
@login_required
def logout():
    flash("logged out", 'danger')
    logout_user()
    return redirect(url_for('home'))


@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=UpdateForm()
    if request.method =='GET':
        form.username.data= current_user.username
        form.email.data = current_user.email
    elif form.validate_on_submit():
        if form.image.data:
            file_name=current_user.image_file
            path=os.path.isfile(app.root_path+'/static/images/'+file_name)
            if path:
                os.remove(app.root_path+'/static/images/'+file_name)
                print (file_name)
            current_user.image_file= save_image(form.image.data)
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Account has updated",'success')
        return redirect(url_for('account'))
    return render_template('account.html',form=form,title="Account")



@app.route("/post",methods=['GET','POST'])
@login_required
def post():
    form=new_post()
    if form.validate_on_submit():
        id=current_user.id
        print (id)
        post=Post(user_id=id,title=form.title.data,content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash("{} Article has created".format(form.title.data),'success')
        return  redirect(url_for('home'))
    return render_template("post.html",form=form,title="New Post",legend="New Post")


@app.route("/post_id/<int:post_id>")
def post_id(post_id):
    post=Post.query.get_or_404(post_id)
    image_file= os.path.join('/static/images',post.author.image_file)
    return render_template("post_id.html",post=post,title=post.title,image_file=image_file)



@app.route("/post_id/<int:post_id>/update",methods=['GET','POST'])
@login_required
def post_update(post_id):
    form = update_post(request.form)
    post = Post.query.get_or_404(post_id)
    print(form.content.data)
    if post.author.username !=current_user.username:
        abort(403)
    elif request.method=='GET':
        form.content.data=post.content

    elif request.method=='POST':
        print (form.content.errors)
        post.content=form.content.data
        db.session.commit()
        flash("post content has updated",'success')


    return render_template("post_update.html",post_id=post_id, form=form,legend='Post Update',post=post)



@app.route("/post_id/<int:post_id>/delete",methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.username !=current_user.username:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post has delete", 'success')
    return redirect(url_for("home"))















