"""
Small server to deliver Smash Hit adverisements

Copyright (C) 2022 Knot126, MIT Licence
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from random import randint

SERVER_PORT = 8000

def loadJson(path):
	"""
	Load a json file
	"""
	
	content = ""
	
	with open(path, "r") as f:
		content = json.load(f)
	
	return content

def loadFileBytes(path):
	"""
	Load a file's bytes.
	"""
	
	f = open(path, "rb")
	content = f.read()
	f.close()
	
	return content

class AdServer(BaseHTTPRequestHandler):
	"""
	The request handler for an ad server
	"""
	
	def log_request(self, code = '-', size = '-'):
		pass
	
	def do_GET(self):
		# Log the request
		print(self.client_address[0], self.client_address[1], self.command, self.path)
		
		# Open ad info file
		# We use a file to prevent restarting for config changes
		ad_info = loadJson("adserver_config.json")
		
		# Set data
		data = b""
		
		# Path parts
		url = self.path.split("?")
		path = url[0]
		params = {}
		
		# Parse parameters
		if (len(url) >= 2):
			url[1] = url[1].split("&")
			
			for param in url[1]:
				p = param.split("=")
				key = p[0]
				value = p[1]
				params[key] = value
		
		# Load attributes of the device
		device_platform = params.get("platform", "unknown")
		device_version = params.get("version", "unknown")
		device_date = params.get("date", "unknown")
		device_old_revision = params.get("rev", "unknown")
		
		# Load attributes of the ads
		revision = str(int(params.get("rev", 0)) + 1) if ad_info.get("forceupdate", False) else ad_info.get("revision", 1)
		showfront = ad_info.get("showfront", 1)
		onlyfree = ad_info.get("onlyfree", 0)
		sale = ad_info.get("sale", 0)
		folder = ad_info.get("folder", "default")
		
		# For ads xml
		if (path.endswith("ads.php") or path.endswith("ads")):
			data = bytes(f"""<ads revision="{revision}" showfront="{showfront}" onlyfree="{onlyfree}" sale="{sale}" folder="{folder}"/>""", "utf-8")
			
			# Print that the device gets ads
			print(f"""\x1b[38;2;{randint(64,256)};{randint(64,256)};{randint(64,256)}mDevice at {self.client_address[0]}:{self.client_address[1]} gets ads:\n\tPlatform: {device_platform}\n\tVersion: {device_version}\n\tDate: {device_date}\n\tOld revision: {device_old_revision}\n\tNew revision: {revision}\n\tFolder: {folder}\n\x1b[0m""")
		
		# As a security measure, we don't trust what the user has sent
		# so we never use it and instead just go by what the URL ends with
		elif (path.endswith("ads.xml")):
			data = loadFileBytes(folder + "/ads.xml")
		
		elif (path.endswith("ads.png")):
			data = loadFileBytes(folder + "/ads.png")
		
		# If the file is not found or known then 404
		else:
			self.send_response(404)
			self.end_headers()
			return
		
		# Send response
		self.send_response(200)
		self.send_header("Content-Length", str(len(data)))
		self.send_header("Content-Type", "text/xml")
		self.end_headers()
		self.wfile.write(data)

def main():
	server = HTTPServer(("0.0.0.0", SERVER_PORT), AdServer)
	
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	
	server.server_close()

if __name__ == "__main__":
	main()
