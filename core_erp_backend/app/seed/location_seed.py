from app.database import SessionLocal
from app.models.masters.state import State
from app.models.masters.city import City


INDIA_STATES_UTS = [
    # States
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",

    # Union Territories
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry",
]


# Optional: small starter city list (you can expand later)
STATE_CITIES = {
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
    "Andhra Pradesh": ["Vijayawada", "Visakhapatnam", "Guntur", "Nellore", "Tirupati"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi", "Belagavi"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "Delhi": ["New Delhi"],
    "West Bengal": ["Kolkata", "Howrah", "Siliguri", "Durgapur"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode"],
    "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur", "Varanasi", "Agra"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela"],
    "Assam": ["Guwahati", "Dibrugarh"],
    "Chhattisgarh": ["Raipur", "Bhilai"],
    "Goa": ["Panaji", "Margao"],
    "Chandigarh": ["Chandigarh"],
    "Puducherry": ["Puducherry"],
    "Jammu and Kashmir": ["Srinagar", "Jammu"],
    "Ladakh": ["Leh"],
}


def seed_states_and_cities():
    db = SessionLocal()
    try:
        print("🌱 Seeding Indian States & UTs...")

        # Insert states/UTs
        for state_name in INDIA_STATES_UTS:
            existing = db.query(State).filter(State.name == state_name).first()
            if not existing:
                db.add(State(name=state_name))

        db.commit()

        # Insert cities
        print("🌱 Seeding starter cities...")
        for state_name, cities in STATE_CITIES.items():
            state = db.query(State).filter(State.name == state_name).first()
            if not state:
                continue

            for city_name in cities:
                existing_city = (
                    db.query(City)
                    .filter(City.name == city_name, City.state_id == state.id)
                    .first()
                )
                if not existing_city:
                    db.add(City(name=city_name, state_id=state.id))

        db.commit()

        print("✅ Done: States + Cities seeded successfully.")

    except Exception as e:
        db.rollback()
        print("❌ Seed failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_states_and_cities()
