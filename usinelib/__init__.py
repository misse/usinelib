""" Usine.se web parser module """
import datetime
import os
import tempfile
import requests
from bs4 import BeautifulSoup


class UsineMenu:
    """ Usine.se menu web parser class """
    def __init__(self):
        self.week_days_eng = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        self.week_days_ger = [
            "Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",
            "Sonntag",
        ]
        self.weekly_menu = []
        self.weekly_veg_menu = []
        self.classic_menu = []
        self.menu = []
        self.today_num = datetime.datetime.today().weekday()

    def __get_full_menu(self):
        url = 'http://www.usine.se/restaurang'
        headers = {
            '_origin': 'http://www.usine.se/restaurang',
        }
        session = requests.Session()
        request = session.get(url, headers=headers)
        soup = BeautifulSoup(request.content, 'html.parser')
        usine38_menu = soup.find_all('div', attrs={'id': 'lunch-bistro38_del'})
        return usine38_menu

    def __populate_weekly_veg_menu(self, _menu):
        for usine38_tag in _menu:
            menu_class = (
                '_bredd100 _ruta_vit _ruta_marginal_upp_ner _marginal_bort_upp_ner'
            )
            div_menu = usine38_tag.find_all(
                'div',
                attrs={
                    'class': menu_class
                },
                limit=1
            )
            for menu_tag in div_menu:
                left_menu_class = '_bilder _bredd50 _ruta4'
                div_left_menu = menu_tag.find_all(
                    'div',
                    attrs={
                        'class': left_menu_class
                    },
                    limit=1
                )
                for div_left_menu_tag in div_left_menu:
                    menu_class = [
                        '_bredd100 _ruta_marginal_upp',
                        '_bredd100 _ruta_marginal_upp_ner'
                    ]
                    weekly_veg_class = [
                        '_ruta_marginal_sidor'
                    ]
                    div_weekly_veg_entry = div_left_menu_tag.find_all(
                        'div',
                        attrs={
                            'class': weekly_veg_class
                        }
                    )
                    for weekly_veg_entry in div_weekly_veg_entry:
                        if '_v_e_c_k_a_n_s _v_e_g_e_t_a_r_i_s_k_a' in weekly_veg_entry.text:
                            dish_name_div = '_meny_ratt_rad_underrubrik'
                            dish_desc_div = '_meny_ratt_rad_vanster'
                            price_div = '_meny_ratt_rad_hoger_marginal'
                            dish_name_obj_list = weekly_veg_entry.find_all(
                                'div',
                                attrs={
                                    'class': dish_name_div
                                }
                            )
                            dish_desc_obj_list = weekly_veg_entry.find_all(
                                'div',
                                attrs={
                                    'class': dish_desc_div
                                }
                            )
                            price_objlist = weekly_veg_entry.find_all(
                                'div',
                                attrs={
                                    'class': price_div
                                }
                            )
                    weekly_veg_list = []

                    for dish_name, dish_desc, price in zip(
                            dish_name_obj_list,
                            dish_desc_obj_list,
                            price_objlist
                    ):
                        weekly_veg_list.append(
                            {
                                'dish': "{name} - {desc}".format(
                                    name=dish_name.text,
                                    desc=dish_desc.text
                                ),
                                'price': price.text.replace('\n', '')
                            }
                        )
        return weekly_veg_list

    def __populate_classic_menu(self, _menu):
        for usine38_tag in _menu:
            menu_class = (
                '_bredd100 _ruta_vit _ruta_marginal_upp_ner _marginal_bort_upp_ner'
            )
            div_menu = usine38_tag.find_all(
                'div',
                attrs={
                    'class': menu_class
                },
                limit=1
            )
            for menu_tag in div_menu:
                right_menu_class = '_bilder _bredd50 _ruta4 _ram_vanster_bred'
                div_right_menu = menu_tag.find_all(
                    'div',
                    attrs={
                        'class': right_menu_class
                    },
                    limit=1
                )
                for right_menu_tag in div_right_menu:
                    menu_class = '_bredd100 _ruta_marginal_upp_ner'
                    classic_menu = right_menu_tag.find_all(
                        'div',
                        attrs={
                            'class': menu_class
                        }
                    )
                    entry_class = '_meny_ratt_rad_hallare'
                    classic_menu_entries = classic_menu[0].find_all(
                        'div',
                        attrs={
                            'class': entry_class
                        }
                    )
                    classic_menu_list = []
                    for entry in classic_menu_entries:
                        titel_class = '_meny_ratt_rad_underrubrik'
                        dish_class = '_meny_ratt_rad_vanster'
                        price_class = '_meny_ratt_rad_hoger'
                        title = entry.find_all(
                            'div',
                            attrs={
                                'class': titel_class
                            }
                        )
                        dish = entry.find_all(
                            'div',
                            attrs={
                                'class': dish_class
                            }
                        )
                        price = entry.find_all(
                            'div',
                            attrs={
                                'class': price_class
                            }
                        )
                        title = title[0].text
                        dish = dish[0].text
                        price = price[0].text.replace('\n', '')
                        classic_menu_list.append(
                            {
                                'title': title,
                                'dish': dish,
                                'price': price
                            }
                        )
        return classic_menu_list

    def __populate_weekly_menu(self, _menu):
        weekly_menu = []
        for usine38_tag in _menu:
            menu_class = (
                '_bredd100 _ruta_vit _ruta_marginal_upp_ner _marginal_bort_upp_ner'
            )
            div_menu = usine38_tag.find_all(
                'div',
                attrs={
                    'class': menu_class
                },
                limit=1
            )
            for menu_tag in div_menu:
                left_menu_class = '_bilder _bredd50 _ruta4'
                div_left_menu = menu_tag.find_all(
                    'div',
                    attrs={
                        'class': left_menu_class
                    },
                    limit=1
                )
                for div_left_menu_tag in div_left_menu:
                    menu_class = [
                        '_bredd100 _ruta_marginal_upp',
                        '_bredd100 _ruta_marginal_upp_ner'
                    ]
                    div_menu_entry = div_left_menu_tag.find_all(
                        'div',
                        attrs={
                            'class': menu_class
                        }
                    )
                    del div_menu_entry[0]
                    index = 0
                    for menu_entry in div_menu_entry:
                        day_div = '_meny_ratt_rubrik _ram_ner_minst'
                        dish_title_div = '_meny_ratt_rad_underrubrik'
                        dish_desc_div = '_meny_ratt_rad_vanster'
                        day_obj = menu_entry.find_all(
                            'div',
                            attrs={
                                day_div
                            }
                        )
                        dish_title_obj = menu_entry.find_all(
                            'div',
                            attrs={
                                dish_title_div
                            }
                        )
                        dish_desc_obj = menu_entry.find_all(
                            'div',
                            attrs={
                                dish_desc_div
                            }
                        )
                        price_div = '_meny_ratt_rad_hoger_marginal'
                        price_obj = menu_entry.find_all(
                            'div',
                            attrs={
                                'class': price_div
                            }
                        )
                        day = day_obj[0].contents[0]
                        dish_title = ""
                        if dish_title_obj:
                            dish_title = dish_title_obj[0].contents[0].strip()
                        dish_desc = dish_desc_obj[0].contents[0].strip()
                        dish = "{title} {desc}".format(
                            title=dish_title,
                            desc=dish_desc
                        ).strip()
                        price = price_obj[0].text.replace('\n', '')
                        weekly_menu.append(
                            [
                                day,
                                dish,
                                price
                            ]
                        )
                        if 'fredag' in day.lower() or index == 4:
                            break
                        index += 1
        return weekly_menu

    def __cleanup_weekly_menu(self, menu):
        weekly_menu = []
        year = datetime.date.today().year
        for row in menu:
            day = (row[0].split()[1].split('/')[0])
            month = (row[0].split()[1].split('/')[1])
            dish = row[1]
            price = row[2]
            date_str = '-'.join(
                [
                    str(year),
                    str(month),
                    str(day)]
            )
            date_obj = datetime.datetime.strptime(date_str, "%_y-%m-%d").date()
            weekly_menu.append(
                {
                    'date': date_obj,
                    'dish': dish,
                    'price': price
                }
            )
        return weekly_menu

    def __todays_lunch(self, menu):
        today = datetime.date.today()
        todays_lunch = next(
            (
                days for days in menu
                if today == days['date']
            ),
            False
        )
        return todays_lunch

    def get_menus(self):
        """ fetches html and parses/cleans it for menu information """
        self.menu = self.__get_full_menu()
        self.weekly_veg_menu = self.__populate_weekly_veg_menu(self.menu)
        self.classic_menu = self.__populate_classic_menu(self.menu)
        weekly_menu = self.__populate_weekly_menu(self.menu)
        self.weekly_menu = self.__cleanup_weekly_menu(weekly_menu)
        return self.weekly_menu, self.weekly_veg_menu, self.classic_menu

    def notify_users(self, users, debug):
        """ generates message notification for each user about todays dish """
        weekly_menu = self.weekly_menu
        schnitzel_day = False
        message = None
        for row in weekly_menu:
            today = datetime.date.today()
            if row['date'] == today:
                message = (
                    row['dish']
                )
                if (
                        "schnitzel" in row['dish']
                ):
                    schnitzel_day = True
                    message = (
                        message +
                        "!!!"
                    )
                else:
                    message = (
                        message +
                        "."
                    )
                if "schnitzel" in str(weekly_menu):
                    for day in weekly_menu:
                        today = datetime.date.today()
                        if (
                                "schnitzel" in day['dish'] and
                                day['date'] > today
                        ):
                            message = (
                                message +
                                "\n\n_but on {day}: {dish}!!!!".format(
                                    day=self.week_days_eng[day['date'].weekday()],
                                    dish=day['dish']
                                )
                            )
                for user in users:
                    recipient = "To: " + user['number'] + "\n\n"
                    if schnitzel_day:
                        greeting = (
                            "_hallo {name}, "
                            "heute ist der grosse _schnitzeltag: ".format(
                                name=user['friendlyname']
                            )
                        )
                        ending = (
                            "\n\n_ich wünsche _ihnen einen schönen schnitzel" +
                            self.week_days_ger[self.today_num]
                        )
                    else:
                        greeting = (
                            "_hi {name}, today usine is serving: ".format(
                                name=user['friendlyname']
                            )
                        )
                        ending = (
                            "\n\n_have a great {day}!".format(
                                day=self.week_days_eng[self.today_num]
                            )
                        )
                    if debug:
                        print(recipient, greeting, message, ending, sep='')
                    else:
                        file_descriptor, path = tempfile.mkstemp(
                            dir="/var/spool/sms/outgoing")
                        os.chmod(path, 0o644)
                        with open(path, 'w') as file:
                            file.write(recipient)
                            file.write(greeting)
                            file.write(message)
                            file.write(ending)
                        os.close(file_descriptor)
        if message is None:
            for user in users:
                recipient = "To: " + user['number'] + "\n\n"
                message = (
                    "Hi {user}, usine aren't serving anything today, " +
                    "or they're garbage and haven't updated their menu yet"
                )
                message = message.format(
                    user=user['friendlyname']
                )
                ending = (
                    "\n\n_have a great {day}!".format(
                        day=self.week_days_eng[self.today_num]
                    )
                )
                if debug:
                    print(recipient, message, ending, sep='')
                else:
                    file_descriptor, path = tempfile.mkstemp(dir="/var/spool/sms/outgoing")
                    os.chmod(path, 0o644)
                    with open(path, 'w') as file:
                        file.write(recipient)
                        file.write(message)
                        file.write(ending)
                    os.close(file_descriptor)
