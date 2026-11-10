from helper import get_choice, get_text
from app import db_ops


def login_rider():
    username = get_text("Rider username: ")
    query = """
    SELECT rider_id, first_name
    FROM Rider
    WHERE username = %(username)s;
    """
    row = db_ops.single_row_params(query, {"username": username})
    if row is None:
        print("No rider found with that username.")
        return None
    print(f"\nWelcome back, {row[1]}!")
    return row[0]


def rider_options():
    print("""
Rider menu:
    1. View rides
    2. Find a driver
    3. Rate my driver
    4. Log out""")
    return get_choice([1, 2, 3, 4])


def view_rider_rides(rider_id):
    query = """
    SELECT r.ride_id, r.ride_datetime, r.pickup_location,
           r.dropoff_location, d.username, r.rating
    FROM Ride r
    JOIN Driver d ON r.driver_id = d.driver_id
    WHERE r.rider_id = %(rider_id)s
    ORDER BY r.ride_datetime DESC, r.ride_id DESC;
    """
    rides = db_ops.select_query_params(query, {"rider_id": rider_id})

    if not rides:
        print("\nYou haven't taken any rides yet.")
        return

    print(f"\nYou have taken {len(rides)} ride{'s' if len(rides) != 1 else ''}:\n")
    print(f"{'Ride ID':<8} {'Date/Time':<20} {'Pickup':<25} "
          f"{'Dropoff':<25} {'Driver':<15} Rating")
    print("-" * 101)
    for ride_id, when, pickup, dropoff, driver, rating in rides:
        rating_str = str(rating) if rating is not None else "not rated"
        print(f"{ride_id:<8} {when.strftime('%Y-%m-%d %H:%M'):<20} "
              f"{pickup:<25} {dropoff:<25} {driver:<15} {rating_str}")


def find_driver(rider_id):
    query = """
    SELECT driver_id, first_name, last_name
    FROM Driver
    WHERE driver_mode = TRUE
    ORDER BY RAND()
    LIMIT 1;
    """
    driver = db_ops.single_row_params(query, {})
    if driver is None:
        print("\nSorry, no drivers are available right now. Try again later.")
        return

    driver_id, first_name, last_name = driver
    print(f"\nYou've been matched with {first_name} {last_name}!")

    pickup = get_text("Pick up location: ")
    dropoff = get_text("Drop off location: ")

    # ride_datetime defaults to CURRENT_TIMESTAMP, rating starts NULL
    insert = """
    INSERT INTO Ride (rider_id, driver_id, pickup_location, dropoff_location)
    VALUES (%(rider_id)s, %(driver_id)s, %(pickup)s, %(dropoff)s);
    """
    ride_id = db_ops.modify_query_params(insert, {
        "rider_id": rider_id,
        "driver_id": driver_id,
        "pickup": pickup,
        "dropoff": dropoff
    })
    print(f"\n{first_name} drove you from {pickup} to {dropoff}. "
          f"(Ride ID {ride_id})")


# ride_id=None returns the rider's most recent ride.
# filtering on rider_id means riders can only rate their own rides.
def get_rider_ride(rider_id, ride_id=None):
    query = """
    SELECT r.ride_id, r.ride_datetime, r.pickup_location,
           r.dropoff_location, d.first_name, d.last_name, r.rating
    FROM Ride r
    JOIN Driver d ON r.driver_id = d.driver_id
    WHERE r.rider_id = %(rider_id)s
    """
    params = {"rider_id": rider_id}
    if ride_id is None:
        query += " ORDER BY r.ride_datetime DESC, r.ride_id DESC LIMIT 1;"
    else:
        query += " AND r.ride_id = %(ride_id)s;"
        params["ride_id"] = ride_id
    return db_ops.single_row_params(query, params)


def confirm_ride(ride):
    ride_id, when, pickup, dropoff, first_name, last_name, rating = ride
    print(f"""
Ride ID:  {ride_id}
Date:     {when.strftime('%Y-%m-%d %H:%M')}
From:     {pickup}
To:       {dropoff}
Driver:   {first_name} {last_name}
Rating:   {rating if rating is not None else 'not rated'}""")
    print("""Is this the ride you want to rate?
    1. Yes
    2. No""")
    return get_choice([1, 2]) == 1


def ask_for_ride(rider_id):
    while True:
        ride_id = get_text("Enter the ride ID of the ride you want to rate: ")
        if not ride_id.isdigit():
            print("Ride ID must be a number.")
            continue
        ride = get_rider_ride(rider_id, int(ride_id))
        if ride is None:
            print("You don't have a ride with that ID.")
            continue
        return ride


def rate_driver(rider_id):
    ride = get_rider_ride(rider_id)
    if ride is None:
        print("\nYou haven't taken any rides yet.")
        return

    print("\nYour most recent ride:")
    while not confirm_ride(ride):
        ride = ask_for_ride(rider_id)

    if ride[6] is not None:
        print(f"This ride is already rated {ride[6]}. "
              "Your new rating will replace it.")

    print("Rate your driver from 1 to 5:")
    rating = get_choice([1, 2, 3, 4, 5])

    update = """
    UPDATE Ride
    SET rating = %(rating)s
    WHERE ride_id = %(ride_id)s AND rider_id = %(rider_id)s;
    """
    db_ops.modify_query_params(update, {
        "rating": rating,
        "ride_id": ride[0],
        "rider_id": rider_id
    })
    print(f"\nThanks! You rated {ride[4]} {rating}/5.")


def rider_menu(rider_id):
    while True:
        choice = rider_options()
        if choice == 1:
            view_rider_rides(rider_id)
        elif choice == 2:
            find_driver(rider_id)
        elif choice == 3:
            rate_driver(rider_id)
        else:
            print("Logged out.")
            break
