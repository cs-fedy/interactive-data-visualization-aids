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
    if region == "Touts":
        return df
    return df[df["regions"] == region]


def handle_bar_chart(plot_details: PlotDetails):
    df = select_region_rows(plot_details.df, plot_details.selected_region)
    fig = px.bar(
        df,
        x="regions" if plot_details.selected_region == "Touts" else "countries",
        y="_".join(plot_details.selected_age.split(" ")),
        title=plot_details.df_title,
    )
    st.plotly_chart(fig, use_container_width=True)


def handle_pie_chart(plot_details: PlotDetails):
    df = select_region_rows(plot_details.df, plot_details.selected_region)
    fig = px.pie(
        df,
        values="_".join(plot_details.selected_age.split(" ")),
        names="regions" if plot_details.selected_region == "Touts" else "countries",
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
    with open(r"quotes.txt", mode="r") as file:
        quotes = file.readlines()
    return choice(quotes)


hiv_incidence_df, aids_mortality_df, children_living_hiv_df = get_data()

regions = list(get_regions(hiv_incidence_df))
regions.insert(0, "Touts")

type_to_dataset = {
    "Incidence du VIH pour 1000 habitants non infectés": hiv_incidence_df,
    "Mortalité liée au SIDA pour 100 000 habitants": aids_mortality_df,
    "Nombre d'enfants vivant avec le VIH": children_living_hiv_df,
}


st.title("🎀 Visualisation interactive de données sur le VIH/SIDA : ÉPIDÉMIOLOGIE")
st.markdown(
    "[Source de données <<UNICEF_State_of_World_Children_2021>>](https://www.kaggle.com/datasets/nguyenngocphung/unicef-state-of-world-children-2021?resource=download)"
)
with st.sidebar:
    st.title("🎀 Protégez-vous du SIDA")

    donneSelected = st.selectbox("Types", type_to_dataset.keys())
    ageSelected = st.selectbox("Âge", ["children 0-14", "girls 10–19", "boys 10–19"])
    regionSelected = st.selectbox("Régions", regions)
    st.header("_**Citations du jour**_")
    st.caption(get_quote())

plot_details = PlotDetails(
    type_to_dataset[donneSelected],
    donneSelected,
    "bar" if donneSelected == "Nombre d'enfants vivant avec le VIH" else "pie",
    regionSelected,
    ageSelected,
)

handle_click(plot_details)
