import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    # 1년간 박스오피스 10위권에 든 영화 216편의 요약표를 불러옵니다
    df = pd.read_csv(DATA_URL)
    # 장르가 세로막대 기호(|)로 여러 개 적힌 영화는 첫 번째 장르만 씁니다
    df["장르"] = df["genre"].str.split("|").str[0]
    return df


df = load_data()

# ── 그래프 1. 장르별 영화 편수 도넛 ──
st.header("1. 장르별 영화 편수 (도넛)")
genre_count = df["장르"].value_counts().reset_index()
genre_count.columns = ["장르", "편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="편수",
    hole=0.45,  # 가운데 구멍을 뚫어 도넛 모양으로
)
# 조각에 마우스를 올리면 편수와 비율이 보이게 합니다
fig.update_traces(hovertemplate="%{label}<br>%{value}편 (%{percent})<extra></extra>")
st.plotly_chart(fig, width="stretch")

# '이 그래프로 알 수 있는 것' 한 문장을 적는 자리
st.text_input("이 그래프로 알 수 있는 것", key="note1")

st.divider()
# 앞으로 그래프를 계속 추가할 구역
st.header("2. (다음 그래프를 여기에 추가)")
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
# 2. 장르 안에 영화 - 트리맵 (크기: 총 관객)
# ---------------------------
st.header("2. 장르별 영화 총 관객 수 트리맵")

fig2_tree = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 안 영화별 총 관객 수 (칸 크기 = 총 관객 수)"
)
fig2_tree.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2_tree, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight2_tree", placeholder="예: 같은 장르 안에서도 영화별로 총 관객 수 차이가 큰지 작은지 알 수 있다.")

st.divider()

# ---------------------------
# 3. 총 관객 수 분포 - 히스토그램
# ---------------------------
st.header("3. 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    labels={"total_audi": "총 관객 수"},
    title="영화별 총 관객 수 분포"
)
fig3.update_traces(hovertemplate="관객 수 구간: %{x}<br>영화 수: %{y}편<extra></extra>")

st.plotly_chart(fig3, use_container_width=True)

# 가장 많이 몰려있는 구간과 최고 관객 영화를 자동 계산
hist_counts, bin_edges = pd.cut(df["total_audi"], bins=30, retbins=True)
most_common_bin = hist_counts.value_counts().idxmax()
top_movie_row = df.loc[df["total_audi"].idxmax()]

st.markdown(f"""
**자동 분석 결과**
- 가장 많은 영화가 몰려 있는 총 관객 수 구간: **{int(most_common_bin.left):,} ~ {int(most_common_bin.right):,}명**
- 총 관객 수가 가장 많은 영화: **{top_movie_row['movieNm']}** (총 관객 {int(top_movie_row['total_audi']):,}명)
""")

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight3", placeholder="예: 대부분의 영화는 총 관객 수가 어느 구간에 몰려 있는지 알 수 있다.")

st.divider()

# ---------------------------
# 4. 개봉일 스크린 수와 총 관객 수의 관계 - 산점도
# ---------------------------
st.header("4. 개봉일 스크린 수와 총 관객 수의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    labels={"first_scrn": "개봉일 스크린수", "total_audi": "총 관객 수"},
    title="개봉일 스크린수 vs 총 관객 수 (장르별 색상 구분)"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight4", placeholder="예: 개봉일 스크린수가 많을수록 총 관객 수가 많은 경향이 있는지 알 수 있다.")

st.divider()

# ---------------------------
# 5. 영화 10편 이상 장르만 - 박스플롯 (총 관객)
# ---------------------------
st.header("5. 영화 10편 이상인 장르별 총 관객 수 분포")

genre_count_series = df["genre"].value_counts()
major_genres = genre_count_series[genre_count_series >= 10].index
df_major = df[df["genre"].isin(major_genres)]

fig5 = px.box(
    df_major,
    x="genre",
    y="total_audi",
    points="outliers",
    hover_data=["movieNm"],
    labels={"genre": "장르", "total_audi": "총 관객 수"},
    title="영화 10편 이상인 장르의 총 관객 수 분포 (이상치에 영화명 표시)"
)
fig5.update_traces(
    hovertemplate="장르: %{x}<br>총 관객: %{y:,}<br>영화명: %{customdata[0]}<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight5", placeholder="예: 영화 편수가 많은 장르 중 어떤 장르가 총 관객 수 편차가 큰지 알 수 있다.")

st.divider()

# ---------------------------
# 6. 스크린수-관객 버블 그래프 (크기: 첫 주 관객)
# ---------------------------
st.header("6. 개봉일 스크린수 · 총 관객 수 · 첫 주 관객 수 버블 그래프")

fig6_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=50,
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객 수",
        "first_week_audi": "개봉 첫 주 관객 수"
    },
    title="개봉일 스크린수 vs 총 관객 수 (버블 크기 = 개봉 첫 주 관객 수)"
)

st.plotly_chart(fig6_bubble, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight6_bubble", placeholder="예: 첫 주 관객이 많은 영화가 전체 관객 수도 많은 경향이 있는지 알 수 있다.")

st.divider()

# ---------------------------
# 7. 국가 -> 장르 선버스트
# ---------------------------
st.header("7. 제작 국가별 장르 선버스트")

fig7_sun = px.sunburst(
    df,
    path=["nation", "genre"],
    title="제작 국가 안의 장르별 영화 편수 (칸 크기 = 영화 편수)"
)
fig7_sun.update_traces(
    hovertemplate="%{label}<br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig7_sun, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight7_sun", placeholder="예: 어떤 국가가 어떤 장르의 영화를 많이 만드는지 알 수 있다.")

st.divider()

st.info("각 그래프 아래 빈칸에 스스로 관찰한 내용을 문장으로 정리해 보세요!")
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
# 2. 장르 안에 영화 - 트리맵 (크기: 총 관객)
# ---------------------------
st.header("2. 장르별 영화 총 관객 수 트리맵")

fig2_tree = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 안 영화별 총 관객 수 (칸 크기 = 총 관객 수)"
)
fig2_tree.update_traces(
    hovertemplate="영화명: %{label}<br>총 관객: %{value:,}명<extra></extra>"
)

