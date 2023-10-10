import json
from aoai import aoai
import streamlit as st


def MovieRecommender(aoai: aoai=aoai()):
    system_msg, user_msg, assitant_msg = prompt_samples() 

    movie_watch_list = """
I've watched
[{'Movie Name': 'The Perks of Being a Wallflower (2012)', 'Rating': 9},
 {'Movie Name': 'The Great Gatsby (2013)', 'Rating': 5},
 {'Movie Name': 'Prisoners (2013)', 'Rating': 10},
 {'Movie Name': 'Argo (2012)', 'Rating': 9},
 {'Movie Name': 'Chronicle (2012)', 'Rating': 6},
 {'Movie Name': 'American Beauty (1999)', 'Rating': 7},
 {'Movie Name': 'Drive (2011)', 'Rating': 8},
 {'Movie Name': 'Welcome to the Punch (2013)', 'Rating': 6},
 {'Movie Name': 'Trance (2013)', 'Rating': 8},
 {'Movie Name': 'The Counselor (2013)', 'Rating': 7},
 {'Movie Name': 'Zodiac (2007)', 'Rating': 8},
 {'Movie Name': 'The Place Beyond the Pines (2012)', 'Rating': 5},
 {'Movie Name': 'The Prestige (2006)', 'Rating': 8},
 {'Movie Name': 'Trainspotting (1996)', 'Rating': 7},
 {'Movie Name': 'Hes Just Not That Into You (2009)', 'Rating': 7},
 {'Movie Name': 'Easy A (2010)', 'Rating': 7},
 {'Movie Name': 'Brothers (2009)', 'Rating': 8},
 {'Movie Name': 'The Social Network (2010)', 'Rating': 7},
 {'Movie Name': 'The Island (2005)', 'Rating': 5},
 {'Movie Name': 'Despicable Me (2010)', 'Rating': 7},
 {'Movie Name': 'The Hurt Locker (2008)', 'Rating': 7},
 {'Movie Name': 'Labyrinth (1986)', 'Rating': 8},
 {'Movie Name': 'Pirates of the Caribbean Dead Mans Chest (2006)', 'Rating': 7},
 {'Movie Name': 'La haine (1995)', 'Rating': 8},
 {'Movie Name': 'Watchmen (2009)', 'Rating': 7},
 {'Movie Name': 'Harry Brown (2009)', 'Rating': 7},
 {'Movie Name': 'White Chicks (2004)', 'Rating': 5},
 {'Movie Name': 'Miss Congeniality 2 Armed and Fabulous (2005)', 'Rating': 4},
 {'Movie Name': 'We Own the Night (2007)', 'Rating': 6},
 {'Movie Name': 'The Longest Yard (2005)', 'Rating': 8},
 {'Movie Name': 'Miss Congeniality (2000)', 'Rating': 7},
 {'Movie Name': 'Hunky Dory (2011)', 'Rating': 5}]
"""

    # sidebar
    with st.sidebar:
        with st.container():
            st.info("Recommend movies based on your preferences. Type a question and click __Ask__ button to get answer.")
        sample_tab, system_tab = st.tabs(["samples", "system"])
        with sample_tab:
            st.write("## Sample Questions")
            st.code("Would you recommend me the movie 'Pirates of the Caribbean The Curse of the Black Pearl (2003)'?", language="html")
            st.code("The Conjuring (2013)", language="html")
            st.code("Gangster Squad (2013)", language="html")
        with system_tab:
            st.write("## System Message")
            st.text_area(label="System", value=system_msg, height=550)
            st.text_area(label="movie and rating", value=movie_watch_list, height=850)
            st.info("I've watched the movie, 'Pirates of the Caribbean The Curse of the Black Pearl (2003)' and I rated it 8.0 out of 10.0")

    st.markdown("# Movie Recommender")
    st.markdown("This demo will show you how to use Azure OpenAI to recommend movies based on your preferences")
    with st.expander("Demo scenario"):
        st.image("https://github.com/hyssh/azure-openai-quickstart/blob/main/images/Architecture-demo.png?raw=true")
        st.markdown("1. User will type text (multi lines) in the input box")
        st.markdown("2. __Web App__ sends the text to __Azure OpenAI__")
        st.markdown("3. __Azure OpenAI__ review the movie list and return the recommended movies with scores in JSON format")
        st.markdown("4. __Web App__ shows the results on screen")

    user_prompt = "Would you recommend me the movie 'Pirates of the Caribbean The Curse of the Black Pearl (2003)'?"
    st.markdown("---")
    st.write("### Type movie name and AI will guess your rating")
    details_text = st.text_area(label="Details", 
                                height=3,
                                max_chars=150,
                                value=user_prompt)
    
    prompt = [{"role":"system", "content":system_msg},
              {"role":"user","content":user_msg},
              {"role":"assistant","content":assitant_msg},
              {"role":"user","content": movie_watch_list+details_text}
    ]
        
    with st.container():
        if st.button("Get recommendation"):
            st.spinner("Thinking... ")
            
            with st.container():
                st.write(f"{aoai.run(prompt=prompt, temperature=0.1, max_tokens=2000)}")
        else:
            with st.container():
                st.empty()

    
