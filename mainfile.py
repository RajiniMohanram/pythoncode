
from scrap import scrape
from opinion_mining_training_module import sentiment_analysis
reviews=[]
for n in range(1,6):
    m=scrape(n)
    for rv in m:
        reviews.append(rv)
	
sentiment_analysis(reviews)
