import os

import dotenv
import folium
import geopandas as gpd
import pandas as pd


def create_dataset() -> gpd.GeoDataFrame:
    billboard_postcodes = pd.read_csv(
        os.path.join("data", "billboard_locations.csv")
    ).drop_duplicates()
    postcode_lookup = pd.read_csv(
        os.path.join("data", "ONSPD_MAY_2025_UK.csv"), low_memory=False
    )[["pcds", "lat", "long"]].rename(columns={"pcds": "postcode"})

    locations = pd.merge(billboard_postcodes, postcode_lookup)
    locations = gpd.GeoDataFrame(
        locations,
        geometry=gpd.points_from_xy(locations["long"], locations["lat"]),
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
    m = folium.Map([51, 0], zoom_start=7, tiles=tile_url, attr=attr)
    folium.GeoJson(
        data,
        marker=folium.Marker(
            icon=folium.Icon(
                icon="rectangle-ad", prefix="fa", color="cadetblue", icon_color="white"
            )
        ),
    ).add_to(m)

    m.save("index.html")


if __name__ == "__main__":
    main()
