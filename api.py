import requests
import json

api_key = "yn6rumz2jddsrjrju6esfppz"

def getID(url):
    ret = ""
    for i in reversed(url):
        if i.isdigit():
            ret = i + ret
    print "--------JUST RAN GETID. ID IS: "
    print ret + "-------------"
    return ret

''' it works
print "running getID..."
print getID(p_url)
'''


p_url="https://www.walmart.com/ip/Imaginext-DC-Super-Friends-RC-Transforming-Batbot/49962535"
url= "http://api.walmartlabs.com/v1/items?apiKey=" + api_key+ "&format=json&itemId=" + getID(p_url)



def api_info(id):
    print "RUNNING API INFO...."
    response = requests.get(url)
    response = json.loads(response.content.decode())
    price = response['items'][0]["salePrice"]
    SD = response['items'][0]["shortDescription"].replace("&quote;", '""')
    name = response['items'][0]["name"]
    img = response['items'][0]["mediumImage"]
    ret = [name, price, SD, img]
    return ret
