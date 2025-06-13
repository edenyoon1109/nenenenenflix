import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="넷플릭스 콘텐츠 분석", layout="wide")

# 제목
st.title("🎬 넷플릭스 콘텐츠 장르 분석 대시보드")
st.markdown("Kaggle에서 수집한 데이터를 바탕으로 넷플릭스 콘텐츠의 장르, 국가, 연도별 트렌드를 시각화합니다.")

# 데이터 로딩 함수 (캐시로 빠르게)
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df = df.dropna(subset=["listed_in", "release_year"])
    df["listed_in"] = df["listed_in"].str.split(", ")
    df = df.explode("listed_in")
    return df

df = load_data()

# 필터 (사이드바)
st.sidebar.header("필터")
types = df["type"].unique().tolist()
selected_types = st.sidebar.multiselect("콘텐츠 유형", types, default=types)

year_min = int(df["release_year"].min())
year_max = int(df["release_year"].max())
selected_years = st.sidebar.slider("제작 연도", year_min, year_max, (2010, 2021))

# 필터 적용
df_filtered = df[
    (df["type"].isin(selected_types)) &
    (df["release_year"].between(selected_years[0], selected_years[1]))
]

# 1. 장르별 콘텐츠 수
st.subheader("1️⃣ 장르별 콘텐츠 수 (Top 10)")
genre_count = df_filtered["listed_in"].value_counts().head(10)
fig1 = px.bar(
    x=genre_count.index,
    y=genre_count.values,
    labels={"x": "장르", "y": "콘텐츠 수"},
    title="장르별 콘텐츠 수",
    color=genre_count.values,
    color_continuous_scale="reds"
)
st.plotly_chart(fig1, use_container_width=True)

# 2. 국가별 콘텐츠 수
st.subheader("2️⃣ 국가별 콘텐츠 수 (Top 10)")
df_country = df[df["country"].notna()]
country_count = df_country[df_country["type"].isin(selected_types)]["country"].value_counts().head(10)
fig2 = px.bar(
    x=country_count.index,
    y=country_count.values,
    labels={"x": "국가", "y": "콘텐츠 수"},
    title="국가별 콘텐츠 수",
    color=country_count.values,
    color_continuous_scale="blues"
)
st.plotly_chart(fig2, use_container_width=True)

# 3. 연도별 콘텐츠 수
st.subheader("3️⃣ 연도별 콘텐츠 수")
yearly_count = df[df["type"].isin(selected_types)].groupby("release_year").size()
fig3 = px.line(
    x=yearly_count.index,
    y=yearly_count.values,
    labels={"x": "연도", "y": "콘텐츠 수"},
    title="연도별 콘텐츠 제작 트렌드"
)
st.plotly_chart(fig3, use_container_width=True)

# 4. 데이터 테이블
st.subheader("📄 필터링된 콘텐츠 데이터 (최대 50개 표시)")
st.dataframe(df_filtered[["title", "type", "listed_in", "country", "release_year"]].head(50))
