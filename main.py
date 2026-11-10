from app import db_ops, startScreen, start_options, create_account
from driver import login_driver, driver_menu
from rider import login_rider, rider_menu


def main():
    startScreen()
    while True:
        choice = start_options()
        if choice == 1:
            account_type, new_id = create_account()
            if account_type == "driver":
                driver_menu(new_id)
            else:
                rider_menu(new_id)
        elif choice == 2:
            rider_id = login_rider()
            if rider_id is not None:
                rider_menu(rider_id)
        elif choice == 3:
            driver_id = login_driver()
            if driver_id is not None:
                driver_menu(driver_id)
        else:
            print("Goodbye!")
            break

    db_ops.destructor()


if __name__ == "__main__":
    main()
