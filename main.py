import dotenv
import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import TagFilterButton


def create_dataset() -> gpd.GeoDataFrame:
    locations = pd.read_csv("data/billboard_locations.csv")[
        ["Name", "Estimated address", "Latitude", "Longitude", "City", "Environment"]
    ]
    locations["Type"] = (
        locations["Environment"]
        .map(
            {
                "transit.subway": "Tube/Underground Stations",
                "transit.train_stations": "Train Stations",
                "outdoor.bus_shelters": "Bus Stops",
            }
        )
        .fillna("Other")
    )
    locations = gpd.GeoDataFrame(
        locations,
        geometry=gpd.points_from_xy(locations["Longitude"], locations["Latitude"]),
        crs=4326,
    )

    return locations


def main():
    config = dotenv.dotenv_values(".env")
    data = create_dataset()
    tile_url = f"https://tile.jawg.io/jawg-lagoon/{{z}}/{{x}}/{{y}}{{r}}.png?access-token={config['JAWG_API_KEY']}&lang=en"
    attr = (
        '<a href="https://jawg.io?utm_medium=map&utm_source=attribution" title="Tiles Courtesy of Jawg Maps" target="_blank" class="jawg-attrib" >'
        "&copy; <b>Jawg</b>Maps</a>"
        " | "
        '<a href="https://www.openstreetmap.org/copyright" title="OpenStreetMap is open data licensed under ODbL" target="_blank" class="osm-attrib">'
        "&copy; OpenStreetMap</a>"
    )
    m = folium.Map([51, 0], zoom_start=7, tiles=tile_url, attr=attr, prefer_canvas=True)
    for tag, group in data.groupby("Type"):
        folium.GeoJson(
            group,
            marker=folium.Circle(
                radius=16, fill_color="blue", fill_opacity=0.4, color="black", weight=1
            ),
            tags=[tag],
        ).add_to(m)

    TagFilterButton(list(data["Type"].unique())).add_to(m)
    m.save("index.html")


if __name__ == "__main__":
    main()
