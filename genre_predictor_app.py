import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 데이터 불러오기
df = pd.read_csv("netflix_titles.csv")
df = df[['description', 'listed_in']].dropna()

# 장르 전처리: 첫 번째 장르만 추출
df['main_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0].strip())

# 학습용 데이터 준비
X = df['description']
y = df['main_genre']

# 텍스트 벡터화
vectorizer = TfidfVectorizer(stop_words='english')
X_vec = vectorizer.fit_transform(X)

# 학습/테스트 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# 모델 학습
model = MultinomialNB()
model.fit(X_train, y_train)

# Streamlit UI
st.title("🎬 넷플릭스 장르 예측기")
st.write("줄거리 설명을 입력하면 적절한 장르를 예측하고 콘텐츠를 추천합니다.")

user_input = st.text_area("줄거리나 보고 싶은 분위기를 입력하세요:")

if user_input:
    input_vec = vectorizer.transform([user_input])
    predicted_genre = model.predict(input_vec)[0]
    st.success(f"예측된 장르: **{predicted_genre}**")

    st.markdown("📺 해당 장르의 추천 콘텐츠:")
    recs = df[df['main_genre'] == predicted_genre].sample(5)
    for idx, row in recs.iterrows():
        st.write(f"- {row['description'][:100]}...")
