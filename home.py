import streamlit as st
import streamlit.components.v1 as components
import requests
import urllib
import json
from IPython.core.display import display, HTML, JSON
from types import SimpleNamespace
import logging
import plotly.graph_objects as go
import webbrowser
import datetime

############ page config
st.set_page_config(
    page_title="FinVerse - Team Cutting Edge - START Hack 2023",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/nathanyaqueby/start-hack-2023',
        'Report a bug': "https://github.com/nathanyaqueby/start-hack-2023",
        'About': """
        In today's world, financial literacy is more important than ever. Unfortunately, many people lack access to the resources and knowledge needed to manage their finances effectively. This is where FinVerse comes in.
        FinVerse is designed to make financial literacy accessible to everyone. By using virtual reality technology, we have created a platform that is engaging, interactive, and easy to use. Our application is specifically designed to help increase inclusivity of financial literacy by making it accessible to the common people.
        With FinVerse, users can explore different financial concepts and strategies in a way that is both fun and informative. Our application allows users to simulate real-life financial scenarios, experiment with different investment strategies, and learn about the basics of budgeting and saving.
        Our team has worked tirelessly to ensure that FinVerse is user-friendly, visually appealing, and most importantly, effective. By combining the power of virtual reality with expert financial advice, we believe that FinVerse has the potential to revolutionize financial literacy education.
        We are excited to participate in this hackathon and look forward to showcasing the power of FinVerse.
        """
    }
)

st.markdown("## Virtual Reality-Based Financial Literacy Web Application")
st.markdown("Welcome to *_FinVerse_*! "
            "Dive into the VR world by running the generator on the left sidebar and use keypads to walk through your financial universe."
            " Read more about our project on [GitHub](https://github.com/nathanyaqueby/start-hack-2023). Enjoy!")

##############################################

logger = logging.getLogger()
logger.setLevel(logging.INFO) # CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

display(HTML("<style>.container { width:90% !important; }</style>"))

