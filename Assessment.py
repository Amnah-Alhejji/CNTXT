from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
import pandas as pd
from datetime import datetime,timedelta

# Authenticate with the Cognite Python SDK #


base_url = "https://api.cognitedata.com"
tenant_id = "48d5043c-cf70-4c49-881c-c638f5796997"

creds = OAuthClientCredentials(
    token_url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
    client_id="1b90ede3-271e-401b-81a0-a4d52bea3273",
    client_secret="svQ8Q~FONdaBp~CPHoo3SE_~Wibi7ReXebII2a5X",
    scopes=[f"{base_url}/.default"]
)

cnf = ClientConfig(
    client_name="Amnah",
    project="publicdata",
    credentials=creds,
    base_url=base_url
)
# Configuration Setup :
client = CogniteClient(cnf)



def solve_assessment():
    # Available projects:
    projects_available = client.iam.token.inspect()
    print(f"The available projects are :{projects_available}")
    # Available assets in the project:
    available_assets = client.assets.list()
    print(f"Available_assets:{available_assets}")

    # Total number of assets:
    asset_count = client.assets.aggregate()
    print(f"Total number of assets:{asset_count[0].count}")


    # Search for specific asset:
    asset_name = "23-TT-92533"
    required_asset = client.assets.list(name=asset_name)
    print(f"The required asset is :{required_asset}")


    # External ID for the asset:
    external_id = required_asset[0].external_id 
    print(f"The external id is :{external_id}")
    

    # Time series belong to the asset:
    number_of_time_series = client.time_series.list(external_id)
    print(f"The length of time series  :{len(number_of_time_series)}")
        
        
    # Events belong to the asset:
    events = client.events.aggregate()
    print(f"The number of the events associated with asset '{asset_name}'= {events[0].count}")
        
    # Latest data point for the given id:
    latest_dataoint = client.time_series.data.retrieve_latest(external_id="pi:160884")
    print(f"latest_dataoint for the given id :{latest_dataoint}")
 


 # The daily average of time series with the given external id over the last 4 weeks: --NOT WORKING :(--
def daily_avg_time_series():
    weeks_ago_time = int((datetime.now() - timedelta(weeks=4)).timestamp()*1000)
    current_time = int(datetime.now().timestamp()*1000)
    datapoints = client.time_series.data.retrieve(external_id="pi:160884",start=weeks_ago_time,end=current_time)
    df = pd.DataFrame(datapoints)
    # df.columns
    df['date time'] = pd.to_datetime(df['timestamp'],unit='ms') #  convert timestamp to date time
    # Calculate the daily Avg. 
    daily_avg = df.set_index('date time').resample('D').mean()
    print(f"the daily average of time series :{len(daily_avg)}")


solve_assessment()
# daily_avg_time_series()
    