import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 2", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.markdown("""
이 앱은 최근 1년간 박스오피스 10위권에 든 영화 216편의 데이터를 활용해
**분포**와 **관계**를 살펴보는 다양한 그래프를 보여줍니다.
""")

# ---------------------------
# 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 열에 세로막대(|)로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    # 개봉일(여덟 자리 숫자)을 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(df["openDt"], format="%Y%m%d", errors="coerce")

    return df

df = load_data()

with st.expander("원본 데이터 미리보기"):
    st.dataframe(df)

st.divider()

# ---------------------------
# 1. 장르별 영화 편수 - 도넛 그래프
# ---------------------------
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig1 = go.Figure(
    data=[
        go.Pie(
            labels=genre_counts["genre"],
            values=genre_counts["count"],
            hole=0.5,
            hovertemplate="장르: %{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
        )
    ]
)
fig1.update_layout(title="장르별 영화 편수 비율")

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight1", placeholder="예: 어떤 장르의 영화가 가장 많이 개봉했는지 알 수 있다.")

st.divider()

# ---------------------------
# 2. 총 관객 수 분포 - 히스토그램
# ---------------------------
st.header("2. 총 관객 수 분포")

fig2 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    labels={"total_audi": "총 관객 수"},
    title="영화별 총 관객 수 분포"
)
fig2.update_traces(hovertemplate="관객 수 구간: %{x}<br>영화 수: %{y}편<extra></extra>")

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight2", placeholder="예: 대부분의 영화는 총 관객 수가 어느 구간에 몰려 있는지 알 수 있다.")

st.divider()

# ---------------------------
# 3. 개봉일 스크린 수와 총 관객 수의 관계 - 산점도
# ---------------------------
st.header("3. 개봉일 스크린 수와 총 관객 수의 관계")

fig3 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    labels={"first_scrn": "개봉일 스크린수", "total_audi": "총 관객 수"},
    title="개봉일 스크린수 vs 총 관객 수 (장르별 색상 구분)"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight3", placeholder="예: 개봉일 스크린수가 많을수록 총 관객 수가 많은 경향이 있는지 알 수 있다.")

st.divider()

# ---------------------------
# 4. 10위권 유지 일수 분포 - 박스플롯 (장르별)
# ---------------------------
st.header("4. 장르별 10위권 유지 일수 분포")

fig4 = px.box(
    df,
    x="genre",
    y="days_in_top10",
    labels={"genre": "장르", "days_in_top10": "10위권 유지 일수"},
    title="장르별 10위권 유지 일수 분포"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight4", placeholder="예: 어떤 장르가 10위권에 더 오래 머무는 경향이 있는지 알 수 있다.")

st.divider()

# ---------------------------
# 5. 개봉 첫 주 관객 수와 총 관객 수의 관계 - 산점도 + 추세선
# ---------------------------
st.header("5. 개봉 첫 주 관객 수와 총 관객 수의 관계")

fig5 = px.scatter(
    df,
    x="first_week_audi",
    y="total_audi",
    trendline="ols",
    hover_name="movieNm",
    labels={"first_week_audi": "개봉 첫 주 관객 수", "total_audi": "총 관객 수"},
    title="개봉 첫 주 관객 수 vs 총 관객 수"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight5", placeholder="예: 개봉 첫 주 관객 수로 총 관객 수를 어느 정도 예측할 수 있는지 알 수 있다.")

st.divider()

st.info("각 그래프 아래 빈칸에 스스로 관찰한 내용을 문장으로 정리해 보세요!")
