from MenuItem import MenuItem
from datetime import date
import requests
from bs4 import BeautifulSoup

lenoir_url = "https://dining.unc.edu/locations/top-of-lenoir/"
chase_url = "https://dining.unc.edu/locations/chase/"
api_url = "https://dining.unc.edu/wp-content/themes/nmc_dining/ajax-content/recipe.php"    

def get_menu(location: str, date: date = date.today()):
    if location == 'chase':
        url = chase_url
    elif location == 'lenoir':
        url = lenoir_url
    else:
        raise Exception('Location passed to get Menu is not \'Chase\' or \'Lenoir\'')
    
    params = {'date': date.isoformat()}
    
    page = requests.get(url, params)
    soup = BeautifulSoup(page.content, "html.parser")

    menu_object = {}
    menu_container = soup.find(id="single-location-wrap")
    menu_stations = menu_container.find_all("div", class_="menu-station")
    for menu_station in menu_stations:
        menu_station_items = []
        menu_items_lis = menu_station.find_all("li", class_="menu-item-li")
        for menu_item_li in menu_items_lis:
            menu_item_li_a = menu_item_li.find("a", class_="show-nutrition")
            menu_item_name = menu_item_li_a.text.strip()
            menu_item_recipe_id = menu_item_li_a.attrs.get('data-recipe')

            menu_station_items.append((menu_item_name, int(menu_item_recipe_id)))
        
        menu_object[menu_station.find('h4').text.strip()] = menu_station_items
    return menu_object

def get_nutrition_facts_for_all_menu_items(menu_object: dict):
    for menu_station_items in menu_object.values():
        for menu_item in menu_station_items:
            get_nutrition_facts_for_menu_item(menu_item[1])

def get_nutrition_facts_for_menu_item(recipe_id: int) -> MenuItem:
    params = {'recipe': recipe_id}
    recipe_html = requests.get(api_url, params).json().get('html')
    recipe_soup = BeautifulSoup(recipe_html, "html.parser")
    menu_item_name = recipe_soup.find('h2').text
    nutrition_facts_table = recipe_soup.find('table', class_='nutrition-facts-table')

    nutrition_facts_list = []
    nutrition_facts_table_rows = nutrition_facts_table.find_all('tr')
    for nutrition_facts_table_row in nutrition_facts_table_rows:
        if nutrition_facts_table_row.find('td', class_="nutrition-amount"):
            tokens = nutrition_facts_table_row.find('th').text.split()
            tokens.extend(nutrition_facts_table_row.find('td', class_="nutrition-amount").text.split())
            nutrition_facts_list.append(tokens)
        else:
            tokens = nutrition_facts_table_row.find('th').text.split()
            nutrition_facts_list.append(tokens)

    menu_item = {
        'name': menu_item_name,
        'recipe_id': recipe_id,
        'amount_per_serving': nutrition_facts_list[0][3] + ' ' + nutrition_facts_list[0][4],
        'calories': nutrition_facts_list[1][1],
        'calories_from_fat': nutrition_facts_list[2][3],
        'total_fat': nutrition_facts_list[3][2] + ' ' + nutrition_facts_list[3][3],
        'saturated_fat': nutrition_facts_list[4][2] + ' ' + nutrition_facts_list[4][3],
        'trans_fat': nutrition_facts_list[5][2] + ' ' + nutrition_facts_list[5][3],
        'cholesterol': nutrition_facts_list[6][1] + ' ' + nutrition_facts_list[6][2],
        'sodium': nutrition_facts_list[7][1] + ' ' + nutrition_facts_list[7][2],
        'total_carbohydrate': nutrition_facts_list[8][2] + ' ' + nutrition_facts_list[8][3],
        'dietary_fiber': nutrition_facts_list[9][2] + ' ' + nutrition_facts_list[9][3],
        'sugars': nutrition_facts_list[10][1] + ' ' + nutrition_facts_list[10][2],
        'protein': nutrition_facts_list[11][1] + ' ' + nutrition_facts_list[11][2],
        'calcium':  nutrition_facts_list[12][3],
        'iron':  nutrition_facts_list[13][3],
        'potassium': nutrition_facts_list[14][1] + ' ' + nutrition_facts_list[14][2],
        'vitamin_d': nutrition_facts_list[15][4]
    }

    print(menu_item)

# menu_soup = get_menu_soup_for_today('chase')
# menu_object = get_menu_object_from_menu_soup(menu_soup)
# get_nutrition_facts_for_menu_item(13807)

# with open('data.json', 'w') as outfile:
#     json.dump(menu_object, outfile, indent=4)
# menu_string = json.dumps(menu_object, indent=4)
# print(menu_string)
