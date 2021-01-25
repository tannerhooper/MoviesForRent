from django.shortcuts import render, reverse, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from random import randint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Movie
from .models import Borrow
from django.core.mail import send_mail
import os

#this requires the user to be logged in or redirects to the login page.

@login_required 
def home(request):
    lend = Movie.objects.filter(owner=request.user.username).filter(available=False)
    borrow = Movie.objects.filter(possession=request.user.username).filter(available=False)
    userData={"user": request.user,"borrowed":borrow,"lent":lend,}
    context={"userData":userData}
    template=loader.get_template('movies/home.html')
    return HttpResponse(template.render(context,request))
    
@login_required
def userDetail(request):
    movies = Movie.objects.filter(owner=request.user.username)
    userData={"user": request.user,"movies":movies,}
    context={"userData":userData}
    template=loader.get_template('movies/userDetail.html')
    return HttpResponse(template.render(context,request))

def updateUser(request):
    lend = Movie.objects.filter(owner=request.user.username).filter(available=False)
    borrow = Movie.objects.filter(possession=request.user.username).filter(available=False)
    userObject =  User.objects.get(username=request.user.username)
    userObject.username =request.POST['username']
    userObject.email =request.POST['email']
    userObject.first_name = request.POST['first_name']
    userObject.last_name = request.POST['last_name']
    userObject.save()
    login(request, userObject)
    userData={"user": userObject,"borrowed":borrow,"lent":lend,}
    template=loader.get_template('movies/userDetail.html')
    context={"userData":userData}
    return redirect(home)
    #return HttpResponse(template.render(context,request))

def proto(request):
    context ={"name":"The Man"}
    template =loader.get_template('movies/proto.html')
    return HttpResponse(template.render(context,request))

def movieList(request):
    movies = Movie.objects.all()
    context ={"movies":movies}
    template =loader.get_template('movies/movieList.html')
    return HttpResponse(template.render(context,request))
    
def movieDetail(request, movie_id):
    try:
    	movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
    	raise Http404("Movie not found")
    template =loader.get_template('movies/moviedetail.html')
    action = 'Borrow'
    if not movie.available and request.user.username == movie.possession:
        action = 'Return'
    context = {'movie': movie, 'action': action}
    return HttpResponse(template.render(context, request))

def loginView(request):
    template =loader.get_template('movies/login.html')
    context = {'error': False}
    return HttpResponse(template.render(context, request))

def loginPage(request):
    lend = Movie.objects.filter(owner=request.user.username).filter(available=False)
    borrow = Movie.objects.filter(possession=request.user.username).filter(available=False)
    usrname = request.POST['username']
    psswrd = request.POST['password']
    user = authenticate(username=usrname, password=psswrd)
    if user is not None:
        login(request, user)
        userData={"user": user,"borrowed":borrow,"lent":lend,}
        context={"userData":userData}
        template=loader.get_template('movies/home.html')
        #return HttpResponse(template.render(context,request))
        return HttpResponseRedirect(reverse('home'))
    else:
        template=loader.get_template('movies/login.html')
        context = {'error': True}
        return HttpResponse(template.render(context, request))

def createUser(request):
    template=loader.get_template('movies/create-user.html')
    context = {'error': 'unknown error'}
    return HttpResponse(template.render(context, request))

def createUserLogin(request):
    lend = Movie.objects.filter(owner=request.user.username).filter(available=False)
    borrow = Movie.objects.filter(possession=request.user.username).filter(available=False)
    userObject =  User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['confirm_password'])
    userObject.first_name = request.POST['first_name']
    userObject.last_name = request.POST['last_name']
    userObject.save()
    login(request, userObject)
    userData={"user": userObject,"borrowed":borrow, "lent":lend,}
    template=loader.get_template('movies/home.html')
    context={"userData":userData}
    return HttpResponse(template.render(context,request))

def logoutUser(request):
    logout(request)
    template=loader.get_template('movies/login.html')
    context = {'error': False}
    return HttpResponse(template.render(context, request))

def postMovieView(request):
    context={"user":request.user}
    template=loader.get_template('movies/postMovie.html')
    return HttpResponse(template.render(context,request))
    
def createMovie(request):
    movie=Movie(title=request.POST['title'],
    genre=request.POST['genre'],
    length=request.POST['length'],
    rating=request.POST['rating'],
    owner=request.user.username,
    possession=request.user.username,
    #possession=request.POST['possession'],
    available=request.POST['available'],
    condition=request.POST['condition'],
    image=request.POST['image'],
    synopsis=request.POST['synopsis'])
    movie.save()
    return HttpResponseRedirect(reverse('home'))

def init(request):
    try:
        userObject = User.objects.get(username="dummyUser")
    except:
        userObject =  User.objects.create_user(username="dummyUser", email="tannerhooper@yahoo.com", password="dummy",
            first_name="Dummy",last_name="User")
        userObject.save()
    for i in range(9):
        m = Movie(title="Star Wars " + str(i+1),
        genre="Sci Fi, Action, Adventure",
        length="120",
        rating="PG",
        owner=userObject.username,
        possession=userObject.username,
        available=True,
        condition=f"Good",
        image="",
        synopsis=f"Such awesomeness movie")
        m.save()
    return HttpResponseRedirect(reverse('home'))

def nuke(request):
    for m in Movie.objects.all():
        m.delete()
    for b in Borrow.objects.all():
        b.delete()
    return redirect('home')

