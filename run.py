import usinelib


def main():
    users = [
        {
            "username": "test",
            "friendlyname": "Test Testsson",
            "number": "46123123123"
        }
    ]
    usine_menu = usinelib.UsineMenu()
    debug = True
    weekly_menu, weekly_veg_menu, classic_menu = usine_menu.get_menus()
    if debug:
        for day in weekly_menu:
            print(day['dish'])
        for classic in classic_menu:
            print(classic['dish'])
        for veg in weekly_veg_menu:
            print(veg['dish'])
    usine_menu.notify_users(users, debug)

if __name__ == '__main__':
    main()
