from datetime import datetime
from typing import List
from sqlalchemy import Float, Index, String, Integer, DateTime, ForeignKey, func, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from .db_enums import UserGender, UserRole

class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

class PhysicalActivityInfo(Base):
    __tablename__ = "physical_activity_info"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    activity_ratio: Mapped[float] =  mapped_column(Float, nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="activity_info")

class UserWeightLog(Base):
    __tablename__ = "user_weight_log"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="weight_log")

class User(Base):
    __tablename__ = "user"

    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    gender: Mapped[UserGender] = mapped_column(Enum(UserGender))    
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    height:  Mapped[float] = mapped_column(Float, nullable=False)
    birth_year: Mapped[int] = mapped_column(Integer, nullable=False)
    physical_activity: Mapped[int] = mapped_column(Integer, 
                                                   ForeignKey("physical_activity_info.id", ondelete="CASCADE"), 
                                                   nullable=False)

    activity_info: Mapped["PhysicalActivityInfo"] = relationship(back_populates="users")
    products: Mapped[List["Product"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    diary_entries: Mapped[List["Diary"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    weight_log: Mapped[List["UserWeightLog"]] = relationship(back_populates="user", 
                                                             cascade="all, delete-orphan",
                                                             order_by="UserWeightLog.timestamp")
    
    @property
    def daily_calorie_norm(self) -> float:
        if not self.activity_info:
            return 0.0

        age = datetime.now().year - self.birth_year  
        if self.gender == UserGender.Male:
            bmr = (self.weight * 10) + (self.height * 6.25) - (age * 5) + 5
        elif self.gender == UserGender.Female:
            bmr = (self.weight * 10) + (self.height * 6.25) - (age * 5) - 161

        return bmr * self.activity_info.activity_ratio


class Product(Base):
    __tablename__ = "product"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    proteins: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrates: Mapped[float] = mapped_column(Float, nullable=False)
    fats: Mapped[float] = mapped_column(Float, nullable=False)
    photo_path: Mapped[str] = mapped_column(nullable=False)
    photo_vector: Mapped[list[float]] = mapped_column(Vector(dim=512))
    is_accepted: Mapped[bool] = mapped_column(default=False, server_default="false", nullable=False)

    user: Mapped["User"] = relationship(back_populates="products")
    diary_entries: Mapped[List["Diary"]] = relationship(back_populates="product")

    __table_args__ = (
        Index(
            'ix_product_photo_vector_hnsw',
            'photo_vector',
            postgresql_using='hnsw',
            postgresql_with={'m': 16, 'ef_construction': 64},
            postgresql_ops={'photo_vector': 'vector_l2_ops'}
        ),

    )

class Diary(Base):
    __tablename__ = "diary"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id", ondelete="SET NULL"), nullable=True, index=True)
    
    product_name_snapshot: Mapped[str] = mapped_column(String(150), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    calories_consumed: Mapped[float] = mapped_column(Float, nullable=False)
    proteins_consumed: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrates_consumed: Mapped[float] = mapped_column(Float, nullable=False)
    fats_consumed: Mapped[float] = mapped_column(Float, nullable=False)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    user: Mapped["User"] = relationship(back_populates="diary_entries")
    product: Mapped["Product"] = relationship(back_populates="diary_entries")