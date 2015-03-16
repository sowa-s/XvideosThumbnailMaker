from flask import Flask
from flask.ext import restful
import requests
from bs4 import BeautifulSoup
import re
import opengraph

app = Flask(__name__)
api = restful.Api(app)

class createThumb(restful.Resource):
	def get(self,url):
		pattern = re.compile(r'xvideos.com')
		matchObj = pattern.search(url)
		if matchObj is None:
			print(url)
			return self.otherThumb(url)
		else:
			return self.xvideosThumb(url)

	def xvideosThumb(self,url):
		try:
			r = requests.get(url)
			soup = BeautifulSoup(r.text.encode(r.encoding))
			embed = soup.find("embed").get("flashvars")
			pattern = re.compile(r'url_bigthumb=http.*?(\.gif|\.png|\.jpg|\.jpeg$|\.bmp)')
			matchObj = pattern.search(embed)
			thumb = matchObj.group(0).replace('url_bigthumb=','')
		except:
			return {'status':'failed'}
		return {'status':'success','img': thumb}

	def otherThumb(self,url):
		try:
			site = opengraph.OpenGraph(url=url)
		except:
			return {'status':'failed'}
		if site.is_valid():
			image = site.image
		else:
			return {'status':'failed'}
		return {'status':'success','img':image}

api.add_resource(createThumb, '/<path:url>',methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)