st.plotly_chart(fig2_tree, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight2_tree", placeholder="예: 같은 장르 안에서도 영화별로 총 관객 수 차이가 큰지 작은지 알 수 있다.")

st.divider()

# ---------------------------
# 3. 총 관객 수 분포 - 히스토그램
# ---------------------------
st.header("3. 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    labels={"total_audi": "총 관객 수"},
    title="영화별 총 관객 수 분포"
)
fig3.update_traces(hovertemplate="관객 수 구간: %{x}<br>영화 수: %{y}편<extra></extra>")

st.plotly_chart(fig3, use_container_width=True)

# 가장 많이 몰려있는 구간과 최고 관객 영화를 자동 계산
hist_counts, bin_edges = pd.cut(df["total_audi"], bins=30, retbins=True)
most_common_bin = hist_counts.value_counts().idxmax()
top_movie_row = df.loc[df["total_audi"].idxmax()]

st.markdown(f"""
**자동 분석 결과**
- 가장 많은 영화가 몰려 있는 총 관객 수 구간: **{int(most_common_bin.left):,} ~ {int(most_common_bin.right):,}명**
- 총 관객 수가 가장 많은 영화: **{top_movie_row['movieNm']}** (총 관객 {int(top_movie_row['total_audi']):,}명)
""")

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight3", placeholder="예: 대부분의 영화는 총 관객 수가 어느 구간에 몰려 있는지 알 수 있다.")

st.divider()

# ---------------------------
# 4. 개봉일 스크린 수와 총 관객 수의 관계 - 산점도
# ---------------------------
st.header("4. 개봉일 스크린 수와 총 관객 수의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    labels={"first_scrn": "개봉일 스크린수", "total_audi": "총 관객 수"},
    title="개봉일 스크린수 vs 총 관객 수 (장르별 색상 구분)"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight4", placeholder="예: 개봉일 스크린수가 많을수록 총 관객 수가 많은 경향이 있는지 알 수 있다.")

st.divider()

# ---------------------------
# 5. 영화 10편 이상 장르만 - 박스플롯 (총 관객)
# ---------------------------
st.header("5. 영화 10편 이상인 장르별 총 관객 수 분포")

genre_count_series = df["genre"].value_counts()
major_genres = genre_count_series[genre_count_series >= 10].index
df_major = df[df["genre"].isin(major_genres)]

fig5 = px.box(
    df_major,
    x="genre",
    y="total_audi",
    points="outliers",
    hover_data=["movieNm"],
    labels={"genre": "장르", "total_audi": "총 관객 수"},
    title="영화 10편 이상인 장르의 총 관객 수 분포 (이상치에 영화명 표시)"
)
fig5.update_traces(
    hovertemplate="장르: %{x}<br>총 관객: %{y:,}<br>영화명: %{customdata[0]}<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight5", placeholder="예: 영화 편수가 많은 장르 중 어떤 장르가 총 관객 수 편차가 큰지 알 수 있다.")

st.divider()

# ---------------------------
# 6. 스크린수-관객 버블 그래프 (크기: 첫 주 관객)
# ---------------------------
st.header("6. 개봉일 스크린수 · 총 관객 수 · 첫 주 관객 수 버블 그래프")

fig6_bubble = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=50,
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객 수",
        "first_week_audi": "개봉 첫 주 관객 수"
    },
    title="개봉일 스크린수 vs 총 관객 수 (버블 크기 = 개봉 첫 주 관객 수)"
)

st.plotly_chart(fig6_bubble, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight6_bubble", placeholder="예: 첫 주 관객이 많은 영화가 전체 관객 수도 많은 경향이 있는지 알 수 있다.")

st.divider()

# ---------------------------
# 7. 국가 -> 장르 선버스트
# ---------------------------
st.header("7. 제작 국가별 장르 선버스트")

fig7_sun = px.sunburst(
    df,
    path=["nation", "genre"],
    title="제작 국가 안의 장르별 영화 편수 (칸 크기 = 영화 편수)"
)
fig7_sun.update_traces(
    hovertemplate="%{label}<br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig7_sun, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight7_sun", placeholder="예: 어떤 국가가 어떤 장르의 영화를 많이 만드는지 알 수 있다.")

st.divider()

# ---------------------------
# 8. 나의 질문: 상위권에 많이 머물수록 실제 관객수가 많을까?
# ---------------------------
st.header("8. 상위권에 많이 머물수록 실제 관객수가 많을까?")

fig8 = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    hover_name="movieNm",
    labels={"days_in_top10": "10위권에 머문 날수", "total_audi": "총 관객 수"},
    title="상위권에 많이 머물수록 실제 관객수가 많을까?"
)

st.plotly_chart(fig8, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight8", placeholder="예: 10위권에 오래 머문 영화일수록 총 관객 수가 많은 경향이 있는지 알 수 있다.")

st.divider()

st.info("각 그래프 아래 빈칸에 스스로 관찰한 내용을 문장으로 정리해 보세요!")
