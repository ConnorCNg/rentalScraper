# Zillow Property Data Web Scraper

### Requirements
Install them from requirements.txt:
```pip install -r requirements.txt```

### API Key
If the amount of monthly API calls limit has been reached, follow the steps below to get and use your own API key.
1. Log in or Register for the Scrapeak Dashboard. https://app.scrapeak.com/dashboard/settings
2. Sign up for any plan, including the free starter plan.
3. Go to the Scrapers page and register for the Zillow scraper
4. Go to the settings page and copy your API key.
5. Open the .env file and replace the key their with your own key. 

### Local Deployment
Enter folder with files and run:
```flask run```

#### Video Demo  
https://www.youtube.com/watch?v=ICbOa06vFQo

### Description
Using Flask to create an interactive webpage I designed a simple webpage which contained a hyperlink to the Zillow property search page. A user can use the already established functionality of Zillow to identify the properties they want to aggregate data on. The user would then copy the resulting URL of the property search, go back to my wepage, then paste it and click 'Submit'. The resulting page shows a table where each row is a property returned by the search and each column has relevant comparison information like current price and square footage. Then tables for each property are displayed below that show the price history for the property.

### Motivation
At the time I was helping my parents get a rental property ready for another tenant as the previous one had moved out after living there a few years. One of the key questions was: "What should we set the rental price to?". My parents walked me through their methods:

1. Go to Zillow
2. Check the rental properties currently for sale in the neighborhood (ex. in the same zipcode)
3. Review how the rentals looked compared to ours
4. Review the price history of the rentals to see if they either realized they could rent their property out for more money due to many offers, or weren't getting many offers with their current rental price.

This project set out to emulate and automate parts of my parents' workflow.

### Research
I started by looking for available APIs that Zillow offers. Upon review, the APIs offered were not granular enough. They did not provide price history and did not allow searching by zipcode. I reviewed other websites like Redfin, however, Zillow is dominant in the rental space and has the most complete data as most renters list on Zillow.

I then tried to code my own web scraper using BeautifulSoup. However, I received a 403 Forbidden error. Zillow has more recently been restricting who can access their data.

I found Scrapeak which has partnertships with companies and offers web scraping APIs. Reading through their [Zillow web scraping API documentation](https://docs.scrapeak.com/zillow-scraper/endpoints/propertydetails) I determined that their 'property' API contained data 'Price History' data, however, an issue was that the 'property' API only returns data for one 'zpid'(Zillow's unique ID they give to each property). I used another of their APIs 'listing' which takes the URL of a Zillow property search and returns the properties found by that search. The reponse from 'listing' contains the zpid for each property among other data. I could search for properties currently for rent based off of zipcode and feed that list of zpids to an API that gets the metadata I want.

### Design considerations
I did not create my own Zillow search feature since I believed it would be redundant as Zillow already has a very easily accessible one. This program is meant to be run only a few times so I did not think saving 2 extra clicks were worth designing a search page over.

I included links to each webpage so the user can easily jump to the property page on Zillow to view the photos or other information. It does look like the 'listing' API contains image URLs so it may be worth pulling those into the webpage. Hoewever, again since this is only meant to be ran once or twice for a property clicking the hyperlink to go to the property webpage and scrolling through the pictures on Zillow only introduces two extra clicks.

I would have liked to see results for properties that have been rented in the past but are not currently for rent. However, that is not possible through the web scraping API used since it requires a Zillow search URL and Zillow only allows searching for properties 'for rent', 'for sale', and 'sold'. I considered scraping all of the 'Sold' properties, however, that runs into the limitation where only 100 queries are allowed per month. Returning all 'Sold' properties generally returns too many results. Discussed a bit more in the 'Limitations' section below.

### Limitations
The Scrapeak APIs only allot 100 API calls per month. (# Scrapeak API calls) = (# properties returned by property search) + 1. My code calls the the 'listing' API once to get a list of properties, then calls the 'property' API once on each zpid returned by the 'listing' API. This is a constraint that only allows a few calls per month. To get around this you can register on Scrapeak with a different URL but that's contstrained by how many email addresses you have or are willing to make. You can also pay Scrapeak for for queries but that is not necessary for the original intended purpose.
