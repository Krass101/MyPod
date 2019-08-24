from gtts import gTTS
from datetime import date
from urllib.request import urlopen
from bs4 import BeautifulSoup
import yagmail

#Get date to use inside the podcast narrative and for the naming of the file
today = date.today()
spoken_date = today.strftime("%A %B %d")

#We create a blob variable to store the narrative of the podcast. Later we append more information to it before it gets converted to audio.
blob = "Here is your podcast for " +spoken_date+ ". First we'll look at the weather for the next three days and then a summary of top news. "
language = 'en'

#First function is to get the weather RSS feed.
def weather(xml_weather_url):

    #Set up the parser
    parse_xml_url = urlopen(xml_weather_url)
    xml_page = parse_xml_url.read()
    parse_xml_url.close()
    soup_page = BeautifulSoup(xml_page, "xml")
    weather_list = soup_page.findAll("item")

    #Declare the global variable so we can add to it inside the function
    global blob

    #For each item in the RSS we get the title since that is where the temperature data is for the RSS feed in the example
    for getfeed in weather_list:
        blob = blob + getfeed.title.text


#Second function is to get the news feed
def news(xml_news_url):

    #Set up the parser
    parse_xml_url = urlopen(xml_news_url)
    xml_page = parse_xml_url.read()
    parse_xml_url.close()
    soup_page = BeautifulSoup(xml_page, "xml")
    news_list = soup_page.findAll("item")

    #Declare the global variable so we can append to it
    global blob

    #Append a short introduction for the news section
    blob = blob + "And now let's take a look at the news. "

    #For each item in the RSS we get the title since that is where the temperature data is for the RSS feed in the example
    for getfeed in news_list:

        #Append each RSS item and a 'next story' phrase to make it clear when a new story starts
        blob = blob + getfeed.description.text + '  NEXT STORY.  '

#Set the URL for the weather RSS
WEATHER_URL = "https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/2643743"
weather(WEATHER_URL)

#Set the URL for the news RSS
NEWS_URL = "http://feeds.bbci.co.uk/news/video_and_audio/news_front_page/rss.xml?edition=uk"
news(NEWS_URL)

#Create object based on blob variable and save it as mp3
myobj = gTTS(text=blob, lang=language, slow=False)
myobj.save("myPod"+str(today)+".mp3")

#Write contects of message which will email the recording
contents = [
    "Hi, here is today's podcast:",
    {'/path to file '+str(today)+'.mp3': 'My Pod'}
]

#Use Yagmail to connect to your email account. Add your own login and password. You can also use Auth2 with Yagmail
yagmail.register('loginID', 'pass')
yag = yagmail.SMTP('loginID', 'pass')

#Send the email
yag.send(to='email address', contents=contents, subject='My Podcast')