def prompt_samples():
    system_msg = """
You're going to recommend a movie to users based on their movie watch history.
As a professional personalization system, you're going to provide the following steps:

# Steps
## 1. Analyze movie watch history
[Add Genres to the movie watch history]

## 2. Calculate the weighted score for each genre

## 3. Cluster the movies based on the genres and weighted score

## 4. Predict User's Rating Score
[Using the weighted scores calculated earlier]
[When user ask for the recommendation score, provide the score, based on the rating history]
[Answer the question with the score first and then explain why you give the score in the next line]

# Safety
Do not show subtitle of each step above
    """

    examples_user_prompt ="""
I've watched
[{'Movie Name': 'Dallas Buyers Club (2013)', 'Rating': 9},
{'Movie Name': 'World Z (2013)', 'Rating': 7},
{'Movie Name': 'Gravity (2013)', 'Rating': 9},
{'Movie Name': 'Her (2013)', 'Rating': 10},
{'Movie Name': '12 Years a Slave (2013)', 'Rating': 8},
{'Movie Name': 'The Secret Life of Walter Mitty (2013)', 'Rating': 9},
{'Movie Name': 'The Grand Budapest Hotel (2014)', 'Rating': 10},
{'Movie Name': 'Riddick (2013)', 'Rating': 6},
{'Movie Name': 'Kick-Ass 2 (2013)', 'Rating': 7},
{'Movie Name': 'Star Trek Into Darkness (2013)', 'Rating': 7},
{'Movie Name': 'The Wolf of Wall Street (2013)', 'Rating': 10},
{'Movie Name': 'American Hustle (2013)', 'Rating': 7},
{'Movie Name': 'Nebraska (2013)', 'Rating': 10},
{'Movie Name': 'Inside Llewyn Davis (2013)', 'Rating': 10},
{'Movie Name': 'R.I.P.D. (2013)', 'Rating': 4},
{'Movie Name': 'The Book Thief (2013)', 'Rating': 9},
{'Movie Name': 'Last Vegas (2013)', 'Rating': 5},
{'Movie Name': 'The Purge (2013)', 'Rating': 3},
{'Movie Name': 'Runner Runner (2013)', 'Rating': 7},
{'Movie Name': 'The (2013)', 'Rating': 9},
{'Movie Name': 'The Worlds End (2013)', 'Rating': 9},
{'Movie Name': 'The Conjuring (2013)', 'Rating': 7},
{'Movie Name': 'Carrie (2013)', 'Rating': 8},
{'Movie Name': 'Don Jon (2013)', 'Rating': 8},
{'Movie Name': 'Vive la France (2013)', 'Rating': 7},
{'Movie Name': 'Saving Mr. Banks (2013)', 'Rating': 9},
{'Movie Name': 'The Kings of Summer (2013)', 'Rating': 7},
{'Movie Name': 'jOBS (2013)', 'Rating': 6},
{'Movie Name': 'This Is the End (2013)', 'Rating': 8},
{'Movie Name': 'Scary Movie 5 (2013)', 'Rating': 6},
{'Movie Name': 'Pain &amp; Gain (2013)', 'Rating': 7},
{'Movie Name': 'Bad Grandpa (2013)', 'Rating': 4},
{'Movie Name': 'Machete Kills (2013)', 'Rating': 7},
{'Movie Name': 'Filth (2013)', 'Rating': 9},
{'Movie Name': 'Hot Fuzz (2007)', 'Rating': 10},
{'Movie Name': 'The Starving Games (2013)', 'Rating': 4}]

Would you recommend me the movie, Garden State (2004)?
    """

    examples_assistant_res = """
1. Analyze movie watch history
Dallas Buyers Club (2013) - Drama  
World War Z (2013) - Action  
Gravity (2013) - Sci-Fi  
Her (2013) - Drama  
12 Years a Slave (2013) - Drama  
The Secret Life of Walter Mitty (2013) - Adventure  
The Grand Budapest Hotel (2014) - Comedy  
Riddick (2013) - Action  
Kick-Ass 2 (2013) - Action  
Star Trek Into Darkness (2013) - Sci-Fi  
The Wolf of Wall Street (2013) - Drama  
American Hustle (2013) - Drama  
Nebraska (2013) - Drama  
Inside Llewyn Davis (2013) - Drama  
R.I.P.D. (2013) - Action  
The Book Thief (2013) - Drama  
Last Vegas (2013) - Comedy  
The Purge (2013) - Horror  
Runner Runner (2013) - Thriller  
The (2013) - Unknown  
The Worlds End (2013) - Comedy  
The Conjuring (2013) - Horror  
Carrie (2013) - Horror  
Don Jon (2013) - Comedy  
Vive la France (2013) - Comedy  
Saving Mr. Banks (2013) - Drama  
The Kings of Summer (2013) - Comedy  
jOBS (2013) - Drama  
This Is the End (2013) - Comedy  
Scary Movie 5 (2013) - Comedy  
Pain & Gain (2013) - Action  
Bad Grandpa (2013) - Comedy  
Machete Kills (2013) - Action  
Filth (2013) - Drama  
Hot Fuzz (2007) - Comedy  
The Starving Games (2013) - Comedy  

2. Calculate the weighted score for each genre
Drama: (9+10+8+10+10+9+7+9+9)/9 = 9.0  
Action: (7+6+7+4+7)/5 = 6.2  
Sci-Fi: (9+7)/2 = 8.0  
Adventure: 9/1 = 9.0  
Comedy: (10+5+9+8+7+7+8+6+4+10+4)/11 = 6.8  
Horror: (3+7+8)/3 = 6.0  
Thriller: 7/1 = 7.0  
Unknown: 9/1 = 9.0  

3. Cluster the movies based on the genres and weighted score
Cluster 1 (High-rated dramas and adventures):  
- Dallas Buyers Club (2013)  
- Her (2013)  
- 12 Years a Slave (2013)  
- The Secret Life of Walter Mitty (2013)  
- The Wolf of Wall Street (2013)  
- American Hustle (2013)  
- Nebraska (2013)  
- Inside Llewyn Davis (2013)  
- The Book Thief (2013)  
- Saving Mr. Banks (2013)  
- jOBS (2013)  
- Filth (2013)  

Cluster 2 (High-rated sci-fi and unknown genres):  
- Gravity (2013)  
- Star

4. Predict User's Rating Score
To predict the rating for "Garden State (2004)," we can use the weighted scores of similar genres from the previous clustering and the user's preferences. "Garden State" is a romantic comedy-drama film. Based on the user's preferences, we can see that the user enjoys drama and comedy films.

Using the weighted scores calculated earlier:

Drama: 9.0
Comedy: 6.8

Since "Garden State" is a blend of both drama and comedy, we can take an average of the weighted scores of these two genres to predict the rating:

Predicted Rating = (Drama Weighted Score + Comedy Weighted Score) / 2
Predicted Rating = (9.0 + 6.8) / 2 = 7.9

So, based on the user's preferences and the movie's genres, we can predict that the user would likely rate "Garden State (2004)" around 7.9 out of 10.
    """
    return system_msg, examples_user_prompt, examples_assistant_res