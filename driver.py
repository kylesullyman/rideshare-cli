from helper import get_choice, get_text
from app import db_ops


def login_driver():
    username = get_text("Driver username: ")
    query = """
    SELECT driver_id, first_name
    FROM Driver
    WHERE username = %(username)s;
    """
    row = db_ops.single_row_params(query, {"username": username})
    if row is None:
        print("No driver found with that username.")
        return None
    print(f"\nWelcome back, {row[1]}!")
    return row[0]


def driver_options(driver_id):
    mode = "ON" if is_driver_mode_on(driver_id) else "OFF"
    print(f"""
Driver menu (driver mode is currently {mode}):
    1. View rating
    2. View rides
    3. Activate/Deactivate driver mode
    4. Log out""")
    return get_choice([1, 2, 3, 4])


# view rating through average to skip nulls
def view_rating(driver_id):
    query = """
    SELECT AVG(rating), COUNT(rating)
    FROM Ride
    WHERE driver_id = %(driver_id)s;
    """
    avg_rating, num_ratings = db_ops.single_row_params(
        query, {"driver_id": driver_id})

    if num_ratings == 0:
        print("\nYou don't have any ratings yet.")
    else:
        print(f"\nYour current rating: {float(avg_rating):.2f} / 5 "
              f"(from {num_ratings} rated ride{'s' if num_ratings != 1 else ''})")


def view_rides(driver_id):
    query = """
    SELECT r.ride_id, r.ride_datetime, r.pickup_location,
           r.dropoff_location, ri.username, r.rating
    FROM Ride r
    JOIN Rider ri ON r.rider_id = ri.rider_id
    WHERE r.driver_id = %(driver_id)s
    ORDER BY r.ride_datetime DESC, r.ride_id DESC;
    """
    rides = db_ops.select_query_params(query, {"driver_id": driver_id})

    if not rides:
        print("\nYou haven't given any rides yet.")
        return

    print(f"\nYou have given {len(rides)} ride{'s' if len(rides) != 1 else ''}:\n")
    print(f"{'Ride ID':<8} {'Date/Time':<20} {'Pickup':<25} "
          f"{'Dropoff':<25} {'Rider':<15} Rating")
    print("-" * 101)
    for ride_id, when, pickup, dropoff, rider, rating in rides:
        rating_str = str(rating) if rating is not None else "not rated"
        print(f"{ride_id:<8} {when.strftime('%Y-%m-%d %H:%M'):<20} "
              f"{pickup:<25} {dropoff:<25} {rider:<15} {rating_str}")

# check driver mode
def is_driver_mode_on(driver_id):
    query = """
    SELECT driver_mode
    FROM Driver
    WHERE driver_id = %(driver_id)s;
    """
    return bool(db_ops.single_record_params(query, {"driver_id": driver_id}))


def toggle_driver_mode(driver_id):
    query = """
    UPDATE Driver
    SET driver_mode = NOT driver_mode
    WHERE driver_id = %(driver_id)s;
    """
    db_ops.modify_query_params(query, {"driver_id": driver_id})

    if is_driver_mode_on(driver_id):
        print("\nDriver mode ACTIVATED. Riders can now be matched with you.")
    else:
        print("\nDriver mode DEACTIVATED. You won't receive new rides.")


def driver_menu(driver_id):
    while True:
        choice = driver_options(driver_id)
        if choice == 1:
            view_rating(driver_id)
        elif choice == 2:
            view_rides(driver_id)
        elif choice == 3:
            toggle_driver_mode(driver_id)
        else:
            print("Logged out.")
            break
