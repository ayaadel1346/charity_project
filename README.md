Crowdfunding Web Platform for Egypt
Overview

This web platform aims to facilitate fundraising projects in Egypt by providing a user-friendly interface for both project creators and donors. It incorporates features such as authentication, project creation, user profiles, project viewing, and administrative functionalities.


Team Members

    Aya Adel Mohammed: Implemented login page with password reset, registration with activation mail, and homepage with search ,category listing ,list similar projects based on tags of project selected ,rate project feature , comment and report comment feature , admin panel home page ,crud operation at( featured project , categories , user profile ) , base templates 
    
    Shaimaa Khalid: Developed user profile functionality,allow update user profile & delete account with password confirmation , project cancellation feature at user interface , and CRUD operations for (tags , reports ,rate) Also worked as tester .
    
    Rehab Kosbar: Designed the view project page, implemented project slideshow image , donation feature with PayPal integration, report project feature  and crud operation for (donation , comment , reply).

    
    Fatma Mahmoud: Implemented project creation, including multiple tags and images and CRUD operations for (projects ,project cancellation and  project pictures).

Features Implemented

    Authentication System: Registration with activation email, login, forgot password, and user profile management.
    Projects: Creation of fundraising campaigns with various details like title, details, category, target amount, and start/end time.
    Homepage: Slider showcasing top-rated projects, list of nearby projects,list of featured projects selected by admin , categories, and a search bar.
    Admin View: Ability to create categories, select featured projects, and manage user accounts.
    Project Viewing: Detailed project pages displaying project information, images, donations, comments, and related projects.
    Donations: Integration with PayPal for secure donations to projects.
    Rating and Reporting: Users can rate projects, report inappropriate projects/comments, and comment on projects.
    Project Management: Project creators can cancel projects if the donation threshold is not met.

Technologies Used

    Frontend: HTML, CSS, JavaScript, Bootstrap
    Backend: Django (Python)
    Database: mysql
    Payment Integration: PayPal API
    

Installation and Usage

    Clone the repository: git clone <repository_url>
    Install dependencies: pip install -r requirements.txt
    Set up the database: python manage.py migrate
    Run the server: python manage.py runserver

Future Improvements

    Implementing additional payment gateways for donations.
    Enhancing project recommendation algorithms based on user preferences.
    Improving user interface and user experience design.
    Scaling the platform for higher traffic and more users.

Contributors

    Aya Adel Mohammed
    Shaimaa Khalid
    Rehab Kosbar
    Fatma Mahmoud
