# NBA official injury report
We want to group all the reports into one big dataframe. We ran into some issues:
1. The NBA official injury report has 5 differnt formats since it started publishing:

- 2018/12/17 - 2019/11/14 format:
[Game Date, Game Time, Matchup, Team, Player Name, Category, Reason, Current Status, Previous Status]
![1](https://user-images.githubusercontent.com/70581662/94700143-d5d30280-0343-11eb-94ea-cc2fc85a4545.png)<br />


- 2019/12/17 format:
[Game Date, Game Time, Matchup, Team, Player Name, Current Status, Reason, Previous Status, Previous Reason]
![2](https://user-images.githubusercontent.com/70581662/94700177-dc617a00-0343-11eb-930f-441bf55b97ba.png)<br />


- 2019/11/15 - 2019/11/19 format:
[Game Date, Game Time, Matchup, Team, Player Name, Reason, Current Status, Previous Status]
![3](https://user-images.githubusercontent.com/70581662/94700184-de2b3d80-0343-11eb-82d5-0648546caaf8.png)<br />

- 2019/11/20 - 2019/12/16 format:
[Game Date, Game Time, Matchup, Team, Player Name, Current Status, Reason, Previous Status]
![4](https://user-images.githubusercontent.com/70581662/94700194-dff50100-0343-11eb-9675-e91a93e5a448.png)<br />

- 2019/12/18 - Today format:
[Game Date, Game Time, Matchup, Team, Player Name, Current Status, Reason]
![5](https://user-images.githubusercontent.com/70581662/94700208-e1bec480-0343-11eb-9113-078d5725c992.png)<br />

2. Because we are converting from a pdf file to a pandas dataframe, The conversion is not done properly and not everything is in the right place. We fixed the problem by shift rows to the right according to the right pattern. We also filled in NA values. 
At the end of the dataframe looks like this:
![full](https://user-images.githubusercontent.com/70581662/94701872-cfde2100-0345-11eb-890f-ef5bc2ce1c27.png)<br />


Now we only have left to clean the dataset.


