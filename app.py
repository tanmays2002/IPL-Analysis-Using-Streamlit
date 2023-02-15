import streamlit as st
from ipl_analysis import *
import plotly.express as px



st.set_page_config(layout="wide")
st.header('------------------------- IPL Data Analysis -----------------------------')
option = st.sidebar.selectbox('Select Analysis Type',['Batsman Analysis','Bolwer Analysis','Teams Analysis'])

if option == 'Batsman Analysis':
    bat_name = st.sidebar.selectbox('Select the Batsman',batsman_name())
    btn1 = st.sidebar.button('Find Batsman Analysis')
    if btn1:
        st.title('Batsman Analysis')
        st.header(bat_name)
        result = batsman(bat_name)
        st.dataframe(result,width=500)
        scatter_1 = scatter[scatter['batter']==bat_name]
        fig1 = px.scatter(scatter_1,x='batsman_run',y='ballnumber',size='batsman_run',color='Season',hover_name='Venue',title='Batsman Carrer Record')
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
        fig = pie_chart(bat_name)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(fig)



elif option == 'Bolwer Analysis':
    bol_name = st.sidebar.selectbox('Select the Bolwer',bolwer_name())
    btn2 = st.sidebar.button('Find Bowler Analysis')
    if btn2:
        st.title('Bowler Analysis')
        st.header(bol_name)
        result1 = bolwer(bol_name)
        st.dataframe(result1,width=400)
        bolwer1 = bolwe[bolwe['bowler'] == bol_name]
        fig1 = px.scatter(bolwer1,x='batsman_run',y='isWicketDelivery',size='isWicketDelivery',color='Season',hover_name='Venue',title='Bolwer Carrer Record')
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)





else:
    team1 = st.sidebar.selectbox('Select first Team ',team_name())
    team2 = st.sidebar.selectbox('Select second Team',team_name())
    btn3 = st.sidebar.button('Find Teams Analysis')
    if btn3:
        st.title('Team Vs Team Analysis')

        #Pie Chart
        df = matches[((matches['Team1'] == team1) & (matches['Team2'] == team2)) | ((matches['Team1'] == team2) & (matches['Team2'] == team1))]
        data = [[team1, df[df['WinningTeam'] == team1].shape[0]], [team2, df[df['WinningTeam'] == team2].shape[0]]]
        df = pd.DataFrame(data, columns=['Team Name', 'Wins'])
        fig = px.pie(df, values='Wins', names='Team Name', title='Team Vs Team Wins', color='Team Name')
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        # Highest Run Scorer and Highest Wicket Taker
        data = df1[(df1['Team1'] == team1) & (df1['Team2'] == team2) | (df1['Team1'] == team2) & (df1['Team2'] == team1)]
        run = data.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head(5).reset_index()
        mask1 = data[(data['kind'] != 'run out') & (data['isWicketDelivery'] == 1)]
        wicket = mask1.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head(5).reset_index()
        col1, col2 = st.columns(2)
        col1.header('Top 5 Batsman')
        col1.dataframe(run)
        col2.header('Top 5 Bowler')
        col2.dataframe(wicket)



