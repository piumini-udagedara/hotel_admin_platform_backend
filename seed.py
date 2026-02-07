from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models.user import User
from app.models.hotel import Hotel
from app.models.room_type import RoomType
from app.models.rate_adjustment import RateAdjustment
from app.core.security import get_password_hash
from datetime import date, timedelta


def seed_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == "admin@hotel.com").first()
        if existing_user:
            print("Database already seeded. Skipping...")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@hotel.com",
            hashed_password=get_password_hash("password123"),
            full_name="Admin User",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("✓ Created admin user: admin@hotel.com / password123")
        
        # Create sample hotels
        hotel1 = Hotel(
            name="Grand Plaza Hotel",
            address="123 Main Street",
            city="New York",
            country="USA",
            description="Luxury hotel in the heart of the city",
            status="active"
        )
        
        hotel2 = Hotel(
            name="Seaside Resort",
            address="456 Beach Road",
            city="Miami",
            country="USA",
            description="Beautiful beachfront resort",
            status="active"
        )
        
        db.add_all([hotel1, hotel2])
        db.commit()
        print(f"✓ Created hotels: {hotel1.name}, {hotel2.name}")
        
        # Create room types for hotel1
        deluxe_room = RoomType(
            hotel_id=hotel1.id,
            name="Deluxe Room",
            description="Spacious room with city view",
            base_rate=150.00,
            capacity=2
        )
        
        suite = RoomType(
            hotel_id=hotel1.id,
            name="Executive Suite",
            description="Luxurious suite with separate living area",
            base_rate=300.00,
            capacity=4
        )
        
        # Create room types for hotel2
        ocean_view = RoomType(
            hotel_id=hotel2.id,
            name="Ocean View Room",
            description="Room with stunning ocean views",
            base_rate=200.00,
            capacity=2
        )
        
        db.add_all([deluxe_room, suite, ocean_view])
        db.commit()
        print(f"✓ Created room types")
        
        # Create rate adjustments
        # Historical adjustment (past)
        past_adjustment = RateAdjustment(
            room_type_id=deluxe_room.id,
            adjustment_amount=20.00,
            effective_date=date.today() - timedelta(days=30),
            reason="Summer season pricing"
        )
        
        # Current adjustment
        current_adjustment = RateAdjustment(
            room_type_id=deluxe_room.id,
            adjustment_amount=30.00,
            effective_date=date.today() - timedelta(days=5),
            reason="Peak season pricing increase"
        )
        
        # Future adjustment
        future_adjustment = RateAdjustment(
            room_type_id=deluxe_room.id,
            adjustment_amount=10.00,
            effective_date=date.today() + timedelta(days=15),
            reason="Post-peak season adjustment"
        )
        
        # Suite adjustment
        suite_adjustment = RateAdjustment(
            room_type_id=suite.id,
            adjustment_amount=50.00,
            effective_date=date.today(),
            reason="High demand period"
        )
        
        db.add_all([past_adjustment, current_adjustment, future_adjustment, suite_adjustment])
        db.commit()
        print(f"✓ Created rate adjustments")
        
        print("\n✅ Database seeded successfully!")
        print("\nLogin credentials:")
        print("  Email: admin@hotel.com")
        print("  Password: password123")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()