class FinancialDataAPI:
    def __init__(self):
        self.url = 'https://web.api.six-group.com/api/findata'
        
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "api-version": "2022-06-01"
        }
        self.session = requests.session()
        certificate_path = 'ch52991-hackathon1'
        self.session.cert = (f'{certificate_path}/signed-certificate.pem', f'{certificate_path}/private-key.pem')
    
    def http_request(self, end_point:str, query_string:dict) -> str:
        # Make an HTTP request and send the raw response
        try:
            http_request = f"{self.url}{end_point}?{urllib.parse.urlencode(query_string)}"
            
            r = self.session.get(http_request, headers=self.headers) #, verify='./six-certificate/certificate.pem')
            if str(r.status_code)[0] != "2":
                logging.debug(f"HTTP{r.status_code}: {r.content}")
            else:
                logging.debug(f"HTTP{r.status_code}: {json.dumps(json.loads(r.content), indent=2)}")
                
            return r
        except requests.exceptions.SSLError as err:
            logging.error(f"Error - {http_request}:\r\n{err}")
            raise(Exception(str(err)))

    def http_request_with_scheme_id(self, end_point:str, scheme:str, ids:list) -> str:
        query_string = query_string = { 
            'scheme': scheme,
            'ids': ",".join(ids)
        }
        return self.http_request(end_point, query_string)        
            
    def _convert_response_to_object(self, http_response):
        if str(http_response.status_code)[0] == "2":
            obj = json.loads(http_response.content, object_hook=lambda d: SimpleNamespace(**d))
            return obj
        return None
            
    def text_search(self, query:str) -> object:
        end_point = "/v1/searchInstruments"
        #end_point = "/search/v1/"
        query_string = { 'query': query }
        resp = self.http_request(end_point, query_string)
        
        return self._convert_response_to_object(resp)
    
    def instrument_summary(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/referenceData/instrumentSummary"
        #end_point = "/v1/summary/instruments"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_symbology(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/referenceData/instrumentSymbology"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_BASELIII_HQLA_EU(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/_regulatoryData/baseliiihqlaEU"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_BASELIII_HQLA_CH(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/_regulatoryData/baseliiihqlaCH"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_SFDR(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/esg/SFDRInvestee"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_TAXONOMY(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/esg/EUTaxonomyInvestee"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)

    def instrument_EUESGMANUFACTURER(self, scheme:str, instruments: list):
        end_point = "/v1/instruments/esg/EUESGManufacturer"
        resp = self.http_request_with_scheme_id(end_point, scheme, instruments)
        return self._convert_response_to_object(resp)
    
    def institution_summary(self, scheme:str, institutions: list):
        end_point = "/v1/institutions/referenceData/institutionSummary"
        resp = self.http_request_with_scheme_id(end_point, scheme, institutions)
        return self._convert_response_to_object(resp)

    def institution_symbology(self, scheme:str, institutions: list):
        end_point = "/v1/institutions/referenceData/institutionSymbology"
        resp = self.http_request_with_scheme_id(end_point, scheme, institutions)
        return self._convert_response_to_object(resp)
    
    def institution_SFDR(self, scheme:str, institutions: list):
        end_point = "/v1/institutions/esg/SFDRInvestee"
        resp = self.http_request_with_scheme_id(end_point, scheme, institutions)
        return self._convert_response_to_object(resp)

    def institution_TAXONOMY(self, scheme:str, institutions: list):
        end_point = "/v1/institutions/esg/EUTaxonomyInvestee"
        resp = self.http_request_with_scheme_id(end_point, scheme, institutions)
        return self._convert_response_to_object(resp)

    def market_summary(self, scheme:str, markets: list):
        end_point = "/v1/markets/referenceData/marketSummary"
        resp = self.http_request_with_scheme_id(end_point, scheme, markets)
        return self._convert_response_to_object(resp)
    
    def market_symboloy(self, scheme:str, markets: list):
        end_point = "/v1/markets/referenceData/marketSymbology"
        resp = self.http_request_with_scheme_id(end_point, scheme, markets)
        return self._convert_response_to_object(resp)

    def listing_EoDTimeseries(self, scheme:str, listings: list, from_date:str, to_date:str = ''):
        end_point = "/v1/listings/marketData/eodTimeseries"
        query_string = query_string = { 
            'scheme': scheme,
            'ids': ",".join(listings),
            'from': from_date,
            'to': to_date
        }
        resp = self.http_request(end_point, query_string)    
        return self._convert_response_to_object(resp)
    
findata = FinancialDataAPI()

######################### print_object_attributes #########################

def print_object_attributes_text(valors, bcs, obj:object, tab_level:int=0, min_attr_length:int=30):
    if obj is None: return
    space_sep = "  "
    space = space_sep*tab_level
    
    if type(obj) == list:
        for o in obj:
            if type(o) == object or type(o) == SimpleNamespace:
                print_object_attributes_text(valors, bcs, o, tab_level+1, min_attr_length)
    else:
        for attr, value in obj.__dict__.items():
            if type(value) == object or type(value) == SimpleNamespace or type(value) == list:
                # st.markdown(f"{space}{attr}")

                adjusted_min_attr_length = min_attr_length - (len(space_sep)*(tab_level+1))
                if adjusted_min_attr_length < 0: adjusted_min_attr_length = 0
                print_object_attributes_text(valors, bcs, value, tab_level+1, adjusted_min_attr_length)
            else:
                if attr == "valor":
                    valors.append(value)
                if attr == "bc":
                    bcs.append(value)
                # st.markdown(f"{space}{attr:<{min_attr_length}}: {value}")    

    # if length of valors and bcs is greater than 0, return them
    if len(valors) > 0 and len(bcs) > 0:
        return valors, bcs 

######################### print_object_attributes (time series) ######################### 

def print_object_attributes_timeseries(highs, lows, obj:object, tab_level:int=0, min_attr_length:int=30):
    if obj is None: return
    space_sep = "  "
    space = space_sep*tab_level
    
    if type(obj) == list:
        for o in obj:
            if type(o) == object or type(o) == SimpleNamespace:
                print_object_attributes_timeseries(highs, lows, o, tab_level+1, min_attr_length)
                # print()
            # else:
            #     print(f"{space}{o:<{min_attr_length}}")
    else:
        for attr, value in obj.__dict__.items():
            if type(value) == object or type(value) == SimpleNamespace or type(value) == list:
                # print(f"{space}{attr}")

                adjusted_min_attr_length = min_attr_length - (len(space_sep)*(tab_level+1))
                if adjusted_min_attr_length < 0: adjusted_min_attr_length = 0
                print_object_attributes_timeseries(highs, lows, value, tab_level+1, adjusted_min_attr_length)
            else:
                if attr == "high":
                    highs.append(value)
                if attr == "low":
                    lows.append(value) 
    
    # if length of dates and volumes is greater than 0, return them
    return highs, lows

######################### DASHBOARD #########################    

# add image to the sidebar
# st.sidebar.image("imgs/SIX_CUTTINGEDGE.png", use_column_width=True)

with st.sidebar.form(key='Form1'):
    # create a sidebar with a submit button
    st.title("📈 3D Stock Dashboard")

    options = st.multiselect(
    'Which companies would you like to see?',
    ['DKSH', 'Tesla', 'Amazon', 'Nike', 'Apple', 'Google', 'Samsung', 'Meta', 'Boeing', 'SIX'],
    default=['Apple', 'Google', 'Samsung', 'Meta', 'Boeing', 'SIX']
    )

    # add an input field for the user to enter the starting date
    start_date = st.date_input("Enter a start date", datetime.date(2022, 7, 1), max_value=datetime.date(2023, 3, 21))

    # save the date in the format YYYY-MM-DD
    start_date = start_date.strftime("%Y-%m-%d")

    # add an input field for the user to enter the starting date
    end_date = st.date_input("Enter an end date", datetime.date(2023, 3, 22), max_value=datetime.date(2023, 3, 22))

    # save the date in the format YYYY-MM-DD
    end_date = end_date.strftime("%Y-%m-%d")

    # add a submit button to the sidebar
    submit_button = st.form_submit_button(label='Generate VR world', use_container_width=True, type="primary")

    # add tips to the sidebar
    st.markdown("""<b>💡 Tips:</b><br>
                Use VR glasses to experience the world in 3D!
                Try our [randomly generated world](https://caramel-lofty-newsprint.glitch.me/).
                """, unsafe_allow_html=True)

# st.sidebar.image("imgs/START_Logo.png", use_column_width=True)

if submit_button:

    with st.spinner('Loading...'):

        video_file = open('trailer.mp4', 'rb')
        video_bytes = video_file.read()

        components.html('<iframe src="https://caramel-lofty-newsprint.glitch.me/" style="position: absolute; height: 100%; width: 100%; border: none"></iframe>', height=390)

        diffs = []

        # for each company in the list, get the company information
        for company in options:

            valors = []
            bcs = []
            highs = []
            lows = []

            count = 0

            # while highs and lows are empty, get the company information
            while len(highs) == 0 and len(lows) == 0:

                try:
                    obj = findata.text_search(company)
                    valors, bcs = print_object_attributes_text(valors, bcs, obj)

                    # get the EoD timeseries for the company
                    obj = findata.listing_EoDTimeseries("VALOR_BC", [f"{valors[count]}_{bcs[count]}"], start_date, end_date)
                    highs, lows = print_object_attributes_timeseries(highs, lows, obj)
                
                except:
                    continue
                    # st.write("Error", company, count)

                count += 1

        with st.expander("For the stock market experts"):
            # plot the differences in a single graph with multiple lines (one for each company)
            fig = go.Figure()
            for i in range(len(diffs)):
                fig.add_trace(go.Scatter(x=[i for i in range(len(diffs[i]))], y=diffs[i], name=options[i]))
            fig.update_layout(title="Differences between highs and lows", xaxis_title="Days", yaxis_title="Differences")
            st.plotly_chart(fig, use_container_width=True)