import streamlit as st
import pandas as pd
import plotly.express as px
from random import choice


class PlotDetails:
    def __init__(
        self,
        df: pd.DataFrame,
        df_title: str,
        df_type: str,
        selected_region: str,
        selected_age: str,
    ) -> None:
        self.df = df
        self.df_title = df_title
        self.df_type = df_type
        self.selected_region = selected_region
        self.selected_age = selected_age


def get_data():
    return [
        pd.read_csv("hiv_incidence.csv", header=0),
        pd.read_csv("aids_mortality_df.csv", header=0),
        pd.read_csv("children_living_hiv_df.csv", header=0),
    ]


def get_regions(df: pd.DataFrame):
    return set(hiv_incidence_df["regions"].values)


def select_region_rows(df: pd.DataFrame, region: str) -> pd.DataFrame:
    if region == "All":
        return df
    return df[df["regions"] == region]


def handle_bar_chart(plot_details: PlotDetails):
    df = select_region_rows(plot_details.df, plot_details.selected_region)
    fig = px.bar(
        df,
        x="regions" if plot_details.selected_region == "All" else "countries",
        y="_".join(plot_details.selected_age.split(" ")),
        title=plot_details.df_title,
    )
    st.plotly_chart(fig, use_container_width=True)


def handle_pie_chart(plot_details: PlotDetails):
    df = select_region_rows(plot_details.df, plot_details.selected_region)
    fig = px.pie(
        df,
        values="_".join(plot_details.selected_age.split(" ")),
        names="regions" if plot_details.selected_region == "All" else "countries",
        title=plot_details.df_title,
        width=700,
        height=700,
        color_discrete_sequence=px.colors.sequential.RdBu,
    )

    st.plotly_chart(fig, use_container_width=True)


def handle_click(plot_details: PlotDetails):
    if plot_details.df_type == "bar":
        handle_bar_chart(plot_details)

    if plot_details.df_type == "pie":
        handle_pie_chart(plot_details)


def get_quote():
    with open(r"quotes.en.fr.txt", mode="r") as file:
        quotes = file.readlines()
    return choice(quotes)


hiv_incidence_df, aids_mortality_df, children_living_hiv_df = get_data()

regions = list(get_regions(hiv_incidence_df))
regions.insert(0, "All")

type_to_dataset = {
    "hiv incidence per 1000 uninfected population": hiv_incidence_df,
    "AIDS-related mortality per 100,000 population": aids_mortality_df,
    "Number of children living with HIV": children_living_hiv_df,
}


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://w7.pngwing.com/pngs/962/58/png-transparent-logo-font-design-ribbon-logo-world-aids-day-thumbnail.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


st.title("🎀 Interactive data visualization about  HIV/AIDS: EPIDEMIOLOGY")
with st.sidebar:
    add_logo()
    donneSelected = st.selectbox("donnes", type_to_dataset.keys())
    ageSelected = st.selectbox("Ages", ["children 0-14", "girls 10–19", "boys 10–19"])
    regionSelected = st.selectbox("Pick a region", regions)
    st.header("_**Quotes of the day**_")
    st.markdown(get_quote())

plot_details = PlotDetails(
    type_to_dataset[donneSelected],
    donneSelected,
    "bar" if donneSelected == "Number of children living with HIV" else "pie",
    regionSelected,
    ageSelected,
)

handle_click(plot_details)
