import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Taylor Swift Dashboard", layout="wide")

df1 = pd.read_csv("taylor_swift_spotify.csv")
df2 = pd.read_csv("spotify_top_songs_audio_features.csv")

df1.columns = df1.columns.str.strip().str.lower()
df2.columns = df2.columns.str.strip().str.lower()

common_cols = list(set(df1.columns).intersection(set(df2.columns)))

if common_cols:
    df = pd.merge(df1, df2, on=common_cols[0], how="inner")
else:
    df = df1.copy()
   

def find_column(names):
    for col in names:
        if col in df.columns:
            return col
    return None

track_col = find_column(['track_name', 'track', 'song'])
album_col = find_column(['album'])
streams_col = find_column(['streams'])
popularity_col = find_column(['popularity'])
energy_col = find_column(['energy'])

if streams_col:
    df[streams_col] = df[streams_col].fillna(0)

if popularity_col:
    df[popularity_col] = df[popularity_col].fillna(0)

if energy_col:
    df[energy_col] = df[energy_col].fillna(0)
else:
    st.warning("⚠️ Energy column not found")

st.title("🎤 Taylor Swift Dashboard")

if album_col:
    selected_album = st.selectbox("Select Album", df[album_col].dropna().unique())
    filtered_df = df[df[album_col] == selected_album]
else:
    filtered_df = df

c1, c2, c3 = st.columns(3)
c1.metric("Total Songs", len(filtered_df))
c2.metric("Avg Popularity", round(filtered_df[popularity_col].mean(), 1))
c3.metric("Total Streams", int(filtered_df[streams_col].sum()))

st.markdown("---")

top = filtered_df.sort_values(by=streams_col, ascending=False).head(10)

fig = px.bar(top, x=track_col, y=streams_col, color=streams_col)
st.plotly_chart(fig, use_container_width=True)

fig2 = px.scatter(
    filtered_df,
    x=energy_col,
    y=popularity_col,
    size=streams_col,
    hover_name=track_col
)

st.plotly_chart(fig2, use_container_width=True)

st.dataframe(filtered_df)
