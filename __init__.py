import requests
import datetime
import tempfile
import os
from bs4 import BeautifulSoup


class usineMenu:
    def __init__(self):
        self.weekDaysEng = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        self.weekDaysGer = [
            "Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",
            "Sonntag",
        ]
        self.weeklyMenu = []
        self.weeklyVegMenu = []
        self.classicMenu = []
        self.menu = []
        self.todayNum = datetime.datetime.today().weekday()

    def __getFullMenu(self):
        url = 'http://www.usine.se/restaurang'
        headers = {
            'Origin': 'http://www.usine.se/restaurang',
        }
        s = requests.Session()
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        usine38Menu = soup.find_all('div', attrs={'id': 'lunch-bistro38Del'})
        return usine38Menu

    def __populateWeeklyVegMenu(self, Menu):
        for usine38Tag in Menu:
            menuClass = (
                'Bredd100 RutaVit RutaMarginalUppNer MarginalBortUppNer'
            )
            divMenu = usine38Tag.find_all(
                'div',
                attrs={
                    'class': menuClass
                },
                limit=1
            )
            for menuTag in divMenu:
                leftMenuClass = 'Bilder Bredd50 Ruta4'
                divLeftMenu = menuTag.find_all(
                    'div',
                    attrs={
                        'class': leftMenuClass
                    },
                    limit=1
                )
                for divLeftMenuTag in divLeftMenu:
                    menuClass = [
                        'Bredd100 RutaMarginalUpp',
                        'Bredd100 RutaMarginalUppNer'
                    ]
                    weeklyVegClass = [
                        'RutaMarginalSidor'
                    ]
                    divWeeklyVegEntry = divLeftMenuTag.find_all(
                        'div',
                        attrs={
                            'class': weeklyVegClass
                        }
                    )
                    for weeklyVegEntry in divWeeklyVegEntry:
                        if 'VECKANS VEGETARISKA' in weeklyVegEntry.text:
                            dishNameDiv = 'MenyRattRadUnderrubrik'
                            dishDescDiv = 'MenyRattRadVanster'
                            priceDiv = 'MenyRattRadHogerMarginal'
                            dishNameObjList = weeklyVegEntry.find_all(
                                'div',
                                attrs={
                                    'class': dishNameDiv
                                }
                            )
                            dishDescObjList = weeklyVegEntry.find_all(
                                'div',
                                attrs={
                                    'class': dishDescDiv
                                }
                            )
                            priceObjlist = weeklyVegEntry.find_all(
                                'div',
                                attrs={
                                    'class': priceDiv
                                }
                            )
                    weeklyVegList = []

                    for dishName, dishDesc, price in zip(
                        dishNameObjList,
                        dishDescObjList,
                        priceObjlist
                    ):
                        weeklyVegList.append(
                            {
                                'dish': "{name} - {desc}".format(
                                    name=dishName.text,
                                    desc=dishDesc.text
                                ),
                                'price': price.text.replace('\n', '')
                            }
                        )
        return weeklyVegList

    def __populateClassicMenu(self, Menu):
        for usine38Tag in Menu:
            menuClass = (
                'Bredd100 RutaVit RutaMarginalUppNer MarginalBortUppNer'
            )
            divMenu = usine38Tag.find_all(
                'div',
                attrs={
                    'class': menuClass
                },
                limit=1
            )
            for menuTag in divMenu:
                rightMenuClass = 'Bilder Bredd50 Ruta4 RamVansterBred'
                divRightMenu = menuTag.find_all(
                    'div',
                    attrs={
                        'class': rightMenuClass
                    },
                    limit=1
                )
                for rightMenuTag in divRightMenu:
                    menuClass = 'Bredd100 RutaMarginalUppNer'
                    classicMenu = rightMenuTag.find_all(
                        'div',
                        attrs={
                            'class': menuClass
                        }
                    )
                    entryClass = 'MenyRattRadHallare'
                    classicMenuEntries = classicMenu[0].find_all(
                        'div',
                        attrs={
                            'class': entryClass
                        }
                    )
                    classicMenuList = []
                    for entry in classicMenuEntries:
                        titelClass = 'MenyRattRadUnderrubrik'
                        dishClass = 'MenyRattRadVanster'
                        priceClass = 'MenyRattRadHoger'
                        title = entry.find_all(
                            'div',
                            attrs={
                                'class': titelClass
                            }
                        )
                        dish = entry.find_all(
                            'div',
                            attrs={
                                'class': dishClass
                            }
                        )
                        price = entry.find_all(
                            'div',
                            attrs={
                                'class': priceClass
                            }
                        )
                        title = title[0].text
                        dish = dish[0].text
                        price = price[0].text.replace('\n', '')
                        classicMenuList.append(
                            {
                                'title': title,
                                'dish': dish,
                                'price': price
                            }
                        )
        return classicMenuList

    def __populateWeeklyMenu(self, Menu):
        weeklyMenu = []
        for usine38Tag in Menu:
            menuClass = (
                'Bredd100 RutaVit RutaMarginalUppNer MarginalBortUppNer'
            )
            divMenu = usine38Tag.find_all(
                'div',
                attrs={
                    'class': menuClass
                },
                limit=1
            )
            for menuTag in divMenu:
                leftMenuClass = 'Bilder Bredd50 Ruta4'
                divLeftMenu = menuTag.find_all(
                    'div',
                    attrs={
                        'class': leftMenuClass
                    },
                    limit=1
                )
                for divLeftMenuTag in divLeftMenu:
                    menuClass = [
                        'Bredd100 RutaMarginalUpp',
                        'Bredd100 RutaMarginalUppNer'
                    ]
                    divMenuEntry = divLeftMenuTag.find_all(
                        'div',
                        attrs={
                            'class': menuClass
                        }
                    )
                    del divMenuEntry[0]
                    iter = 0
                    for menuEntry in divMenuEntry:
                        dayDiv = 'MenyRattRubrik RamNerMinst'
                        dishTitleDiv = 'MenyRattRadUnderrubrik'
                        dishDescDiv = 'MenyRattRadVanster'
                        dayObj = menuEntry.find_all(
                            'div',
                            attrs={
                                dayDiv
                            }
                        )
                        dishTitleObj = menuEntry.find_all(
                            'div',
                            attrs={
                                dishTitleDiv
                            }
                        )
                        dishDescObj = menuEntry.find_all(
                            'div',
                            attrs={
                                dishDescDiv
                            }
                        )
                        priceDiv = 'MenyRattRadHogerMarginal'
                        priceObj = menuEntry.find_all(
                            'div',
                            attrs={
                                'class': priceDiv
                            }
                        )
                        day = dayObj[0].contents[0]
                        dishTitle = ""
                        if dishTitleObj:
                            dishTitle = dishTitleObj[0].contents[0].strip()
                        dishDesc = dishDescObj[0].contents[0].strip()
                        dish = "{title} {desc}".format(
                            title=dishTitle,
                            desc=dishDesc
                        ).strip()
                        price = priceObj[0].text.replace('\n', '')
                        weeklyMenu.append(
                            [
                                day,
                                dish,
                                price
                            ]
                        )
                        if 'fredag' in day.lower() or iter == 4:
                            break
                        iter += 1
        return weeklyMenu

    def __cleanupWeeklyMenu(self, menu):
        weeklyMenu = []
        year = datetime.date.today().year
        for row in menu:
            day = (row[0].split()[1].split('/')[0])
            month = (row[0].split()[1].split('/')[1])
            dish = row[1]
            price = row[2]
            dateStr = '-'.join(
                [
                    str(year),
                    str(month),
                    str(day)]
            )
            dateObj = datetime.datetime.strptime(dateStr, "%Y-%m-%d").date()
            weeklyMenu.append(
                {
                    'date': dateObj,
                    'dish': dish,
                    'price': price
                }
            )
        return weeklyMenu

    def __todaysLunch(self, menu):
        today = datetime.date.today()
        todaysLunch = next(
            (
                days for days in menu
                if today == days['date']
            ),
            False
        )
        return todaysLunch

    def getMenus(self):
        self.menu = self.__getFullMenu()
        self.weeklyVegMenu = self.__populateWeeklyVegMenu(self.menu)
        self.classicMenu = self.__populateClassicMenu(self.menu)
        weeklyMenu = self.__populateWeeklyMenu(self.menu)
        self.weeklyMenu = self.__cleanupWeeklyMenu(weeklyMenu)
        return self.weeklyMenu, self.weeklyVegMenu, self.classicMenu

    def notifyUsers(self, users, debug):
        weeklyMenu = self.weeklyMenu
        schnitzelDay = False
        message = None
        for row in weeklyMenu:
            today = datetime.date.today()
            if row['date'] == today:
                message = (
                    row['dish']
                )
                if (
                    "schnitzel" in row['dish']
                ):
                    schnitzelDay = True
                    message = (
                        message +
                        "!!!"
                    )
                else:
                    message = (
                        message +
                        "."
                    )
                if "schnitzel" in str(menu):
                    for day in menu:
                        today = datetime.date.today()
                        if (
                            "schnitzel" in day['dish'] and
                            day['date'] > today
                        ):
                            message = (
                                message +
                                "\n\nBut on {day}: {dish}!!!!".format(
                                    day=weekDaysEng[day['date'].weekday()],
                                    dish=day['dish']
                                )
                            )
                for user in users:
                    to = "To: " + user['number'] + "\n\n"
                    if schnitzelDay:
                        greeting = (
                            "Hallo {name}, "
                            "heute ist der grosse Schnitzeltag: ".format(
                                name=user['friendlyname']
                            )
                        )
                        ending = (
                            "\n\nIch wünsche Ihnen einen schönen schnitzel" +
                            weekDaysGer[self.todayNum]
                        )
                    else:
                        greeting = (
                            "Hi {name}, today usine is serving: ".format(
                                name=user['friendlyname']
                            )
                        )
                        ending = (
                            "\n\nHave a great {day}!".format(
                                day=self.weekDaysEng[self.todayNum]
                            )
                        )
                    if debug:
                        print(to, greeting, message, ending, sep='')
                    else:
                        fd, path = tempfile.mkstemp(
                            dir="/var/spool/sms/outgoing")
                        os.chmod(path, 0o644)
                        with open(path, 'w') as file:
                            file.write(to)
                            file.write(greeting)
                            file.write(message)
                            file.write(ending)
                        os.close(fd)
        if message is None:
            for user in users:
                to = "To: " + user['number'] + "\n\n"
                message = (
                    "Hi {user}, usine aren't serving anything today, " +
                    "or they're garbage and haven't updated their menu yet"
                )
                message = message.format(
                    user=user['friendlyname']
                )
                ending = (
                    "\n\nHave a great {day}!".format(
                        day=self.weekDaysEng[self.todayNum]
                    )
                )
                if debug:
                    print(to, message, ending, sep='')
                else:
                    fd, path = tempfile.mkstemp(dir="/var/spool/sms/outgoing")
                    os.chmod(path, 0o644)
                    with open(path, 'w') as file:
                        file.write(to)
                        file.write(message)
                        file.write(ending)
                    os.close(fd)
