import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

# 타이틀 및 소개
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    "1년간 박스오피스 10위권에 든 영화 중 해당 기간에 개봉한 216편의 데이터를"
    " 바탕으로 영화의 분포와 관계를 살펴봅니다."
)
st.markdown("---")


# 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
  url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
  df = pd.read_csv(url)

  # 장르 열이 존재할 경우 세로막대 기호(|)를 기준으로 첫 번째 장르만 추출
  if "genre" in df.columns:
    df["genre"] = df["genre"].apply(
        lambda x: str(x).split("|")[0] if pd.notnull(x) else "기타"
    )
  return df


# 데이터 로드
try:
  df = load_data()

  # ==========================================
  # 첫 번째 그래프: 장르별 영화 편수 도넛 그래프
  # ==========================================
  st.header("1. 장르별 영화 편수 분포")
  st.markdown(
      "박스오피스 10위권에 진입한 영화들의 대표 장르별 편수와 전체 대비 비율을"
      " 확인합니다."
  )

  # 장르별 편수 집계
  genre_counts = df["genre"].value_counts().reset_index()
  genre_counts.columns = ["genre", "count"]

  # Plotly 도넛 그래프 생성
  fig_genre = px.pie(
      genre_counts,
      names="genre",
      values="count",
      hole=0.4,  # 도넛 모양 생성
      title="대표 장르별 영화 편수 비율",
  )
  fig_genre.update_traces(
      textinfo="percent+label", hoverinfo="label+value+percent"
  )

  # 그래프 출력
  st.plotly_chart(fig_genre, use_container_width=True)

  # '이 그래프로 알 수 있는 것' 구역 (1)
  st.markdown("---")
  st.subheader("💡 이 그래프로 알 수 있는 것 (1)")
  st.info(
      "• 1년 동안 박스오피스 상위권에 가장 많이 이름을 올린 **주요 인기 장르**가"
      " 무엇인지 파악할 수 있습니다.\n• 전체 영화 중 특정 장르가 차지하는"
      " **상대적인 비중(%)**을 한눈에 비교할 수 있습니다."
  )

  st.markdown("---")

  # ==========================================
  # 두 번째 그래프: 장르 내 영화 트리맵 (총 관객 기준)
  # ==========================================
  st.header("2. 장르별 개별 영화 총 관객 수 트리맵")
  st.markdown(
      "각 장르(상위 그룹) 안에 포함된 개별 영화들을 트리맵으로 표현하고, 칸의"
      " 면적을 통해 **총 관객 수**의 규모를 비교합니다."
  )

  # Plotly 트리맵 생성
  fig_treemap = px.treemap(
      df,
      path=["genre", "movieNm"],
      values="total_audi",
      title="장르 및 영화별 총 관객 수 분포",
      custom_data=["movieNm", "total_audi", "genre"],
  )

  fig_treemap.update_traces(
      hovertemplate=(
          "<b>영화명:</b> %{customdata[0]}<br><b>장르:</b>"
          " %{customdata[2]}<br><b>총 관객 수:</b>"
          " %{customdata[1]:,}명<br><extra></extra>"
      )
  )

  # 그래프 출력
  st.plotly_chart(fig_treemap, use_container_width=True)

  # '이 그래프로 알 수 있는 것' 구역 (2)
  st.markdown("---")
  st.subheader("💡 이 그래프로 알 수 있는 것 (2)")
  st.info(
      "• 각 장르별 전체 흥행 규모와 함께, **어떤 개별 영화가 해당 장르 내에서"
      " 가장 큰 관객 지분을 차지하고 있는지** 직관적으로 파악할 수 있습니다.\n•"
      " 장르 간의 전반적인 흥행 파워와 블록버스터 영화들의 분포 관계를"
      " 한눈에 비교할 수 있습니다."
  )

  st.markdown("---")

  # ==========================================
  # 세 번째 그래프: 총 관객 수 히스토그램
  # ==========================================
  st.header("3. 총 관객 수 분포 히스토그램")
  st.markdown(
      "영화별 총 관객 수의 전체적인 분포 형태와 빈도수를 히스토그램으로"
      " 살펴봅니다."
  )

  # Plotly 히스토그램 생성 (hover_data에 영화명을 추가하여 마우스오버 시 표시)
  fig_hist = px.histogram(
      df,
      x="total_audi",
      nbins=20,
      title="총 관객 수 구간별 영화 편수 분포",
      labels={"total_audi": "총 관객 수", "count": "영화 편수"},
      hover_data=["movieNm", "genre"],
  )

  # 그래프 출력
  st.plotly_chart(fig_hist, use_container_width=True)

  # 데이터 분석 자동화 (가장 관객이 많은 영화 찾기)
  max_audi_row = df.loc[df["total_audi"].idxmax()]
  max_movie_name = max_audi_row["movieNm"]
  max_audi_val = max_audi_row["total_audi"]

  # '이 그래프로 알 수 있는 것' 구역 (3)
  st.markdown("---")
  st.subheader("💡 이 그래프로 알 수 있는 것 (3)")
  st.info(
      f"• 대부분의 영화는 저~중관객 구간에 집중적으로 몰려 있으며, 흥행 영화와"
      f" 일반 영화 간의 관객 수 격차가 뚜렷하게 나타납니다.\n• 본 데이터셋에서"
      f" **가장 관객이 많은 영화**는 **'{max_movie_name}'**(약"
      f" {max_audi_val:,}명)입니다."
  )

except Exception as e:
  st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
