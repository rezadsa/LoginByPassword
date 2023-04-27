from main import app,db,bcrypt,login_manager
from flask import render_template,redirect,flash,url_for,request
from main.forms import RegistrationForm,LoginForm,UpdateForm,PostForm
from main.models import User,Post
from flask_login import current_user,login_user,login_required,logout_user
from sqlalchemy import desc



@app.route('/')
def home():
    page=request.args.get('page')

    if page and page.isdigit():
        page=int(page)
    else:
        page=1

    pages=Post.query.order_by(desc('date')).paginate(page=page,per_page=8)
    
    return render_template('home.html',pages=pages)

@app.route('/post/<int:id>/read')
def post_read(id):
    post=Post.query.get_or_404(id)

    return render_template('post_read.html',post=post)


@app.route('/register',methods=['POST','GET'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data)
        user=User(username=form.username.data,
                  email=form.email.data,
                  password=hashed_password
                  )
        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully  ',['success',form.username.data])
        return redirect(url_for('home'))

    return render_template('register.html',form=form)



@app.route('/update',methods=['GET','POST'])
def update_user():
    form=UpdateForm()


    return render_template('update_user.html',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash('Welcome  ',['success',user.username])
            next_page=request.args.get('next')
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash('Email or Password is Invalid!',['warning',' '])


    return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        username=current_user.username
        logout_user()
        flash('Logged Out Successfuly  ',['info',username])
        return redirect(url_for('home'))
    
@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
        form=UpdateForm()
        if form.validate_on_submit():
            current_user.username=form.username.data
            current_user.email=form.email.data
            db.session.commit()
            flash('Uadated successfully   ',['success',current_user.username])
            return redirect(url_for('profile'))
        
        form.username.data=current_user.username
        form.email.data=current_user.email
        return render_template('profile.html',form=form)


@app.route('/post/new',methods=['GET','POST'])
@login_required
def create_post():
    form=PostForm()
    if form.validate_on_submit():
            post=Post(title=form.title.data,content=form.content.data,author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('New Post Successfully Added    ',['info',form.title.data[:30 ]])
            return redirect(url_for('profile'))
       
    
    return render_template('create_post.html',form=form)

@app.route('/post/<int:id>/update',methods=['GET','POST'])
@login_required
def post_update(id):
    post=Post.query.get_or_404(id)
    if current_user==post.author:
        form=PostForm()
        if form.validate_on_submit():
        
            post.title=form.title.data
            post.content=form.content.data
            db.session.commit()
            flash('Post updated ',['success',post.title[:30]])
            return redirect (url_for('post_read',id=post.id))

        form.title.data=post.title
        form.content.data=post.content
        return render_template('post_update.html',form=form)
    else:
        flash('You cannt update another persons post !!!!   ',['danger',current_user.username])
        return redirect(url_for('home'))

@app.route('/post/<int:id>/delete',methods=['GET'])
@login_required
def post_delete(id):
    post=Post.query.get_or_404(id)
    if current_user==post.author:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted  ',['info',' '])
        return redirect(url_for('profile'))
    else:
        flash('You cannt delete another persons post !!!!   ',['danger',current_user.username])
        return redirect(url_for('home'))

