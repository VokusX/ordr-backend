def sanitize_items_data(data):
    return {
        "name": data.name,
        "price": data.price,
        "categoryUUID": data.categoryUuid,
        "description": data.description,
        "uuid": data.uuid,
        # "pictures":
    }