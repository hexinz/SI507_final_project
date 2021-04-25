# SI507_final_project
Scrape and Crawl project for Google Play Apps from https://play.google.com/store/apps/.
## Instructions:
- Clone the repository
- Run the command: `python3 interact_plotly.py` or `python interact_plotly.py`
- Follow the printed messages to explore the data. 
  - At the very beginning, a list of app categories with id in front of each category is printed. 
  - Then, you could choose to visualize plots or make detail search of a certain category. 
  - If you choose the former one, you could explore different plots like follows:
  <img width="1592" alt="boxplot" src="https://user-images.githubusercontent.com/78745684/115985980-cc133400-a5e0-11eb-83f6-9cd62d90ddfb.png">
  <img width="1626" alt="barplot" src="https://user-images.githubusercontent.com/78745684/115986120-66737780-a5e1-11eb-9858-119113b50b50.png">
  <img width="1607" alt="histplot-self-defined" src="https://user-images.githubusercontent.com/78745684/115986126-683d3b00-a5e1-11eb-9516-5972ceba7b03.png">
  <img width="1601" alt="histplot" src="https://user-images.githubusercontent.com/78745684/115986127-6a9f9500-a5e1-11eb-89d1-30d156296fe1.png">
  - If you choose the latter one, you will see a list of apps with developers and stars. Choose the app id will give you the downloading url for each app. 
  - Finally, type `back` to return to the first choice interface; type `exit` to end the program. 
 
## Required Python packages:
- requests
- bs4
- plotly
- pandas
- numpy
