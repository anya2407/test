from datetime import datetime
from app.extensions import db


class Citizen(db.Model):
    __tablename__ = "citizens"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)

    # One citizen can create many needs
    needs = db.relationship("Need", back_populates="citizen")


class Volunteer(db.Model):
    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    skills = db.Column(db.String(255))
    availability = db.Column(db.Boolean, default=True)

    # One volunteer can have many assignments
    assignments = db.relationship("Assignment", back_populates="volunteer")


class ReliefCenter(db.Model):
    __tablename__ = "relief_centers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    current_occupancy = db.Column(db.Integer, default=0)
    status = db.Column(db.String(30), default="AVAILABLE")

    # One relief centre can handle many assignments
    assignments = db.relationship(
        "Assignment",
        back_populates="relief_center"
    )


class Need(db.Model):
    __tablename__ = "needs"

    id = db.Column(db.Integer, primary_key=True)

    citizen_id = db.Column(
        db.Integer,
        db.ForeignKey("citizens.id"),
        nullable=False
    )

    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    urgency = db.Column(db.String(20), default="MEDIUM")
    status = db.Column(db.String(20), default="OPEN")

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships
    citizen = db.relationship(
        "Citizen",
        back_populates="needs"
    )

    attachments = db.relationship(
        "Attachment",
        back_populates="need",
        cascade="all, delete-orphan"
    )

    assignments = db.relationship(
        "Assignment",
        back_populates="need"
    )


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)

    need_id = db.Column(
        db.Integer,
        db.ForeignKey("needs.id"),
        nullable=False
    )

    volunteer_id = db.Column(
        db.Integer,
        db.ForeignKey("volunteers.id"),
        nullable=False
    )

    relief_center_id = db.Column(
        db.Integer,
        db.ForeignKey("relief_centers.id"),
        nullable=False
    )

    status = db.Column(db.String(30), default="ASSIGNED")

    assigned_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    completed_at = db.Column(db.DateTime)

    # Relationships
    need = db.relationship(
        "Need",
        back_populates="assignments"
    )

    volunteer = db.relationship(
        "Volunteer",
        back_populates="assignments"
    )

    relief_center = db.relationship(
        "ReliefCenter",
        back_populates="assignments"
    )


class Attachment(db.Model):
    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)

    need_id = db.Column(
        db.Integer,
        db.ForeignKey("needs.id"),
        nullable=False
    )

    file_url = db.Column(db.String(500), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(100))

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    need = db.relationship(
        "Need",
        back_populates="attachments"
    )