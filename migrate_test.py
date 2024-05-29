from app.database import  SessionLocal
from app.models import User, Message, Inbox


def create_sample_data():
    db = SessionLocal()
    try:
        user1 = User(email="example1@example.com", hashed_password="hashed_secret1", full_name="John Doe")
        user2 = User(email="example2@example.com", hashed_password="hashed_secret2", full_name="Jane Doe")

        db.add(user1)
        db.add(user2)
        db.commit()

        message1 = Message(subject="Hello John", body="This is a message for John.", sender_id=user2.id,
                           recipient_id=user1.id)
        message2 = Message(subject="Hello Jane", body="This is a message for Jane.", sender_id=user1.id,
                           recipient_id=user2.id)

        db.add(message1)
        db.add(message2)
        db.commit()

        inbox1 = Inbox(user_id=user1.id, message_id=message1.id, is_read=False)
        inbox2 = Inbox(user_id=user2.id, message_id=message2.id, is_read=False)

        db.add(inbox1)
        db.add(inbox2)
        db.commit()
    finally:
        db.close()



