from geocoder import get_coordinates
from business import find_businesses
from distance import lonlat_distance
from mapapi_PG import show_map


def get_color(business_hours):
    if business_hours is None:
        return (128, 128, 128)  # серый цвет для аптек без информации о времени работы

    hours = business_hours.lower()

    if "круглосуточно" in hours:
        return (0, 255, 0)  # зеленый цвет для круглосуточных аптек

    if "закрыто" in hours:
        return (128, 128, 128)  # серый цвет для закрытых аптек

    return (0, 0, 255)  # синий цвет для аптек с обычным режимом работы


def main():
    address = input("Введите адрес: ")
    coordinates = get_coordinates(address)

    if coordinates is None:
        print("Не удалось определить координаты адреса")
        return

    ll = f"{coordinates[0]},{coordinates[1]}"
    spn = "0.005,0.005"
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": "map"
    }

    businesses = find_businesses(ll, "аптека", 1)

    for business in businesses:
        business_ll = business["geometry"]["coordinates"]
        distance = lonlat_distance(coordinates, business_ll)
        business_hours = business["properties"]["CompanyMetaData"].get("Hours", None)
        color = get_color(business_hours)

        print(f"Название: {business['properties']['name']}")
        print(f"Адрес: {business['properties']['description']}")
        print(f"Расстояние: {distance:.2f} км")
        print(f"Режим работы: {business_hours}")
        print("=" * 50)

        point_params = f"pt={business_ll[0]},{business_ll[1]},pm2blm"
        map_params["pt"] = [point_params]

        show_map("&".join([f"{key}={value}" for key, value in map_params.items()]), add_params=point_params)


if __name__ == '__main__':
    main()