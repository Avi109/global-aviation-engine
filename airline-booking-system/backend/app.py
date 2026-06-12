from flask import Flask
from models import db
from routes import flight_routes
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airline.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'modern-airline-secret-token'

db.init_app(app)
app.register_blueprint(flight_routes)

@app.route("/seed")
def seed_database():
    from models import Flight, User
    db.drop_all()
    db.create_all()  
    
    # Global Hub Matrix
    airlines = ["AA", "DL", "UA", "BA", "EK", "QF", "LH", "SQ"]
    hubs = [
        {"city": "New York", "code": "JFK"},
        {"city": "London", "code": "LHR"},
        {"city": "Tokyo", "code": "HND"},
        {"city": "Paris", "code": "CDG"},
        {"city": "Dubai", "code": "DXB"},
        {"city": "Sydney", "code": "SYD"},
        {"city": "Singapore", "code": "SIN"},
        {"city": "Los Angeles", "code": "LAX"}
    ]
    
    flights_to_add = []
    flight_id_counter = 100
    base_date = datetime.now()
    
    for day in range(14): # Covers a 2-week window
        target_day = base_date + timedelta(days=day)
        
        for _ in range(8):
            origin = random.choice(hubs)
            destination = random.choice(hubs)
            
            while destination["city"] == origin["city"]:
                destination = random.choice(hubs)
                
            airline = random.choice(airlines)
            flight_id_counter += random.randint(1, 9)
            flight_num = f"{airline}-{flight_id_counter}"
            
            hour = random.randint(5, 22)
            minute = random.choice([0, 15, 30, 45])
            departure_dt = datetime(target_day.year, target_day.month, target_day.day, hour, minute)
            
            duration_hours = random.randint(6, 14)
            arrival_dt = departure_dt + timedelta(hours=duration_hours)
            
            price = round(random.uniform(450.00, 1450.00), 2)
            
            flights_to_add.append(
                Flight(
                    flight_number=flight_num,
                    departure_city=origin["city"],
                    arrival_city=destination["city"],
                    departure_time=departure_dt,
                    arrival_time=arrival_dt,
                    base_price=price
                )
            )
            
    db.session.add_all(flights_to_add)

    # Core Test Accounts
    p1 = User(username="flyer123", email="passenger@example.com", is_admin=False)
    p1.set_password("pass123")
    
    a1 = User(username="admin101", email="admin@globalair.com", is_admin=True)
    a1.set_password("admin123")
    
    db.session.add_all([p1, a1])
    db.session.commit()
    return f"Success! 112 dynamic global flights across a 14-day calendar window successfully generated."

if __name__ == "__main__":
    app.run(debug=True, port=8000)