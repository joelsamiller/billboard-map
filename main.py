import os

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
    data = create_dataset()

    m = folium.Map([51, 0], zoom_start=4)
    folium.GeoJson(data).add_to(m)

    m.save("index.html")


if __name__ == "__main__":
    main()
