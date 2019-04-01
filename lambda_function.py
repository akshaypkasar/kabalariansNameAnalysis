import mechanize
from bs4 import BeautifulSoup

def fetch_name_analysis(name, gender):

    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Firefox')]

    br.open( "https://www.kabalarians.com" )
    br.select_form("mainForm")
    br['FirstName'] = name
    if gender == 'M':
        br['gender'] = ['M']
    else:
        br['gender'] = ['F']

    response = br.submit()

    soup = BeautifulSoup(response.read(),'html.parser')
    
    return soup.find(id="headerOL").find_all('li')[0].text.replace('\xa0','')


def lambda_handler(event, context):

	if ('name' in event) & ('gender' in event):
		return {
			'statusCode': 200,
			'body': fetch_name_analysis(event['name'], event['gender'])
		}
	else:
		return {
            'statusCode': 400,
            'body': "Parameters Missing"
        }