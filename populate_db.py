from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Book, User


engine = create_engine('sqlite:///library.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session=DBSession()

User1 = User(username="ilikebooks", email="ilikebooks@gmail.com",password="ilikebooks".password_hash)
User2 = User(username="ialsolikebooks", email="ialsolikebooks@gmail.com",password="ialsolikebooks".password_hash)

print "added users"

Book1 = Book(title="Cloud Atlas", author="David Mitchell", genre="Fiction", description="This is a book",user_id=1)
session.add(Book1)
session.commit()

Book2 = Book(title="The Signal and the Noise", author="Nate Silver", genre="Nonfiction", description="This is also a book",user_id=2)
session.add(Book2)
session.commit()

Book3 = Book(title="Harry Potter and the Sorcerer's Stone", author="J.K. Rowling", genre="Fantasy", description="This is a well-loved book",user_id=1)
session.add(Book3)
session.commit()

print "added books"