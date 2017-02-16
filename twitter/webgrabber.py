""" 
	Grab data from a http server with a userspecified agent and referrer
	Nicholas <nicholas@purged.info>
	
	TODO:
		[X] Spoofable user agent and referrer
		[X] Redirect support
		[X] GZIP support
		[X] Cookie handling
		[X] Basic Authentication support
		[X] Proxy support
		[X] SSL support
		[X] Better error handling
		[ ] Connection keep alive support
		[ ] Pipelining support
		[ ] Digest Authentication support
	
	Example usage:
		grabber = webgrab(authentication="user:password")
		grabber.grab('https://secure.purged.info/')
		for key,val in grabber.result.items():
			print "%-15s: %s" % (key, val)
			
		grabber.setCookie("blaat")
		grabber.grab('url')
		print grabber['cookie']			(cookie received from site)
		print grabber['data']			(html output)
		print grabber['date']			(last modified data)
		print grabber['etag']			(etag)
		print grabber['status']			(apache status code)
	
"""


import httplib, urllib, urllib2, urlparse, gzip, base64
from StringIO import StringIO

# Set request type to http/1.1
httplib.HTTP._http_vsn_str = 'HTTP/1.1'


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):    
    def http_error_301(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)              
        result.status = code                                
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)              
        result.status = code                                
        return result                                       

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):   
	def http_error_default(self, req, fp, code, msg, headers):
		result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)       
		result.status = code                       
		return result                   

class webgrab(object):
	def __init__(self, **args):
		self.result = {}
		self.header = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"}
		self.proxy = {}
		for k,v in args.items():
			object = 'set'+k
			function = getattr(self, object)
			function(v)
			
	def __getitem__(self, key):
		return self.result[key]
		
	def setAgent(self, agent):
		self.header["User-Agent"] = agent
		
	def setReferrer(self, referrer):
		self.header["Referer"] = referrer
	
	def setEtag(self, etag):
		self.header["If-None-Match"] = etag
		
	def setDate(self, date):
		self.header["If-Modified-Since"] = date
	
	def setCookie(self, cookie):
		self.header["Cookie"] = cookie
		
	def setAuthentication(self, username, password):
		base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
		self.header["Authorization"] = "Basic %s" % base64string
	
	def setAuthentication(self, userpass):
		''' UserPass in the form of username:password''' 
		base64string = base64.encodestring('%s' % userpass)[:-1]
		self.header["Authorization"] = "Basic %s" % base64string
		
	def setProxy(self, host, proxytype='http'):
		self.proxy["host"] = host
		self.proxy["proxytype"] = proxytype


	def grab(self, source, method='GET', arguments=None):  
		'''Grab data and metadata from a URL, file, stream, or string
		'''
		# First fix the request type...
		params = arguments and urllib.urlencode(arguments) or None
		if method == 'POST':
			request = urllib2.Request(source, params)
		elif arguments == None:
			request = urllib2.Request(source)
		else:
			request = urllib2.Request("%s?%s" % (source, params))
		# set up request header
		request.add_header('Accept-encoding', 'gzip')
		for k,v in self.header.items():
			request.add_header(k, v)
		if self.proxy: request.set_proxy(self.proxy['host'], self.proxy['proxytype'])
		# actual request
		f = urllib2.build_opener(SmartRedirectHandler(), DefaultErrorHandler()).open(request)
		#f = urllib2.urlopen(request)
		# parse result
		self.result['data'] = f.read()
		self.result['etag'] = f.headers.get('ETag')
		self.result['lastmodified'] = f.headers.get('Last-Modified')
		self.result['url'] = f.url
		self.result['status'] = 200
		if hasattr(f, 'status'): self.result['status'] = f.status
		if f.headers.get('Set-Cookie'): 
			self.result['cookie'] = f.headers['Set-Cookie']
		if f.headers.get('content-encoding', '') == 'gzip':
			self.result['data'] = gzip.GzipFile(fileobj=StringIO(self.result['data'])).read()
		f.close()
		

if __name__ == "__main__":
    wg = webgrab()
    wg.grab("http://volkskrant.nl/rss/laatstenieuws.rss")
    print wg['data']
#EOF
