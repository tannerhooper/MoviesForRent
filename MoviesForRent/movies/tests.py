from django.test import TestCase
from .models import Movie, Borrow
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import requests

# Create your tests here.
# Classes must inherit TestCase
# test functions must start with test


# test crucial api endpoint to see if they work
class ApiTestCase(TestCase):
	def test_movie_search(self):
		r= requests.get('https://api.themoviedb.org/3/search/movie?api_key=633b13af41578573e167d76d0d102ab0&language=en-US&query=lego&include_adult=false')
		self.assertEqual(r.status_code,200)
		
	def test_movie_detail(self):
		r= requests.get('https://api.themoviedb.org/3/movie/27?api_key=633b13af41578573e167d76d0d102ab0&language=en-US&append_to_response=release_dates')
		self.assertEqual(r.status_code,200)
		
class MovieTestCase(TestCase):
	def setUp(self):
		Movie.objects.create(title="TestMovie",
        genre="Sci Fi, Action, Adventure",
        length="120",
        rating="PG",
        owner="Him",
        possession="Other him",
        available=True,
        condition=f"good",
        image="imageurl.png",
        synopsis=f"synopsis here")

	def test_movie_rating(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.rating,"PG")

	def test_movie_title(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.title,"TestMovie")

	def test_movie_availibility(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.available,True)

	def test_movie_genre(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.genre,"Sci Fi, Action, Adventure")

	def test_movie_length(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.length,"120")

	def test_movie_owner(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.owner,"Him")

	def test_movie_possession(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.possession,"Other him")

	def test_movie_condition(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.condition,"good")

	def test_movie_image(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.image,"imageurl.png")

	def test_movie_synopsis(self):
		m =Movie.objects.get(title="TestMovie")
		self.assertEqual(m.synopsis,"synopsis here")

class BorrowTestCase(TestCase):
	def setUp(self):
		Borrow.objects.create(terms="Terms",
			message="Can plz have?",
			owner="OwnerUserName",
			borrower="BorrowerUserName",
			movieId="66")

	def test_owner(self):
		b = Borrow.objects.get(terms="Terms")
		self.assertEqual(b.owner, "OwnerUserName")
	
	def test_borrower(self):
		b = Borrow.objects.get(terms="Terms")
		self.assertEqual(b.borrower, "BorrowerUserName")

	def test_borrow_terms(self):
		b = Borrow.objects.get(terms="Terms")
		self.assertEqual(b.terms, "Terms")

	def test_borrow_message(self):
		b = Borrow.objects.get(terms="Terms")
		self.assertEqual(b.message, "Can plz have?")

	def test_movieId(self):
		b = Borrow.objects.get(terms="Terms")
		self.assertEqual(b.movieId, "66")

class UserTestCase(TestCase):
	def setUp(self):
		user = User.objects.create(username="TestPerson1",
			first_name="Test",
			last_name="Person",
			email="testperson@test.com",
			password="password1")
		user.set_password('password1')
		user.save()
	
	def test_username(self):
		user = User.objects.get(username="TestPerson1")
		self.assertEqual(user.username, "TestPerson1")

	def test_name(self):
		user = User.objects.get(username="TestPerson1")
		self.assertEqual(user.first_name, "Test")
		self.assertEqual(user.last_name, "Person")
	
	def test_email(self):
		user = User.objects.get(username="TestPerson1")
		self.assertEqual(user.email, "testperson@test.com")
	
	def test_authentication(self):
		user = User.objects.get(username="TestPerson1")
		test = authenticate(username=user.username, password="password1")
		self.assertIsNotNone(test)