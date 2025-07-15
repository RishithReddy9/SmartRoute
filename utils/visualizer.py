import folium
from folium.plugins import BeautifyIcon
from utils.maps import get_road_path  # Your directions API function

def display_routes(routes, latlngs, locations):
    m = folium.Map(location=latlngs[0], zoom_start=12)
    colors = ["red", "blue", "green", "purple", "orange"]

    for vehicle_id, route in enumerate(routes):
        color = colors[vehicle_id % len(colors)]

        # ➤ Plot route lines using Directions API
        for i in range(len(route) - 1):
            start = latlngs[route[i]]
            end = latlngs[route[i + 1]]
            road_path = get_road_path(start, end)
            folium.PolyLine(road_path, color=color, weight=4.5, opacity=0.9).add_to(m)

        # ➤ Add numbered markers
        for order, idx in enumerate(route):
            lat, lon = latlngs[idx]
            label = f"{order}"
            popup_text = f"Stop {order}: {locations[idx]}"

            # Use different color for depot
            icon_color = "blue" if order == 0 else "green"
            icon = BeautifyIcon(
                icon_shape="marker",
                number=label,
                border_color=icon_color,
                text_color="white",
                background_color=icon_color,
            )
            folium.Marker(
                location=(lat, lon),
                popup=popup_text,
                icon=icon
            ).add_to(m)

    return m._repr_html_()
