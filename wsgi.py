#def application(env, start_responce):
#	start_response('200OK', [('Content-Type', 'text/html')])
#	return ['Hello world.']
	
def application(environ, start_response):
	post_env = environ.copy()
	data = "Hello!\nGET data:\n" + post_env['QUERY_STRING'] + "\nPOST data:";
	post_env['QUERY_STRING'] = ''
	post = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', '0')))
	data += post
	data += '\n'
	start_response("200 OK", [
		("Content-Type", "text/plain"),
		("Content-Length", str(len(data))),
		])
	return iter([data])