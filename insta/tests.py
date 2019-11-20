from django.test import TestCase
from .models import User,Profile,Image

# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.new_user = User(full_name="ray ndegwa",username="ray",email="ray@gmail.com",password="1234")
    
    def test_instance(self):
        self.assertTrue(isinstance(self.new_user,User))

class ProfileTest(TestCase):
    def setUp(self):
        self.new_user = User(full_name="ray ndegwa",username="ray",email="ray@gmail.com",password="1234")
        self.new_profile = Profile(profile_photo="ray.jpeg",bio="Add a bio",user=self.new_user)
    
    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))

class ImageTest(TestCase):
    def setUp(self):
        self.new_user = User(full_name="ray ndegwa",username="ray",email="ray@gmail.com",password="1234")
        self.new_profile = Profile(profile_photo="ray.jpeg",bio="Add a bio",user=self.new_user)
        self.new_image = Image(image="beach.jpeg",name="ray",caption="ray at the beach",profile=self.new_profile)
    
    def test_instance(self):
        self.assertTrue(isinstance(self.new_image,Image))