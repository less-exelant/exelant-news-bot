# Define RSS feeds
rss_feeds = {
    "Executive Orders": [
        "https://www.federalregister.gov/api/v1/documents.rss?"
        "conditions%5Bcorrection%5D=0&"
        "conditions%5Bpresident%5D=&"
        "conditions%5Bpresidential_document_type%5D=executive_order&"
        "conditions%5Bsigning_date%5D%5Byear%5D=&"
        "conditions%5Btype%5D%5B%5D=PRESDOCU",
    ],
    "Federal Laws": [
        "https://www.govinfo.gov/rss/plaw.xml",
    ],
    "District and Apellate Courts" : [
        "https://www.govinfo.gov/rss/uscourts-flsd.xml",
        "https://www.govinfo.gov/rss/uscourts-flmd.xml",
        "https://www.govinfo.gov/rss/uscourts-flnd.xml",
        "https://www.govinfo.gov/rss/uscourts-ca11.xml",
    ],
    "Florida Law": [
        "https://www.flsenate.gov/Tracker/RSS/Video_Latest25",
        "https://www.floridalawreview.com/feed",
        "https://thefloridachannel.org/videos/feed/",

    ],
    "Urban Planning and Land Use": [
        "https://www.planetizen.com/rss.xml",
        "https://www.esri.com/about/newsroom/rss/",
        "https://www.smartcitiesdive.com/feeds/news/",
        "https://news.mit.edu/rss/topic/urban-studies",
    ],
    "Housing Policy and Real Estate": [
        "https://hfront.org/feed/",
        "https://www.housingwire.com/rss/",
        "https://www.zillow.com/research/feed/",
        "https://rss.nytimes.com/services/xml/rss/nyt/RealEstate.xml",
        "https://feeds.content.dowjones.io/public/rss/latestnewsrealestate",
        "https://eyeonhousing.org/category/macroeconomics/feed/",
        "https://news.mit.edu/rss/topic/real-estate",
    ],
    "Affordable Housing": [
        "https://shelterforce.org/feed/",
        "https://furmancenter.org/thestoop/feed",
        "https://affordablehousingonline.com/blog/feed/",
        "https://affordablehousingaction.org/feed/",
        "https://www.multifamilyinsiders.com/categories/affordable-housing?format=feed&type=rss",
        "https://www.reit.com/news/articles/rss.xml",
    ],
    "Education Policy": [
        "https://edsource.org/feed/atom",
        "https://feeds.npr.org/1019/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Education.xml",
    ],
    "Infrastructure and Transportation": [
        "https://edsource.org/feed/atom",
        "https://t4america.org/feed/",
        "https://usa.streetsblog.org/feed/",
    ],
    "Artificial Intelligence": [
        "https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml",
        "https://bair.berkeley.edu/blog/feed.xml",
        "https://ai.stanford.edu/blog/feed.xml",
        "https://openai.com/news/rss.xml",
    ]
}