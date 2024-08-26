# CineM8 #
This is your personal guide to the world of cinema! Whether you're a film buff looking for your next great watch, a casual viewer exploring new genres, or just curious about a specific movie, this website is designed with you in mind..

## Aim ##
This NLP suggests movies based on a rotten-tomatoes database and the movie database(tmdb) and processes film suggestions as per its similarities, genres, cast, production company, similar keywords with other films.

## Tech Stack used ##
For the Frontend part: streamlit, a python framework to ease out component-wise rendering within python.
For Data Procesing: numpy, pandas
For developing NLP: nltk, scikit-learn, pickle

## Future Improvvements ##
With our NLP, if we can scrape the data on similar lines from social media websites (which we could not achieve during the hackathon), it can be of mass usage for businesses and can also be applied for building user personas.

To run the code, in the project directory, run to install all dependencies:
```
pip3 install . -r requirements.txt
```
For launching the streamlit app, run:
```
streamlit run main.py
```
