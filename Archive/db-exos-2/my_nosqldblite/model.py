import pymongo
import hashlib
import logging

log = logging.getLogger(__file__)

def pwd(txt):
    return hashlib.sha256(txt.encode('utf-8')).hexdigest()

def get_database():
    myclient = pymongo.MongoClient("mongodb://localhost:27017") # port by default
    mydb = myclient["mycivilisation"]
    return mydb

def get_user_data():
    return [
            {"name": "lionel", "lastname": "auroux", "email": "lionel.auroux@gmail.com", "login": "iopi", "pwd": pwd("s!a][i13`qjwq")},
            {"name": "joe", "lastname": "hackerman", "email": "hack@man.com", "login": "hckz", "pwd": pwd("skSmwsoi21[@")},
            {"name": "julie", "lastname": "glandouille", "email": "ju@gland.me", "login": "juju", "pwd": pwd("kooL:!#?")},
            {"name": "celia", "lastname": "looze", "email": "celia@cool.org", "login": "cel", "pwd": pwd("1234132")},
    ]

city_list = [
    "Washington",
    "Cairo",
    "Canberra",
    "Tenochtitlan",
    "Babylon",
    "Rio de Janeiro",
    "Constantinople",
    "Ottawa",
    "Xi'an",
    "Beijing",
    "Mikisiw-Wacîhk",
    "Amsterdam",
    "Râ-Kedet",
    "London",
    "Addis Ababa",
    "Paris",
    "Aduatuca",
    "Tbilisi",
    "Aachen",
    "Bogotá",
    "Athens",
    "Sparta",
    "Buda",
    "Qusqu",
    "Delhi",
    "Patna",
    "Majapahit",
    "Kyoto",
    "Angkor Thom",
    "Mbanza Kongo",
    "Gyeongju",
    "Pella",
    "Niani",
    "Te Hokianga-nui-a-kupe",
    "Ngulu Mapu",
    "Wak Kab'nal",
    "Qaraqorum",
    "Xanadu",
    "Nidaros",
    "Meroë",
    "Istanbul",
    "Pasargadae",
    "Tyre",
    "Kraków",
    "Lisbon",
    "Rome",
    "St. Petersburg",
    "Stirling",
    "Pokrovka",
    "Madrid",
    "Uruk",
    "Stockholm",
    "Thăng Long",
    "Ulundi"
]

def set_all_initial_city(mydb, rd, citydocname="mycity"):
    global city_list
    mycity = mydb[citydocname]
    log.error(f"INIT CITY")
    for login in mydb["users"].find({}, {'login': 1}):
        log.error(f"ID {login}")
        city_id = rd.randint(0, len(city_list))
        px, py = rd.randint(0, 100), rd.randint(0, 100)
        first_city = {
            "name": city_list[city_id], 
            "pos_x": px, 
            "pos_y": py, 
            "owner": login['_id'],
            "population_current": 5,
            "population_growth_by_turn": 1,
            "level": 1
        }
        log.error(f"ADD CITY {login} : {first_city}")
        mycity.insert_one(first_city)

### Game related stuff

building_list = [
    { "name": "Farm", "hammer_total": 20 },
    { "name": "Lumber-mill", "hammer_total": 30 },
    { "name": "Wonder", "hammer_total": 500 },
    { "name": "Blacksmith", "hammer_total": 80 },
]

food_req_by_city_level = [
    { "level": 1, "food_req": 30 },
    { "level": 2, "food_req": 250 },
    { "level": 3, "food_req": 1000 },
]

