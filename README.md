This Flask app is a way to keep track of the books in your home library.

To populate the database with sample information, run ```python populate_db.py``` before you run the application for the first time. This will create two users and add several books to the list. Run the application with ```python views.py```, then head to localhost:5000 in your browser. You should see the list of books already created.

To add new books, create an account. Users can edit and delete their own items, but not ones created by other users.