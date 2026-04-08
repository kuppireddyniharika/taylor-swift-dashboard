import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Taylor Swift Dashboard", layout="wide")

# Load data
df1 = pd.read_csv("taylor_swift_spotify.csv")
df2 = pd.read_csv("spotify_top_songs_audio_features.csv")

# Clean column names
df1.columns = df1.columns.str.strip().str.lower()
df2.columns = df2.columns.str.strip().str.lower()

# Merge datasets
common_cols = list(set(df1.columns).intersection(set(df2.columns)))

if common_cols:
    df = pd.merge(df1, df2, on=common_cols[0], how="inner")
else:
    df = df1.copy()

# Debug: show columns
st.write("Columns in dataset:", df.columns)

# Function to find column safely
def find_column(names):
    for col in names:
        if col in df.columns:
            return col
    return None

# Identify columns
track_col = find_column(['track_name', 'track', 'song'])
album_col = find_column(['album'])
streams_col = find_column(['streams'])
popularity_col = find_column(['popularity'])
energy_col = find_column(['energy'])

# Fill missing values safely
if streams_col:
    df[streams_col] = df[streams_col].fillna(0)

if popularity_col:
    df[popularity_col] = df[popularity_col].fillna(0)

if energy_col:
    df[energy_col] = df[energy_col].fillna(0)
else:
    st.warning("⚠️ Energy column not found")

# Title
st.title("🎤 Taylor Swift Dashboard")

# Filter
if album_col:
    selected_album = st.selectbox("Select Album", df[album_col].dropna().unique())
    filtered_df = df[df[album_col] == selected_album]
else:
    filtered_df = df

# KPIs
c1, c2, c3 = st.columns(3)

c1.metric("Total Songs", len(filtered_df))

if popularity_col:
    c2.metric("Avg Popularity", round(filtered_df[popularity_col].mean(), 1))
else:
    c2.metric("Avg Popularity", "N/A")

if streams_col:
    c3.metric("Total Streams", int(filtered_df[streams_col].sum()))
else:
    c3.metric("Total Streams", "N/A")

st.markdown("---")

# Top songs
if streams_col:
    top = filtered_df.sort_values(by=streams_col, ascending=False).head(10)
else:
    top = filtered_df.head(10)

# Bar chart
if streams_col and track_col:
    fig = px.bar(top, x=track_col, y=streams_col, color=streams_col)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Required columns for bar chart not found")

# Scatter plot
if energy_col and popularity_col and streams_col and track_col:
    fig2 = px.scatter(
        filtered_df,
        x=energy_col,
        y=popularity_col,
        size=streams_col,
        hover_name=track_col
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("⚠️ Required columns for scatter plot not found")

# Data table
st.dataframe(filtered_df)

   
