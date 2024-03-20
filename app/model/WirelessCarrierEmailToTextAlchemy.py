from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, text, UniqueConstraint

from app.model.EmailCredsAlchemy import Base, session


class WirelessCarrierEmailText(Base):
    __tablename__ = 'wireless_carrier_email_text'

    id = Column(Integer, primary_key=True, autoincrement=True)
    wireless_carrier = Column(String(200), nullable=False)
    domain = Column(String(200), nullable=False)
    allow_multimedia = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                        default=datetime.now)

    __table_args__ = (
        UniqueConstraint('wireless_carrier', 'domain', 'allow_multimedia', name='unique_carrier'),
        {'mysql_engine': 'InnoDB'}  # You can adjust the MySQL engine as per your preference
    )

    def __str__(self) -> str:
        return f'Wireless Carrier: {self.wireless_carrier}, Domain: {self.domain}, Allow Multimedia: {self.allow_multimedia}, Created At: {self.created_at}'

    def as_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def get_all() -> list:
        return session.query(WirelessCarrierEmailText).all()

    @staticmethod
    def get_all_by_allow_multimedia(allow_multimedia: bool) -> list:
        return session.query(WirelessCarrierEmailText).filter_by(allow_multimedia=allow_multimedia).all()

    @staticmethod
    def create(wireless_carrier: str, domain: str, allow_multimedia: bool):
        try:
            new_record = WirelessCarrierEmailText(
                wireless_carrier=wireless_carrier,
                domain=domain,
                allow_multimedia=allow_multimedia
            )
            session.add(new_record)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f'Error creating new record: {e}')
            raise e

    @staticmethod
    def delete_by_id(id: int):
        try:
            # Construct a delete query based on the ID
            num_deleted = session.query(WirelessCarrierEmailText).filter_by(id=id).delete()
            # Commit the transaction
            session.commit()
            if num_deleted == 0:
                raise ValueError("Record not found")
        except Exception as e:
            session.rollback()
            print(f'Error deleting record: {e}')
            raise e
