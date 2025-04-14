import pickle
import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv('TMDB_API_KEY')

# Custom CSS for responsive UI, teal background, and clear text
st.markdown("""
    <style>
    /* Global styles */
    .main {
        background: linear-gradient(135deg, #0A6C74 0%, #1E8E8E 100%);
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
        padding: 20px;
        min-height: 100vh;
        animation: backgroundFade 12s infinite alternate;
        
    }
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    h1 {
        color: #FF9F1C;
        text-align: center;
        font-size: clamp(2em, 5vw, 2.8em);
        text-shadow: 2px 2px 6px rgba(0,0,0,0.4);
        animation: fadeIn 1s ease-in;
    }
    .movie-card {
        background: #1A3C44;
        border-radius: 12px;
        padding: clamp(8px, 2vw, 12px);
        text-align: center;
        transition: transform 0.4s ease, box-shadow 0.4s ease, opacity 0.6s ease;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        opacity: 0;
        transform: translateY(20px);
        animation: slideUp 0.5s ease forwards;
        animation-delay: calc(0.1s * var(--index));
        width: 100%;
        max-width: 250px;
        margin: 0 auto;
    }
    .movie-card:hover {
        transform: scale(1.08);
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .movie-poster {
        border-radius: 8px;
        width: 100%;
        height: auto;
        transition: transform 0.3s ease;
    }
    .movie-poster:hover {
        transform: scale(1.05);
    }
    .movie-title {
        color: #F5F6F5;
        font-size: clamp(1.1em, 2.8vw, 1.3em);
        font-weight: 600;
        margin: 12px 0;
        height: 60px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF9F1C, #F48C06);
        color: white;
        border: none;
        padding: clamp(10px, 2vw,12px) clamp(20px, 4vw, 24px);
        border-radius: 30px;
        font-size: clamp(0.9em, 2vw, 1.1em);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(255,159,28,0.5);
        animation: pulse 1.5s infinite;
    }
    .stSelectbox {
        background: #1A3C44;
        border-radius: 12px;
        padding: 8px;
        color: #e0e0e0;
        font-size: clamp(0.9em, 2vw, 1em);
    }
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }
    .theme-toggle button {
        background: #FF9F1C;
        border-radius: 20px;
        padding: clamp(6px, 1.5vw, 8px) clamp(12px, 3vw, 16px);
        font-size: clamp(0.8em, 2vw, 0.9em);
    }
    .error-message {
        color: #FF9F1C;
        text-align: center;
        font-size: clamp(1.1em, 2.5vw, 1.3em);
        margin: 30px 0;
        animation: fadeIn 0.5s ease;
    }
    .loading-spinner {
        text-align: center;
        font-size: clamp(1.1em, 2.5vw, 1.3em);
        color: #FF9F1C;
        animation: fadeIn 0.5s ease;
    }
    /* Light theme */
    .light-theme .main {
        background: linear-gradient(135deg, #E6F3F3 0%, #CFF1F1 100%);
        color: #333;
    }
    .light-theme h1 {
        color: #F48C06;
    }
    .light-theme .movie-card {
        background: #F5F6F5;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .light-theme .movie-title {
        color: #1A3C44;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
    }
    .light-theme .stSelectbox {
        background: #DDE4E4;
        color: #333;
    }
    .light-theme .theme-toggle button {
        background: #F48C06;
    }
    /* Animations */
    @keyframes slideUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    @keyframes backgroundFade {
        from {
            background: linear-gradient(135deg, #0A6C74 0%, #1E8E8E 100%);
        }
        to {
            background: linear-gradient(135deg, #1E8E8E 0%, #0A6C74 100%);
        }
    }
    /* Responsive design */
    @media (max-width: 1024px) {
        .stApp {
            padding: 10px;
        }
        .movie-card {
            max-width: 200px;
        }
        .theme-toggle {
            top: 15px;
            right: 15px;
        }
    }
    @media (max-width: 768px) {
        .stColumns {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
        }
        .movie-card {
            max-width: 45%;
            margin-bottom: 15px;
        }
        h1 {
            font-size: 2em;
        }
    }
    @media (max-width: 480px) {
        .movie-card {
            max-width: 100%;
        }
        .theme-toggle {
            top: 10px;
            right: 10px;
        }
        .stButton>button {
            width: 100%;
        }
        .stSelectbox {
            width: 100%;
        }
        .movie-title {
            font-size: 1.1em;
            height: 56px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Cache API calls
@st.cache_data
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image+Available"
    except requests.RequestException:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        return [], []

# Load data
try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Movie data files are missing. Please ensure 'movie_list.pkl' and 'similarity.pkl' are available.")
    st.stop()

# Theme toggle state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Theme toggle button with key to detect click
theme_button_key = "theme_toggle"
if st.button(f"Switch to {'Light' if st.session_state.theme == 'dark' else 'Dark'} Mode", key=theme_button_key):
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# Apply theme class
st.markdown(f'<div class="{st.session_state.theme}-theme">', unsafe_allow_html=True)

# UI Elements
st.markdown('<div class="theme-toggle">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.header('🎥 Movie Recommender System')

# Searchable selectbox
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Search or select a movie",
    movie_list,
    format_func=lambda x: x.title(),
    help="Type to find your favorite movie"
)

if st.button('Get Recommendations'):
    with st.spinner('Curating your movie picks...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        if recommended_movie_names:
            st.markdown("### Your Movie Picks")
            with st.container():
                cols = st.columns([1, 1, 1, 1, 1] if len(recommended_movie_names) >= 5 else len(recommended_movie_names))
                for idx, (name, poster) in enumerate(zip(recommended_movie_names, recommended_movie_posters)):
                    with cols[idx % len(cols)]:
                        st.markdown(f"""
                            <div class="movie-card" style="--index: {idx};">
                                <img src="{poster}" class="movie-poster" alt="{name} poster">
                                <div class="movie-title">{name}</div>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-message">No recommendations found for this movie!</div>', unsafe_allow_html=True)
else:
    st.info("Pick a movie and hit 'Get Recommendations' to discover new films!")

st.markdown('</div>', unsafe_allow_html=True)  # Close theme div