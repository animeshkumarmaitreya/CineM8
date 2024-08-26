import streamlit as st
import streamlit_option_menu
from streamlit_extras.stoggle import stoggle
from processing import nlp
from processing.makedb import Main
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript

st.set_page_config(
    page_title="A3S",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Report a bug":"https://docs.google.com/forms/d/e/1FAIpQLSdjGJiG_aVCQhHwGZqIbSm5SBzTPhCCYMtCkG2R58M_4_WHyw/viewform?usp=sf_link",
        "About":"""
            ### Welcome to CineM8 
            This is your personal guide to the world of cinema! Whether you're a film buff looking for your next great watch, a casual viewer exploring new genres, or just curious about a specific movie, this website is designed with you in mind..
        """,
    }
)
displayed=[]
if 'movie_number' not in st.session_state:
    st.session_state['movie_number'] = 0

if 'selected_movie_name' not in st.session_state:
    st.session_state['selected_movie_name'] = ""

if 'user_menu' not in st.session_state:
    st.session_state['user_menu'] = ""

def main():
    def initial_options():
        components.html(
            """
            <div style="background-color: #FFD700; padding: 20px; border-radius: 10px;">
                <h1 style='text-align: center; color: #300'>Welcome to CineM8</h1>
            </div>
            """,
            height=150
        )
        st.title("What Are You Looking For? \n#### Get the best movie recommends powered with AI ! #### ")
        col1,col2,col3,col4,col5,col6=st.columns(6)
        with col1:
            if st.button("Recommend me a similar movie"):
                st.session_state.user_menu = "Recommend me a Similar movie"
        with col2:
            if st.button("Describe me a movie"):
                st.session_state.user_menu = "About the selected Movie"

        if "user_menu" in st.session_state:
           if st.session_state.user_menu == "Recommend me a Similar Movie":
            recommend_display()
           elif st.session_state.user_menu == "About the selected Movie":
            display_movie_details()
        paging_movies()
    
    def recommend_display():
        st.title('A3S')
        selected_movie_name = st.selectbox(
            'Select a Movie...', new_df['title'].values
        )
        rec_button=st.button('Recommend')
        if rec_button:
            st.session_state.selected_movie_name = selected_movie_name
            recommendation_tags(new_df, selected_movie_name, r'data/similarity_tags_tags.pkl',"are")
            recommendation_tags(new_df, selected_movie_name, r'data/similarity_tags_genres.pkl',"on the basis of genres are")
            recommendation_tags(new_df, selected_movie_name,
                                r'data/similarity_tags_tprduction_comp.pkl',"from the same production company are")
            recommendation_tags(new_df, selected_movie_name, r'data/similarity_tags_keywords.pkl',"on the basis of keywords are")
            recommendation_tags(new_df, selected_movie_name, r'data/similarity_tags_tcast.pkl',"on the basis of cast are")

    def recommendation_tags(new_df, selected_movie_name, pickle_file_path,str):
        movies,posters=nlp.recommend(new_df, selected_movie_name, pickle_file_path)
        st.subheader(f'Best Recommendations {str}...')
        rec_movies=[]
        rec_posters=[]
        cnt=0
        for i,j in enumerate(movies):
            if cnt==10:
                break
            if j not in displayed:
                rec_movies.append(j)
                rec_posters.append(posters[i])
                displayed.append(j)
                cnt+=1
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            st.text(rec_movies[0])
            st.image(rec_posters[0])
        with col2:
            st.text(rec_movies[1])
            st.image(rec_posters[1])
        with col3:
            st.text(rec_movies[2])
            st.image(rec_posters[2])
        with col4:
            st.text(rec_movies[3])
            st.image(rec_posters[3])
        with col5:
            st.text(rec_movies[4])
            st.image(rec_posters[4])

    def display_movie_details():
        selected_movie_name=st.session_state.selected_movie_name
        info=nlp.get_details(selected_movie_name)
        with st.container():
            image_col,text_col=st.columns((1, 2))
            with image_col:
                st.text('\n')
                st.image(info[0])

            with text_col:
                st.text('\n')
                st.text('\n')
                st.title(selected_movie_name)
                st.text('\n')
                st.write("OVERVIEW")
                st.write(info[3], wrapText=False)
                st.text('\n')
                col1,col2,col3=st.columns(3)
                with col1:
                    st.text("Rating")
                    st.write(info[8])
                with col2:
                    st.text("No. of ratings")
                    st.write(info[9])
                with col3:
                    st.text("Runtime")
                    st.write(info[6])
                st.text('\n')
                col1,col2,col3=st.columns(3)
                with col1:
                    str=""
                    st.text("Genres")
                    for i in info[2]:
                        str=str+i+"  "
                    st.write(str)
                with col2:
                    str=""
                    st.text("Languages")
                    for i in info[13]:
                        str=str+i+"  "
                    st.write(str)
                with col3:
                    st.text("Directed By")
                    st.text(info[12][0])
                st.text('\n')
                col1,col2,col3=st.columns(3)
                with col1:
                    st.text("Release Date")
                    st.text(info[4])
                with col2:
                    st.text("Budget")
                    st.text(info[1])
                with col3:
                    st.text("Revenue")
                    st.text(info[5])
                st.text('\n')
        st.header('Cast')
        cnt=0
        urls=[]
        bio=[]
        for i in info[14]:
            if cnt==10:
                break
            url,biography=nlp.fetch_person_details(i)
            urls.append(url)
            bio.append(biography)
            cnt+=1
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            st.image(urls[0])
            stoggle(
                "Show More",
                bio[0],
            )
        with col2:
            st.image(urls[1])
            stoggle(
                "Show More",
                bio[1],
            )
        with col3:
            st.image(urls[2])
            stoggle(
                "Show More",
                bio[2],
            )
        with col4:
            st.image(urls[3])
            stoggle(
                "Show More",
                bio[3],
            )
        with col5:
            st.image(urls[4])
            stoggle(
                "Show More",
                bio[4],
            )
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            st.image(urls[5])
            stoggle(
                "Show More",
                bio[5],
            )
        with col2:
            st.image(urls[6])
            stoggle(
                "Show More",
                bio[6],
            )
        with col3:
            st.image(urls[7])
            stoggle(
                "Show More",
                bio[7],
            )
        with col4:
            st.image(urls[8])
            stoggle(
                "Show More",
                bio[8],
            )
        with col5:
            st.image(urls[9])
            stoggle(
                "Show More",
                bio[9],
            )

    def paging_movies():
        st.divider()
        max_pages=movies.shape[0]//10
        col1,col2,col3,col4,col5,col6=st.columns([1,1,5,2,1,1])
        with col1:
            st.text("Previous page")
            prev_btn=st.button("Prev")
            if prev_btn:
                if st.session_state['movie_number']>=10:
                    st.session_state['movie_number']-=10
        with col2:
            st.text("Next page")
            next_btn=st.button("Next")
            if next_btn:
                if st.session_state['movie_number']+10<len(movies):
                    st.session_state['movie_number']+=10
        with col3:
            new_page_number=st.number_input("Jump to page number", min_value=0, max_value=max_pages, value=st.session_state['movie_number']//10)
            jump_btn=st.button("Enter")  
            if jump_btn:
                st.session_state['movie_number']=new_page_number*10
        display_all_movies(st.session_state['movie_number'])

    def display_all_movies(start):
        st.divider()
        i=start
        with st.container():
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link,caption=movies['title'][i])
                i=i+1
            with col2:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i=i+1
            with col3:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i=i+1
            with col4:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link,caption=movies['title'][i])
                i=i+1
            with col5:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link,caption=movies['title'][i])
                i=i+1
        with st.container():
            col1,col2,col3,col4,col5=st.columns(5)
            with col1:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link,caption=movies['title'][i])
                i=i+1
            with col2:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link,caption=movies['title'][i])
                i=i+1
            with col3:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link,caption=movies['title'][i])
                i=i+1
            with col4:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link,caption=movies['title'][i])
                i=i+1
            with col5:
                id=movies.iloc[i]['movie_id']
                link=nlp.fetch_posters(id)
                st.image(link,caption=movies['title'][i])
                i=i+1
        st.session_state['page_number']=i
    with Main() as bot:
        bot.main_()
        new_df, movies, movies2 = bot.getter()
        initial_options()

if __name__ == '__main__':
    main()
