# valorantEsports

This project is a collection of the code, graphs and analyses that i've created while trying to answer some questions about the video game "Valorant", developed by Riot Games, and it's esports domain. 

I've added a short description (question being answered, analysis methods used, conclusion, other thoughts) for each file

“mastersCopenhagen2022MVP.py”:
Here I wanted to see who was the best player during Valorant’s “Stage 2: Master’s Copenhagen” tournament. 
I selected the highest performing players from the grand finals of the tournament, using VLR.gg as my main resource. To analyze each player’s performance, I generated 4 radar/spider charts, one for the last 4 maps played in the grand finals. Then, the variables I examined were Kills, ACS, K-D Difference, Assists, KAST%, ADR, HS%, First Kills, and First Kill Difference. I then overlaid the top 5 players on top of each other, with the intention that the best players would take up the most area of the radar chart. I built my radar charts similar to how matplotlib does it in their documentation (https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html).
My conclusion is that while Jingg did do really well despite losing, the MVP award should have gone to either Shao or SUGETSU on the winning team. 
I think that while the use of radar charts was really good to visualize the data, some of the metrics I used(Assists and HS% in particular) weren’t necessarily the best metrics to use, as a low number of Assists or low HS% doesn’t necessarily mean that a player is good/bad. Sure, these metrics could hint how efficient/good a player is, but I think it did more harm than good, especially during Jinggg’s performance on Haven. 
