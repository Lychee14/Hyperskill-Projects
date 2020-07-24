# Hyperskill-Projects
Simple Banking System
Has an initial menu asking you to create an account, log in or exit from the application.
When creating an account, it adds the account info to the database and while logging in, it reads the data and checks if the combination matches.
Once logged in, it asks whether to see the balance where it reads from the database, add income where it updates the database, log out, delete the account or exit the program.
It also asks if you would like to transfer money to another user where it checks if there is such a user in the database, if it matches the luhn algorith, if it is exactly 16 digits long and if the amount inputed is below the balance of the user. If all is well, the amount is deducted from the user and added to the other user.
