import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRcGdAVJcNCjJ_aPe1NBfw-wmZuErcr6zHPZ0WQq05kguiecHVl2kQO2hiqTIJaZOGG89HdpgOdqZI9/pub?output=csv'
matches = pd.read_csv(url)

balls = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSeW__6fFE4WnNm696CUBBsOpP1aTLPlZyqGW6Xw_R6DI_mpDsNeE9d6Iu_hJZ3HbDfb4dg8IFYFbNG/pub?output=csv')

df1 = balls.merge(matches, on='ID', how='outer').copy()

df1['BattingTeam'] = df1['BattingTeam'].replace('Rising Pune Supergiants','Rising Pune Supergiant')
df1['Team2'] = df1['BattingTeam'].replace('Rising Pune Supergiants','Rising Pune Supergiant')
df1['Team2'] = df1['BattingTeam'].replace('Rising Pune Supergiants','Rising Pune Supergiant')

def batsman_name():
    return sorted(list(df1['batter'].unique()))

def bolwer_name():
    return sorted(list(df1['bowler'].unique()))

def team_name():
    return sorted(list(df1['Team1'].unique()))


def teamVteam(team1,team2):
  df = matches[((matches['Team1'] == team1) & (matches['Team2'] == team2)) | ((matches['Team1'] == team2) & (matches['Team2'] == team1))]
  mp = df.shape[0]
  team1_win =   df[df['WinningTeam'] == team1].shape[0]
  team2_win = df[df['WinningTeam'] == team2].shape[0]
  df2 = df[(df['TossWinner'] == team1) & (df['WinningTeam'] == team1) | (df['TossWinner'] == team2) & (df['WinningTeam'] == team2)]
  toss_jito_match_jito_prob =  round(((df2.shape[0]) /mp ) * 100,0)
  mom = df['Player_of_Match'].value_counts().sort_values(ascending=False).head(3)

  # Highest Run Scorer and Highest Wicket Taker
  data = df1[(df1['Team1']== team1) & (df1['Team2']==team2) | (df1['Team1']== team2) & (df1['Team2']==team1)]
  run = data.groupby('batter')['batsman_run'].sum().sort_values(ascending=False).head(5)
  mask1 = data[(data['kind'] != 'run out') & (data['isWicketDelivery'] == 1)]
  wicket = mask1.groupby('bowler')['isWicketDelivery'].sum().sort_values(ascending=False).head(5)

  # return wicket
  return {
      'Matches Played':mp,
      team1:team1_win,
      team2:team2_win,
      'toss_jito_match_jito_prob':toss_jito_match_jito_prob,
      'Man of the Match':mom,
      'Highest Run Scorer': run.reset_index(),
      'Highest Wicket Taker':(wicket)
  }


# batstman record created for streamlit app
def batsman(name):
    res = df1[df1['batter'] == name]
    innings = len(res['ID'].unique())
    runs = res['batsman_run'].sum()
    balls = res[res['extra_type'] != 'wides'].shape[0]
    highest_score = \
    res.groupby('ID')['batsman_run'].sum().sort_values(ascending=False).head(1).reset_index()['batsman_run'][0]
    avg = round(runs/res[res['player_out']==name].shape[0],2)
    strike_rate = round((runs / balls) * 100, 2)
    temp = res.groupby('ID')['batsman_run'].sum().reset_index()
    fifty = temp[temp['batsman_run'] >= 50].shape[0]
    hundreds = temp[temp['batsman_run'] >= 100].shape[0]
    fours = res[res['batsman_run'] == 4].shape[0]
    six = res[res['batsman_run'] == 6].shape[0]
    return pd.DataFrame({'Values': [round(innings),runs,balls,highest_score,avg,strike_rate,fifty,hundreds,fours,six]},
                      index=['Innings', 'Runs', 'Balls', 'Highest Score','Average','Strike Rate','Fifty','Hundreds','Fours','Sixes'])

# Pie chart for the distribution of runs
def pie_chart(name):
  res = df1[df1['batter']==name]
  runs = res['batsman_run'].sum()
  fours = res[res['batsman_run']==4].shape[0]
  six = res[res['batsman_run']==6].shape[0]
  a = fours * 4
  b = six * 6
  c = runs - a -b
  fig, ax = plt.subplots()
  share = [a, b, c]
  labels = ['Fours', 'Six', 'Ones & Twos']
  plt.style.use('ggplot')
  plt.title('Distribution of Total Runs In IPL')
  plt.axis('equal')
  colors = ['#12FCF8','#FC2412','#AEFC12']
  explode = [0, 0.1, 0]
  ax.pie(x=share, labels=labels,explode=explode, shadow=True,startangle=90,colors=colors ,autopct='%.2f%%')
  return plt.show()


def bolwer(name):
    sol = df1[df1['bowler'] == name]
    innings = len(sol['ID'].unique())
    balls = (sol.shape[0]) - (sol[sol['extra_type'] == 'noballs'].shape[0]) - (
    sol[sol['extra_type'] == 'wides'].shape[0])
    runs = sol[(sol['extra_type'] != 'legbyes') & (sol['extra_type'] != 'noballs') & (sol['extra_type'] != 'byes')][
        'total_run'].sum()
    temp = sol.groupby(['ID', 'overs'])['total_run'].sum().reset_index()
    maidens = temp[temp['total_run'] == 0].shape[0]
    a = sol[sol[(sol['kind'] != 'retired hurt') | (sol['kind'] != 'retired out') | (
                sol['kind'] != 'obstructing the field')]['isWicketDelivery'] == 1]
    wickets = a[a['kind'] != 'run out'].shape[0]
    avg = round(runs / wickets, 2)
    Economy = round(runs / (balls / 6), 1)
    strike_rate = round(balls / wickets, 1)
    obj = sol.groupby('ID')
    best_bowling_performances = obj.agg({
        'isWicketDelivery': 'sum',
        'total_run': 'sum'
    }).sort_values(['isWicketDelivery', 'total_run'], ascending=[False, True]).head(5)
    best_bowling_performances
    b = obj['isWicketDelivery'].sum().reset_index()
    three_wicket = b[b['isWicketDelivery'] >= 3].shape[0]
    five_wicket = b[b['isWicketDelivery'] >= 5].shape[0]
    return pd.DataFrame({'Values': [innings,balls,runs,maidens,wickets,avg,Economy,strike_rate,three_wicket,five_wicket]},
                      index=['Innings', 'Balls', 'Runs' ,'Maidens Overs','Wickets','Average','Economy','Strike Rate','Three Wickets','Five Wickets'])


#Scatter chart of record of player
group = balls.groupby(['ID','batter'])
runs = group['batsman_run'].sum().reset_index()
ball = group['ballnumber'].count().reset_index()
scatter_temp = runs.merge(ball,left_on=['ID','batter'],right_on=['ID','batter'],how='left').reset_index()
scatter = scatter_temp.merge(matches,on='ID',how='left').reset_index()[['ID','Date','Venue','Season','batter','batsman_run','ballnumber']]


#Scatter Chart for record of the bolwer
group1 = balls.groupby(['ID','bowler'])
runs1 = group1['isWicketDelivery'].sum().reset_index()
ball1 = group1['batsman_run'].sum().reset_index()
bow = runs1.merge(ball1,left_on=['ID','bowler'],right_on=['ID','bowler'],how='left').reset_index()
bolwe = bow.merge(matches,on='ID',how='left').reset_index()[['ID','Date','Venue','Season','bowler','batsman_run','isWicketDelivery']]