def borrow(request,borrow_id):
    borrowObject =  Borrow.objects.get(id=borrow_id)
    movieObject =  Movie.objects.get(id=borrowObject.movieId)
    template=loader.get_template('movies/borrow.html')
    context = {'id':borrow_id,'borrow':borrowObject,'movie':movieObject,'userData':{"user": request.user,}}
    return HttpResponse(template.render(context, request))

def sendBorrowRequest(request, movie_id):
    movieObject = Movie.objects.get(id=movie_id)
    userObject = User.objects.get(username=movieObject.owner)
    template=loader.get_template('movies/moviedetail.html')
    message = None
    if request.user.username == movieObject.owner:
        message = 'You already own this movie'
    if not movieObject.available:
        message = "This movie is not available."
    if message is not None:
        context = {'movie': movieObject, 'action': 'Borrow', 'status': False, 'message': message}
        return HttpResponse(template.render(context, request))

    borrowObject = Borrow(owner=userObject.username,
        terms="",
        borrower=request.user.username,
        borrowerEmail=request.user.email,
        message=", I am interesting in renting your movie!",
        movieId=movie_id
    )
    borrowObject.save()
    subject = request.user.username + " wants to borrow " + movieObject.title + " from you!"
    to = userObject.email
    emailFrom = request.user.email
    developmentLink = 'https://rent-a-movie-231721.appspot.com/borrow/'  + str(borrowObject.id)
    if os.getenv('GAE_INSTANCE'):
        pass
    else:
        developmentLink = 'http://localhost:8000/borrow/' + str(borrowObject.id)
    message = request.user.username + " would like to borrow " + movieObject.title + " from you.\n\n Click on this link to accept/reject " + developmentLink
    status = True
    try:
        send_mail(
            subject,
            message,
            emailFrom, 
            [to, 'hawkeye.zach@gmail.com'],
            fail_silently=False
        )
    except:
        status = False
    template=loader.get_template('movies/moviedetail.html')
    context = {'movie': movieObject, 'action': 'Borrow', 'status': status}
    return HttpResponse(template.render(context, request))
    
def acceptBorrow(request,borrow_id):
    borrowObject =  Borrow.objects.get(id=borrow_id)
    movieObject = Movie.objects.get(id=borrowObject.movieId)
    movieObject.available=False
    movieObject.possession=borrowObject.borrower
    borrowObject.terms= request.POST['terms']
    borrowObject.message= request.POST['message']
    borrowObject.save()
    movieObject.save()

    subject = request.user.username + " has accepted your borrow request for " + movieObject.title + "!"
    to = borrowObject.borrowerEmail
    emailFrom = request.user.email

    message = "Congrats " + borrowObject.borrower + ", " + request.user.username + " has accepted your borrow request for " + movieObject.title + "!"
    message1 = "\n\n Terms: " + borrowObject.terms
    message2 = "\n\n Message: " + borrowObject.message
    message3 = "\n\n Email them now at " + request.user.email + " to obtain the movie"
    message = message + message1 + message2 + message3
    status = True
    try:
        send_mail(
            subject,
            message,
            emailFrom, 
            [to, 'hawkeye.zach@gmail.com'],
            fail_silently=False
        )
    except:
        status = False

    template=loader.get_template('movies/BorrowRequestFeedBack.html')
    context = {'movie': movieObject, 'accepted': True}
    return HttpResponse(template.render(context, request))
    
def rejectBorrow(request,borrow_id):
    #send email to borrower indicating rejetion
    borrowObject = Borrow.objects.get(id=borrow_id)
    borrowObject.message= request.POST['message']
    borrowObject.save()
    movieObject = Movie.objects.get(id=borrowObject.movieId)

    subject = request.user.username + " has rejected your borrow request for " + movieObject.title
    to = borrowObject.borrowerEmail
    emailFrom = request.user.email

    developmentLink = 'https://rent-a-movie-231721.appspot.com/moviedetail/'  + str(movieObject.id)
    if os.getenv('GAE_INSTANCE'):
        pass
    else:
        developmentLink = 'http://localhost:8000/moviedetail/' + str(movieObject.id)

    message = request.user.username + " has rejected your borrow request for " + movieObject.title
    message1 = "\n\n Message: " + borrowObject.message
    message2 = "\n\n Visit " + developmentLink + " to re-request the movie"
    message = message + message1 + message2
    status = True
    try:
        send_mail(
            subject,
            message,
            emailFrom, 
            [to, 'hawkeye.zach@gmail.com'],
            fail_silently=False
        )
    except:
        status = False

    template=loader.get_template('movies/BorrowRequestFeedBack.html')
    context = {'movie': movieObject, 'accepted': False}
    return HttpResponse(template.render(context, request))

def returnMovie(request, movie_id):
    movieObject = Movie.objects.get(id=movie_id)
    template =loader.get_template('movies/moviedetail.html')
    if request.user.username == movieObject.owner:
        context = {'movie': movieObject, 'action': 'Return', 'status': False, 'message': 'You cannot return a movie you do not have'}
        return HttpResponse(template.render(context, request))
    movieObject.available = True
    movieObject.possession = movieObject.owner
    movieObject.save()
    userObject = User.objects.get(username=movieObject.owner)

    subject = request.user.username + " has officially returned your movie " + movieObject.title
    to = userObject.email
    emailFrom = request.user.email

    message = "Congrats " + movieObject.owner + ", " + request.user.username + " has officially returned your movie " + movieObject.title
    status = True
    try:
        send_mail(
            subject,
            message,
            emailFrom, 
            [to, 'hawkeye.zach@gmail.com'],
            fail_silently=False
        )
    except:
        status = False

    context = {'movie': movieObject, 'action': 'Return', 'status': True}
    return HttpResponse(template.render(context, request))
