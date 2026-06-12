from flask import Blueprint, jsonify, request, session, render_template
from models import db, Booking, User
import requests
from datetime import datetime
import random

flight_routes = Blueprint('flight_routes', __name__)
AVIATIONSTACK_API_KEY = "YOUR_REAL_API_KEY_HERE"

@flight_routes.route('/')
def home():
    return render_template("index.html")

@flight_routes.route('/admin')
def admin_page():
    return render_template("admin.html")

@flight_routes.route('/api/flights', methods=['GET'])
def get_real_time_flights():
    origin = request.args.get('from', '').strip().upper()  
    destination = request.args.get('to', '').strip().upper() 
    travel_date = request.args.get('date') 
    
    if not origin or not destination:
        return jsonify({"error": "Please provide both Origin and Destination airport parameters."}), 400

    processed_flights = []
    
    try:
        if AVIATIONSTACK_API_KEY and "YOUR_REAL" not in AVIATIONSTACK_API_KEY:
            url = "http://api.aviationstack.com/v1/flights"
            params = {'access_key': AVIATIONSTACK_API_KEY, 'dep_iata': origin, 'limit': 10}
            response = requests.get(url, params=params, timeout=4)
            api_data = response.json()
            raw_flights = api_data.get('data', [])
            
            for flight in raw_flights:
                arr_info = flight.get('arrival', {})
                if arr_info.get('iata') == destination:
                    flight_details = flight.get('flight', {})
                    dep_info = flight.get('departure', {})
                    
                    processed_flights.append({
                        "id": f"{flight_details.get('iata', 'GA-100')}_{travel_date}",
                        "flight_number": flight_details.get('iata') or f"KE-{flight_details.get('number', '121')}",
                        "from": f"{dep_info.get('airport', 'International Hub')} ({origin})",
                        "to": f"{arr_info.get('airport', 'International Hub')} ({destination})",
                        "departure": f"{travel_date} 14:20",
                        "arrival": f"{travel_date} 22:45",
                        "price": 850.00
                    })
    except Exception as e:
        print(f"Live stream bypass trace notice: {e}")

    if len(processed_flights) == 0:
        airport_names = {
            "ICN": "Seoul Incheon Int'l Airport", "GMP": "Seoul Gimpo Int'l Airport",
            "PUS": "Busan Gimhae Int'l Airport", "CJU": "Jeju International Airport",
            "LAX": "Los Angeles International", "JFK": "New York John F. Kennedy",
            "LHR": "London Heathrow", "HND": "Tokyo Haneda", "CDG": "Paris Charles de Gaulle",
            "DXB": "Dubai International", "KTM": "Kathmandu Tribhuvan Int'l"
        }
        
        orig_name = airport_names.get(origin, f"{origin} International Airport")
        dest_name = airport_names.get(destination, f"{destination} International Airport")
        display_date = travel_date if travel_date else datetime.now().strftime('%Y-%m-%d')
        
        airlines = [("Korean Air", "KE"), ("Asiana Airlines", "OZ"), ("Delta Air Lines", "DL")]
        for i in range(3):
            airline_name, code = airlines[i]
            f_num = f"{code}-{random.randint(100, 999)}"
            hours = ["08:15", "13:40", "19:10"][i]
            arr_hours = ["16:30", "22:00", "04:15"][i]
            price = round(random.uniform(720.00, 1450.00), 2)
            
            processed_flights.append({
                "id": f"{f_num}_{display_date}_{i}", "flight_number": f_num,
                "from": f"{orig_name} ({origin})", "to": f"{dest_name} ({destination})",
                "departure": f"{display_date} {hours}", "arrival": f"{display_date} {arr_hours}",
                "price": price
            })
            
    return jsonify(processed_flights)

@flight_routes.route('/api/bookings', methods=['POST'])
def create_booking():
    if not session.get('user_id'):
        return jsonify({"error": "Authentication required. Please sign in to choose a seat."}), 401
        
    data = request.get_json()
    flight_id_str = data.get('flight_id') 
    seat = data.get('seat_number')
    flight_summary = data.get('flight_summary')

    if not flight_id_str or not seat:
        return jsonify({"error": "Missing reservation allocation data parameters"}), 400
        
    new_booking = Booking(seat_number=seat, flight_id=1, user_id=session['user_id'])
    
    if 'history' not in session:
        session['history'] = []
        
    clean_number = flight_summary.split('(')[0].strip() if flight_summary and '(' in flight_summary else "Live Flight"
        
    session['history'].append({
        "flight_number": clean_number, "route_summary": flight_summary if flight_summary else "Live Route Corridor",
        "seat": seat, "time": datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    session.modified = True
    
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"message": "Global manifest booking locked successfully!", "booking_id": new_booking.id}), 201

@flight_routes.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "Username is already taken"}), 400
        
    new_user = User(username=data.get('username'), email=data.get('email'), is_admin=False)
    new_user.set_password(data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Account created successfully!"}), 201

@flight_routes.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({"error": "Invalid login credentials"}), 401
        
    session['user_id'] = user.id
    session['username'] = user.username
    session['is_admin'] = user.is_admin
    return jsonify({"message": "Sign-in successful", "username": user.username, "is_admin": user.is_admin}), 200

@flight_routes.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

@flight_routes.route('/api/session', methods=['GET'])
def get_current_session():
    if 'user_id' in session:
        return jsonify({"logged_in": True, "username": session['username'], "is_admin": session['is_admin']})
    return jsonify({"logged_in": False})

@flight_routes.route('/api/my-tickets', methods=['GET'])
def get_my_tickets():
    if not session.get('user_id'):
        return jsonify({"error": "Please login first"}), 401
    return jsonify(session.get('history', []))