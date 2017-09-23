This Flask app is a way to keep track of the books in your home library.

Before running this code, [create a new Facebook app](https://developers.facebook.com/apps/) and add http://localhost:5000 as the site URL. Create a file in the home directory called `fb_client_secrets.json`, then add your credentials to that document as follows:

```
{
  "web": {
    "app_id": "APP-ID",
    "app_secret": "APP-SECRET-KEY"
  }
}
```

To populate the database with sample information, run `python populate_db.py` before you run the application for the first time. This will create two users and add several books to the list. Run the application with `python views.py`, then head to localhost:5000 in your browser. You should see the list of books already created.

To add new books, create an account by logging in through Facebook. Users can edit and delete their own items, but not ones created by other users.