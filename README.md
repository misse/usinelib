# usinelib

## Usage
``` 
import usinelib

users = [
    {
        "username": "test",
        "friendlyname": "Test Testsson",
        "number": "46123123123"
    }
]


def main():
    usineMenu = usinelib.usineMenu()
    debug = True
    weeklyMenu, weeklyVegMenu, classicMenu = usineMenu.getMenus()
    if debug:
        for day in weeklyMenu:
            print(day['dish'])
        for classic in classicMenu:
            print(classic['dish'])
        for veg in weeklyVegMenu:
            print(veg['dish'])
    usineMenu.notifyUsers(users, debug)


if __name__ == '__main__':
    main()
```
