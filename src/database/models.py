from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass




class Donor(Base):
    __tablename__ = "donors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    blood_type: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    last_donation_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    donations: Mapped[list["Donation"]] = relationship(
        back_populates="donor"
    )

    matches: Mapped[list["Match"]] = relationship(
        back_populates="donor"
    )




class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    blood_type: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    hospital: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    requests: Mapped[list["BloodRequest"]] = relationship(
        back_populates="patient"
    )




class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False
    )

    blood_type: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    units_required: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    urgency: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    hospital: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Pending",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    patient: Mapped["Patient"] = relationship(
        back_populates="requests"
    )

    matches: Mapped[list["Match"]] = relationship(
        back_populates="request"
    )




class Donation(Base):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    donor_id: Mapped[int] = mapped_column(
        ForeignKey("donors.id"),
        nullable=False
    )

    donation_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    blood_type: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    units_donated: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Completed",
        nullable=False
    )

    # Relationships
    donor: Mapped["Donor"] = relationship(
        back_populates="donations"
    )




class BloodInventory(Base):
    __tablename__ = "blood_inventory"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    blood_type: Mapped[str] = mapped_column(
        String(3),
        unique=True,
        nullable=False
    )

    units_available: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    low_stock_threshold: Mapped[int] = mapped_column(
        Integer,
        default=10,
        nullable=False
    )

    last_updated: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )



class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    request_id: Mapped[int] = mapped_column(
        ForeignKey("blood_requests.id"),
        nullable=False
    )

    donor_id: Mapped[int] = mapped_column(
        ForeignKey("donors.id"),
        nullable=False
    )

    compatibility_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    distance_km: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    ranking_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Suggested",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    donor: Mapped["Donor"] = relationship(
        back_populates="matches"
    )

    request: Mapped["BloodRequest"] = relationship(
        back_populates="matches"
    )