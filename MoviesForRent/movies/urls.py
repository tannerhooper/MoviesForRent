from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('proto', views.proto, name='proto'),
    path('movieList', views.movieList, name='movieList'),
    path('login', views.loginView, name='login'),
    path('login/home', views.loginPage, name='submitLogin'),
    path('create-movie', views.createMovie, name='createMovie'),
    path('post-movie', views.postMovieView, name='postMovieView'),
    path('create-user', views.createUser, name='createUser'),
    path('userDetail',views.userDetail, name='userDetail'),
    path('updateUser',views.updateUser,name='updateUser'),
    path('create-user/login', views.createUserLogin, name='createUserLogin'),
    path('logout', views.logoutUser, name='logout'),
    path('init', views.init, name='init'),
    path('nuke', views.nuke, name='nuke'),
    path('borrow/<int:borrow_id>',views.borrow,name='borrow'),
    path('sendBorrowRequest/<int:movie_id>',views.sendBorrowRequest,name='sendBorrowRequest'),
    path('acceptBorrow/<int:borrow_id>',views.acceptBorrow,name='acceptBorrow'),
    path('rejectBorrow/<int:borrow_id>',views.rejectBorrow,name='rejectBorrow'),
    path('moviedetail/<int:movie_id>', views.movieDetail, name='moviedetail'),
    path('returnMovie/<int:movie_id>', views.returnMovie, name='returnMovie'),
]
