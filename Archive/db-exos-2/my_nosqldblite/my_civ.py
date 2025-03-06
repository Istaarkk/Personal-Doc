def init_once(db, collection_name, datalist):
    collection = db[collection_name]
    for data in datalist:
        if not collection.find_one(data):
            collection.insert_one(data)

def get_city_by_owner(db, login):
    user = db["users"].find_one({"login": login})
    if not user:
        raise ValueError("Utilisateur introuvable")
    city = db["mycity"].find_one({"owner": user["_id"]})
    if not city:
        raise ValueError("Aucune ville trouvée")
    return city


def add_food_into_city(collection, city_id, apple_current, apple_by_turn, next_increase):
    document = collection.find_one({"_id": city_id})
    if document is None:
        raise ValueError("Ville introuvable")

    if 'foods' not in document:
        document['foods'] = {}

    collection.update_one(
        {"_id": city_id},
        {
            "$set": {
                "foods.apple_current": apple_current,
                "foods.apple_by_turn": apple_by_turn,
                "foods.next_increase": next_increase,
            }
        }
    )

def add_production_in_queue(db, cityid, prod_name, hammer_current, hammer_by_turn):
    collection = db["mycity"]
    city = collection.find_one({"_id": cityid})
    if city is None:
        raise ValueError("Ville introuvable")
    
    building = db["buildings"].find_one({"name": prod_name})
    if building is None:
        hammer_total = 0
    else :
        hammer_total = building.get("hammer_total",0)

    productions = city.get("productions",[])

    for i,production in enumerate(productions):
        if production['prod_name'] == prod_name:
            productions[i] = {
            'prod_name': prod_name,
            'hammer_current': hammer_current,
            'hammer_by_turn': hammer_by_turn,
            'hammer_total': hammer_total
        }
            break
    else:
        productions.append({
            'prod_name': prod_name,
            'hammer_current': hammer_current,
            'hammer_by_turn': hammer_by_turn,
            'hammer_total': hammer_total
        })
    
    collection.update_one({"_id": cityid}, {"$set": {"productions": productions}})