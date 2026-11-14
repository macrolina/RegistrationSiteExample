# Registration Application Website Example
**Minimalistic website with registration form using database encryption and hashing user data with email authentication.**

Design with a Cybersecurity tactics using Python and its libraries and HTML+CSS.

# Warning
Created project is an educational one, so it has the following simplifications if it is used in commercial works:

1. Key Management's keys(`MASTER_KEY`, `BLIND_INDEX_KEY`, `MAIL_API`) is  by local environment variables (`.env`). In real works production system should delegate key storage and rotation to a dedicated KMS(AWS KMS).
2. Password Safety is controlled by symmetric encryption (`Fernet`), not slow hashing (`bcrypt`/`Argon2`). In real databases it might lead to dangerous encryption of users' password, which might be used elsewhere.

**Do *NOT* use this programm with unchanged code for commercial purposes!**

# Security Features:
- Usage of the Shannon formula of information entropy to check password safety.
- Symmetric Encryption using Fernet from cryptography.
- Fast Hashing for Blind Indexes to find sensitive data.
- Email Authentication to ensure users' ownership of email address.

# Tech Stack
- Core Language: Python 3.12
- GUI/Website: HTMl, CSS
- Web application framework: Flask
- Database & ORM: SQLite, SQLAlchemy
- Cryptography: cryptography.Fernet, hmac, hashlib
- Email Authentication: itsdangerous, flask_mail
- Password checker: math, string
- Other features: dotenv(work with env), os(return data from .env)

# Project Structure

```bash
│   .example.env # example of .env file
│   .gitignore # exclude all unnecessary files
│   database.py # file with all functions related to database work
│   exception.py # exceptions for some unique situations
│   main.py # mail file/starter
│   password_checker.py # file with all functions related to password checking
│   README.md # Documentation
│   requirements.txt # List of required Python packages
│
├───static
│       main.css # Design of main page
│       registration.css # Design of registration and sign in forms 
│
├───template
       main_page.html # main page
       registration.html # registration form
       sign_in.html # sign in form
       verify_email.html # format of authentication email, sent to user
```

# Installation & Setup

1. Clone the repository
```bash
git clone https://github.com/macrolina/RegistrationSiteExample.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python main.py
```