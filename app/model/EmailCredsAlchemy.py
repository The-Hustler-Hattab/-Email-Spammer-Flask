from sqlalchemy import create_engine, Column, String, Date, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

from app import app, Constants

# Create a base class for our declarative models
Base = declarative_base()

engine = create_engine(app.config.get(Constants.MYSQL_URL))

Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


class EmailCreds(Base):
    __tablename__ = 'email_creds'

    email = Column(String(500), primary_key=True, nullable=False)
    domain = Column(String(100), nullable=False)
    email_pass = Column(String(500), nullable=False)
    email_host = Column(String(300), nullable=False)
    port = Column(Numeric, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    created_by = Column(String(200), nullable=False)

    def __str__(self) -> str:
        return f'Email: {self.email}, Domain: {self.domain}, Email Pass: {self.email_pass}, Email_host: {self.email_host}, Created At: {self.created_at}, Created By: {self.created_by}'

    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'email_pass'}


    @staticmethod
    def get_all() -> list[object]:
        return session.query(EmailCreds).all()

    @staticmethod
    def create_email(email: str, email_pass: str, port: int, email_host: str, created_by='EMAIL_SERVICE') -> str:
        try:
            domain: str = email.split('@')[1]
        except IndexError:
            domain = email
        try:

            # Create an EmailCreds object
            email_creds = EmailCreds(email=email, domain=domain, email_pass=email_pass, email_host=email_host,
                                     created_by=created_by, port=port)
            # Add the object to the session
            session.add(email_creds)

            # Commit the session to persist the object in the database
            session.commit()
        except Exception as e:
            session.rollback()
            print(f'Error committing to the db: {e}')
            raise e
    @staticmethod
    def get_by_email(sender_email: str) -> object:
        return session.query(EmailCreds).filter(EmailCreds.email.__eq__(sender_email)).first()


