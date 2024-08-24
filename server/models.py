from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=True)  # Allow nullable phone numbers
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and not phone_number.isdigit():
            raise ValueError("Phone number must be a sequence of digits")
        if phone_number and len(phone_number) != 10:
            raise ValueError("Phone number must have exactly ten digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=True)  # Allow nullable content
    category = db.Column(db.String)
    summary = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title")
        if len(title) > 250:
            raise ValueError("Post title must be at least 250 characters long")
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title must contain clickbait phrases")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary cannot exceed 250 characters")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Post category must be 'Fiction' or 'Non-Fiction'")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'