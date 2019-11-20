## Built By [Ray Ndegwa](https://github.com/sokkyyy/)

## Description
The app is clone of the popular social media application, Instagram.  

## User Stories
These are the behaviours/features that the application implements for use by a user.

As a user I can:
* Sign in to the application to start using.
* Upload my pictures to the application.
* See my profile with all my pictures.
* Follow other users and see their pictures on my timeline.
* Like a picture and leave a comment on it.

## Specifications
| Behaviour | Input | Output |
| :---------------- | :---------------: | ------------------: |
| Display Login Page if user is not logged in | **On page load** | Login and Registration Options |
| Display following pictures | **Follow Users on their profiles** | Other users pictures|
| View picture details and comments | **Click 'picture name' on image overlay or 'Comment Icon'** | Comment page / Image details page |
| Search for pictures and users |**Enter search term on the navigation bar 'Seach Bar'**|Displays users and images that meet the search term|

## SetUp / Installation Requirements
### Prerequisites
* python3.6
* pip
* postgres database
* virtualenv
* django

### Cloning
* In your terminal:
        
        $ git clone https://github.com/sokkyyy/Instagram.git
        $ cd sokkyyy-the-gallery

## Running the Application
* Creating the virtual environment:

        $ pip install virtualen
        $ virtualenv virtual
        $ source virtual/bin/activate

* Installing Django and other Modules:

        $ pip install -r requirements.txt


* To run the application, in your terminal:


        $ python3.6 manage.py runserver



## Testing the Application
* To run the tests for the class files:

        $ python3.6 manage.py test insta

## Technologies Used
* Python3.6
* Django
* MDbootstrap
* Google Fonts
* FontAwesome
* Postgres SQL

## License
[Ray Ndegwa](https://github.com/sokkyyy/)
