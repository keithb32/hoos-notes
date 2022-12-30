from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from scheduler.models import *
from django.core.files import File
import datetime
import unittest

# Create your tests here.
class SignUpTest(TestCase):

	def test_create_account_with_password(self):
		alice = User.objects.create_user(username='alice', password='inw0nd3rland', email='alice@gmail.com')
		allUsers = User.objects.all()
		self.assertTrue(alice in allUsers)

	def test_create_account_without_password(self):
		bob = User.objects.create_user(username='bob', email='bob@gmail.com')
		allUsers = User.objects.all()
		self.assertTrue(bob in allUsers)

	def test_create_account_no_credentials(self):
		self.assertRaises(TypeError, User.objects.create_user)

	def test_create_account_empty_credentials(self):
		self.assertRaises(ValueError, User.objects.create_user, username='', password='', email='')


class LoginTest(TestCase):

	def setUp(self):
		user = User.objects.create_user(username='correctUser', password='c0rrectpassw0rd', email='correctUser@email.com')

	def test_login_correct_credentials(self):	
		logged_in = self.client.login(username='correctUser', password='c0rrectpassw0rd')
		self.assertTrue(logged_in)

	def test_login_incorrect_password(self):
		logged_in = self.client.login(username='correctUser', password='inc0rrectpassw0rd')
		self.assertFalse(logged_in)

	def test_login_incorrect_user(self):
		logged_in = self.client.login(username='incorrectUser', password='c0rrectpassw0rd')
		self.assertFalse(logged_in)

	def test_login_incorrect_credentials(self):
		logged_in = self.client.login(username='incorrectUser', password='inc0rrectpassw0rd')

	def test_login_no_credentials(self):
		logged_in = self.client.login()
		self.assertFalse(logged_in)

	def test_sql_injection(self):
		logged_in = self.client.login(username='\' or 1=1 #', password='', email='')
		self.assertFalse(logged_in)


class LogoutTest(TestCase):

	def setUp(self):
		self.testUser = User.objects.create_user(username='testUser', password='t3stpassw0rd', email='testUser@email.com')
		self.client.login(username='testUser', password='t3stpassw0rd')

	def test_logout_redirect(self):
		# Logout test case adapted from Astik Anand, 7/16/19
		# https://stackoverflow.com/questions/57048654/how-to-assert-the-user-is-logout-in-django-test-testcase
		# Description: makes sure the logout url permanently redirects user
		request = self.client.get('/accounts/logout/')
		self.assertEquals(request.status_code, 302)


class ProfileTest(TestCase):

	def setUp(self):
		self.testUser = User.objects.create_user(username='testUser', password='t3stpassw0rd', email='testUser@email.com')

	def test_profile_automatically_created_for_new_user(self):
		testProfile = Profile.objects.get(user=self.testUser)
		self.assertEquals(testProfile.user, self.testUser)


class StudentClassTest(TestCase):

	def setUp(self):
		testUser1 = User.objects.create_user(username='testUser', password='t3stpassw0rd', email='testUser@email.com')
		testUser2 = User.objects.create_user(username='testUser2', password='t3stpassw0rd2', email='testUser2@email.com')
		
		self.testProfile1 = Profile.objects.get(user=testUser1)
		self.testProfile2 = Profile.objects.get(user=testUser2)
		start1 = datetime.time(11, 0, 0)
		start2 = datetime.time(9, 30, 0)
		end1 = datetime.time(12, 15, 0)
		end2 = datetime.time(10, 45, 0)
		days = [("Tuesday", "Tuesday"), ("Thursday", "Thursday")]
		
		self.course1 = StudentClass.objects.create(class_name="CS 3240", instructor="Sherriff", start_time=start1, end_time=end1, location="Rice 130", days_of_the_week=days)
		self.course1.users.add(self.testProfile1)
		self.course1.users.add(self.testProfile2)

		self.course2 = StudentClass.objects.create(class_name="CS 3330", instructor="Reiss", start_time=start2, end_time=end2, location="Nau 001", days_of_the_week=days)
		self.course2.users.add(self.testProfile1)

	def test_redirect_when_not_logged_in(self):
		request = self.client.get('/createclass')
		self.assertEquals(request.status_code, 302)

	def test_access_when_logged_in(self):
		self.client.login(username='testUser', password='t3stpassw0rd')
		request = self.client.get('/createclass')
		self.assertEquals(request.status_code, 200)

	def test_correct_number_of_students_in_course(self):
		self.assertEquals(self.course1.users.count(), 2)
		self.assertEquals(self.course2.users.count(), 1)

	def test_correct_number_of_courses_for_student(self):
		self.assertEquals(2, self.testProfile1.studentclass_set.all().count())
		self.assertEquals(1, self.testProfile2.studentclass_set.all().count())

	def test_enrolled_students_belong_to_course(self):
		course1_students = self.course1.users.all()
		course2_students = self.course2.users.all()
		self.assertTrue(self.testProfile1 in course1_students and self.testProfile2 in course1_students)

	def test_non_enrolled_student_dont_belong_to_course(self):
		non_enrolled_user = User.objects.create_user(username='notEnrolled', password='n0tenr0lled', email='notEnrolled@email.com')
		non_enrolled_profile = Profile.objects.get(user=non_enrolled_user)
		self.assertFalse(non_enrolled_profile in self.course1.users.all())

	def test_course_belongs_to_enrolled_student(self):
		user1_courses = self.testProfile1.studentclass_set.all()
		user2_courses = self.testProfile2.studentclass_set.all()
		self.assertTrue(self.course1 in user1_courses and self.course2 in user1_courses)
		self.assertTrue(self.course1 in user2_courses)

	def test_course_doesnt_belong_to_non_enrolled_student(self):
		user2_courses = self.testProfile2.studentclass_set.all()
		self.assertFalse(self.course2 in user2_courses)

		
