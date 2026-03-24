# ========================
# IMPORT LIBRARIES
# ========================
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ========================
# PAGE CONFIGURATION
# ========================
st.set_page_config(
    page_title="Netflix Content Analysis", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Netflix Theme Colors
NETFLIX_RED = "#E50914"
NETFLIX_BLACK = "#221F1F"
NETFLIX_GREY = "#F5F5F1"

# ========================
# TITLE & DESCRIPTION
# ========================
st.markdown(f"<h1 style='text-align: center; color: {NETFLIX_RED};'>🎬 Netflix Content Analysis</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Interactive dashboard to explore trends in Netflix movies and TV shows.</p>", unsafe_allow_html=True)
st.divider()

# ========================
# LOAD DATA (WITH CACHE)
# ========================
@st.cache_data
def load_data():
    df = pd.read_csv("data/netflix_titles.csv")

    # Basic cleaning
    df["country"] = df["country"].fillna("Unknown")
    df["listed_in"] = df["listed_in"].fillna("Unknown")
    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), format="%B %d, %Y", errors="coerce")
    
    return df

df = load_data()

# ========================
# PREPROCESS DATA FOR FILTERS
# ========================
# Explode genres
df["genre_list"] = df["listed_in"].apply(lambda x: [g.strip() for g in x.split(",")])
all_genres = pd.Series([g for sublist in df["genre_list"] for g in sublist])
top_genres = all_genres.value_counts().head(20).index.tolist()

# Explode countries
all_countries = pd.Series([c.strip() for sublist in df["country"].dropna().str.split(",") for c in sublist])
unique_countries = sorted(all_countries[all_countries != "Unknown"].unique())

# ========================
# SESSION STATE FOR SEARCH
# ========================
# Initialize search query in session state if it doesn't exist
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

def clear_search():
    st.session_state.search_query = ""

# ========================
# SIDEBAR FILTERS
# ========================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.header("🔍 Analysis Filters")

# Search Input tied to session state
search_term = st.sidebar.text_input(
    "🔎 Search by Title", 
    key="search_query", 
    placeholder="Ex: Stranger Things"
)

# Clear Search Button
st.sidebar.button("❌ Clear Search", on_click=clear_search)

st.sidebar.divider()

type_filter = st.sidebar.multiselect(
    "📺 Content Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

country_filter = st.sidebar.multiselect(
    "🌍 Country",
    options=unique_countries
)

selected_genres = st.sidebar.multiselect(
    "🎭 Genre",
    options=top_genres
)

# ========================
# APPLY FILTERS
# ========================
filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[filtered_df["title"].str.contains(search_term, case=False, na=False)]

if type_filter:
    filtered_df = filtered_df[filtered_df["type"].isin(type_filter)]

if country_filter:
    # Filter if any of the selected countries are in the country string
    pattern = '|'.join(country_filter)
    filtered_df = filtered_df[filtered_df["country"].str.contains(pattern, na=False)]

if selected_genres:
    filtered_df = filtered_df[
        filtered_df["genre_list"].apply(
            lambda genres: any(g in genres for g in selected_genres)
        )
    ]

# Stop execution if no data
if filtered_df.empty:
    st.error("No data found for the selected filters. Please adjust your search.")
    st.stop()

# ========================
# KPIs ROW
# ========================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_titles = len(filtered_df)
movies_count = len(filtered_df[filtered_df['type'] == 'Movie'])
tv_shows_count = len(filtered_df[filtered_df['type'] == 'TV Show'])
top_country = filtered_df['country'].value_counts().index[0] if not filtered_df.empty else "N/A"

kpi1.metric("📌 Total Titles", f"{total_titles:,}")
kpi2.metric("🎥 Movies", f"{movies_count:,}")
kpi3.metric("📺 TV Shows", f"{tv_shows_count:,}")
kpi4.metric("🌍 Top Country", top_country.split(',')[0])

st.divider()

# ========================
# CHARTS SECTION
# ========================
col1, col2 = st.columns(2)

with col1:
    # CHART 1 - TYPE DISTRIBUTION
    st.subheader("Distribution by Type")
    type_counts = filtered_df["type"].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    fig1 = px.pie(
        type_counts, 
        values='Count', 
        names='Type', 
        hole=0.4,
        color='Type',
        color_discrete_map={'Movie': NETFLIX_RED, 'TV Show': NETFLIX_BLACK}
    )
    fig1.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # CHART 2 - YEARLY TREND
    st.subheader("Releases by Year")
    year_counts = filtered_df["release_year"].value_counts().sort_index().reset_index()
    year_counts.columns = ['Year', 'Releases']
    # Filter out very old years for better visualization if needed
    year_counts = year_counts[year_counts['Year'] > 2000] 
    
    fig2 = px.area(
        year_counts, 
        x='Year', 
        y='Releases',
        color_discrete_sequence=[NETFLIX_RED]
    )
    fig2.update_layout(margin=dict(t=20, b=20, l=20, r=20), xaxis_title="Year", yaxis_title="Number of Titles")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    # CHART 3 - TOP GENRES
    st.subheader("Top 10 Genres")
    genre_exploded = filtered_df["genre_list"].explode()
    genre_counts = genre_exploded.value_counts().head(10).reset_index()
    genre_counts.columns = ['Genre', 'Count']
    
    fig3 = px.bar(
        genre_counts, 
        x='Count', 
        y='Genre', 
        orientation='h',
        color_discrete_sequence=[NETFLIX_BLACK]
    )
    fig3.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # CHART 4 - TOP COUNTRIES
    st.subheader("Top 10 Producing Countries")
    # Handle exploded countries just for this chart
    countries_exploded = filtered_df['country'].str.split(', ').explode()
    top_countries_chart = countries_exploded[countries_exploded != 'Unknown'].value_counts().head(10).reset_index()
    top_countries_chart.columns = ['Country', 'Count']
    
    fig4 = px.bar(
        top_countries_chart, 
        x='Count', 
        y='Country', 
        orientation='h',
        color_discrete_sequence=[NETFLIX_RED]
    )
    fig4.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig4, use_container_width=True)

# ========================
# WORDCLOUD
# ========================
st.subheader("☁️ Wordcloud: Titles")
text = " ".join(filtered_df["title"].dropna())

if text:
    wordcloud = WordCloud(
        width=1200, 
        height=400, 
        background_color="white", 
        colormap="Reds"
    ).generate(text)

    fig5, ax5 = plt.subplots(figsize=(15, 5))
    ax5.imshow(wordcloud, interpolation="bilinear")
    ax5.axis("off")
    st.pyplot(fig5)

# ========================
# RAW DATA EXPANDER
# ========================
with st.expander("📄 View Raw Data Table"):
    display_df = filtered_df.drop(columns=["show_id", "genre_list"], errors='ignore')
    st.dataframe(display_df, use_container_width=True)