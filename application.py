from flask import Flask, render_template, request
import requests
from src.pipelines.predication_pipeline import PredictPipeline, CustomMovie

app = Flask(__name__)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=your_api_key&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        movie_title = request.form.get('movie')
        if movie_title:
            predict_pipeline = PredictPipeline()
            recommended_movie_names = predict_pipeline.recommend(movie_title)
            recommended_movie_posters = [fetch_poster(movie_id) for movie_id in recommended_movie_names]
            return render_template('home.html', movie_names=recommended_movie_names, posters=recommended_movie_posters, zip=zip)
    return render_template('home.html', zip=zip)

if __name__ == '__main__':
    app.run(debug=True)