class TodoListItemTest(TestCase):

	def setUp(self):
		testUser1 = User.objects.create_user(username='testUser', password='t3stpassw0rd', email='testUser@email.com')
		testUser2 = User.objects.create_user(username='testUser2', password='t3stpassw0rd2', email='testUser2@email.com')
		
		self.testProfile1 = Profile.objects.get(user=testUser1)
		self.testProfile2 = Profile.objects.get(user=testUser2)

		self.todo_item1a = TodoListItem.objects.create(content="Quiz 1")
		self.todo_item1a.users.add(self.testProfile1)
		self.todo_item1b = TodoListItem.objects.create(content="HW 1")
		self.todo_item1b.users.add(self.testProfile1)

		self.todo_item2a = TodoListItem.objects.create(content="Project")
		self.todo_item2a.users.add(self.testProfile2)

	def test_correct_number_of_todo_items_for_student(self):
		self.assertEquals(2, self.testProfile1.todolistitem_set.all().count())
		self.assertEquals(1, self.testProfile2.todolistitem_set.all().count())

	def test_todo_items_belong_to_correct_profile(self):
		user1_todo_items = self.testProfile1.todolistitem_set.all()
		user2_todo_items = self.testProfile2.todolistitem_set.all()
		self.assertTrue(self.todo_item1a in user1_todo_items and self.todo_item1b in user1_todo_items)
		self.assertTrue(self.todo_item2a in user2_todo_items)

	def test_todo_items_dont_belong_to_incorrect_profile(self):
		user1_todo_items = self.testProfile1.todolistitem_set.all()
		user2_todo_items = self.testProfile2.todolistitem_set.all()
		self.assertFalse(self.todo_item1a in user2_todo_items and self.todo_item1b in user2_todo_items)
		self.assertFalse(self.todo_item2a in user1_todo_items)

'''
class NoteFileTest(TestCase):

	def setUp(self):
		testUser1 = User.objects.create_user(username='testUser1', password='t3stpassw0rd1', email='testUser1@email.com')
		testUser2 = User.objects.create_user(username='testUser2', password='t3stpassw0rd2', email='testUser2@email.com')
		
		self.testProfile1 = Profile.objects.get(user=testUser1)
		self.testProfile2 = Profile.objects.get(user=testUser2)

		start1 = datetime.datetime.now()
		start2 = datetime.datetime.now()

		
		p1 = open('test1.pdf')
		p2 = open('test2.pdf')
		p3 = open('test2.pdf')

		pdf1 = File(p1)
		pdf2 = File(p2)
		pdf3 = File(p3)

		
		self.note1a = NoteFile.objects.create(note = 'Rplot.pdf', title = 'Rplot', upload_time = start1)
		self.note1a.users.add(self.testProfile1)
		self.note1b = NoteFile.objects.create(note = 'HW5.pdf', title = 'HW5', upload_time = start2)
		self.note1b.users.add(self.testProfile1)
		self.noteX = NoteFile.objects.create(note = 'test.pdf', title = 'Test', upload_time = start2)
		
		self.note1a = NoteFile.objects.create(note = pdf1, title = 'test1', upload_time = start1)
		self.note1a.users.add(self.testProfile1)
		self.note1b = NoteFile.objects.create(note = pdf2, title = 'test2', upload_time = start2)
		self.note1b.users.add(self.testProfile1)
		self.noteX = NoteFile.objects.create(note = pdf3, title = 'test3', upload_time = start2)
		

	def test_correct_number_of_files_for_user(self):
		self.assertEquals(2, self.testProfile1.notefile_set.all().count())
		self.assertEquals(0, self.testProfile2.notefile_set.all().count())

	def test_note_items_belong_to_correct_profile(self):
		user1_note_items = self.testProfile1.notefile_set.all()
		self.assertTrue(self.note1a in user1_note_items and self.note1b in user1_note_items)

	def test_note_items_dont_belong_to_incorrect_profile(self):
		user1_note_items = self.testProfile1.notefile_set.all()
		user2_note_items = self.testProfile2.notefile_set.all()
		self.assertFalse(self.note1a in user2_note_items and self.note1b in user2_note_items)
		self.assertFalse(self.noteX in user1_todo_items)

'''	










