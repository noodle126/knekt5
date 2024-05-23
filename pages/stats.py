import streamlit as st
import pandas as pd
import components.all as ac

ac.hideSideBar()
ac.topHeader()
# Load data (example)
# data = {
#     'Country': ['USA', 'China', 'Japan', 'Russia'],
#     'Best Athlete': ['Michael Phelps', 'Liu Xiang', 'Kohei Uchimura', 'Alexander Karelin'],
#     'Ranking': [1, 2, 3, 4],
#     'Gold Medals in Sport': ['Swimming', 'Gymnastics', 'Gymnastics', 'Wrestling']
# }

# df = pd.DataFrame(data)
df= pd.read_csv('/data/in/tables/CLEAN_OLYMPIC_MEDALS.csv')

# Title of the app
# st.title("Olympics Data Explorer")
st.title(df.count())


# # Select favorite country
# selected_country = st.selectbox("Select your favorite country", df['country_name'])

# # Display relevant data for the selected country
# if selected_country:
#     country_data = df[df['Country'] == selected_country]
#     best_athlete = country_data['Best Athlete'].values[0]
#     ranking = country_data['Ranking'].values[0]
#     sport_with_most_gold = country_data['Gold Medals in Sport'].values[0]

#     st.header(f"Data for {selected_country}")
#     st.write(f"Best Athlete: {best_athlete}")
    # st.write(f"Ranking: {ranking}")
    # st.write(f"Sport with Most Gold Medals: {sport_with_most_gold}")

# Footer
st.write("Powered by Streamlit")
