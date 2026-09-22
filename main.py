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

  # '이 그래프로 알 수 있는 것' 구역
  st.markdown("---")
  st.subheader("💡 이 그래프로 알 수 있는 것")
  st.info(
      "• 1년 동안 박스오피스 상위권에 가장 많이 이름을 올린 **주요 인기 장르**가"
      " 무엇인지 파악할 수 있습니다.\n• 전체 영화 중 특정 장르가 차지하는"
      " **상대적인 비중(%)**을 한눈에 비교할 수 있습니다."
  )

  # (추가로 필요한 다른 그래프를 이 아래에 계속해서 확장할 수 있습니다)

except Exception as e:
  st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
