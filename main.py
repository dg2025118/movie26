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
# 8. 개봉월별 총 관객 수 합계 & 최고 관객 영화
# ---------------------------
st.header("8. 개봉월별 총 관객 수 합계와 최고 관객 영화")

st.info("""
**안내:** 이 데이터는 지난 1년간 박스오피스 10위권에 든 영화 216편의 자료입니다.
'지난 10년'에 대한 데이터는 없기 때문에, 대신 **가지고 있는 1년치 데이터 안에서
개봉월별 관객 수 합계**를 분석했습니다. 실제로 10년치 자료를 분석하려면
여러 해의 박스오피스 데이터가 추가로 필요합니다.
""")

df_month = df.dropna(subset=["openDt"]).copy()
df_month["open_month"] = df_month["openDt"].dt.month

monthly_audi = df_month.groupby("open_month")["total_audi"].sum().reset_index()
monthly_audi.columns = ["month", "total_audi_sum"]

fig8 = px.bar(
    monthly_audi,
    x="month",
    y="total_audi_sum",
    labels={"month": "개봉 월", "total_audi_sum": "총 관객 수 합계"},
    title="개봉 월별 총 관객 수 합계"
)
fig8.update_xaxes(dtick=1)
fig8.update_traces(hovertemplate="개봉월: %{x}월<br>총 관객 수 합계: %{y:,}명<extra></extra>")

st.plotly_chart(fig8, use_container_width=True)

# 관객이 가장 많았던 달과, 그 달에 가장 많이 본 영화 찾기
best_month_row = monthly_audi.loc[monthly_audi["total_audi_sum"].idxmax()]
best_month = int(best_month_row["month"])

df_best_month = df_month[df_month["open_month"] == best_month]
top_movie_in_best_month = df_best_month.loc[df_best_month["total_audi"].idxmax()]

st.markdown(f"""
**자동 분석 결과**
- 총 관객 수 합계가 가장 많았던 개봉 월: **{best_month}월** (합계 {int(best_month_row['total_audi_sum']):,}명)
- 그 달에 개봉한 영화 중 가장 많이 본 영화: **{top_movie_in_best_month['movieNm']}**
  (총 관객 {int(top_movie_in_best_month['total_audi']):,}명)
""")

st.markdown("**이 그래프로 알 수 있는 것:** ")
st.text_area("문장을 직접 적어보세요.", key="insight8", placeholder="예: 어떤 달에 영화 관객이 몰리는지, 그 시기에 인기 있었던 영화가 무엇인지 알 수 있다.")

st.divider()

st.info("각 그래프 아래 빈칸에 스스로 관찰한 내용을 문장으로 정리해 보세요!")
