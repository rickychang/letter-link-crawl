import mechanize
import urlnorm
import urllib2
import re
import sys

VALID_CHARS = '^([-A-Za-z0-9+&@#/%=~_()| ]*)$'

def validate_search_term(search_term):
	return bool(re.search(VALID_CHARS, search_term))

def print_url(url, letter_index, max_index):
	if (not url or letter_index == -1):
		print ''
	else:
		padding = ' ' * (max_index - letter_index)
		print '%s%s %s %s' % (padding, url[0:letter_index], url[letter_index], url[letter_index+1:])

def find_matching_links(br, target_word, result, visited):
	if (not target_word):
		return result
	else:
		current_URL = br.geturl()
		current_letter = target_word[0]
		if (current_letter.isspace()):
			return find_matching_links(br, target_word[1:], result + [('', -1, ' ')], visited)
		else:
			matches = [(link, link.absolute_url[7:].find(current_letter.lower()) + 7) for link in br.links() if link.absolute_url[7:].find(current_letter.lower())!= -1]
			for m in matches:
				try:
					# if (urlnorm.norm(m[0].absolute_url) not in visited):
					if (urlnorm.norm(m[0].absolute_url) not in visited):
						visited.add(urlnorm.norm(m[0].absolute_url))
						print m[0].absolute_url
						br.follow_link(m[0])
						child_result = find_matching_links(br, target_word[1:], result + [(m[0].absolute_url, m[1], current_letter)], visited)
						if (child_result):
							return child_result
						else:
							br.back()
				except Exception as e:
					pass
	print "backtracking"
	return []




if (len(sys.argv) < 3 ):
	print "usage: ll-print.py <url> <search term>"
	print "example: ll-print.py http://www.hunch.com 'hunch team'"
	exit(0)
root_URL = sys.argv[1]
search_term = sys.argv[2]
if (not validate_search_term(search_term)):
	print "Invalid search term.  Please only use valid url characters and spaces."
	exit(1)

first_letter = search_term[0]
first_letter_match = root_URL.find(first_letter.lower())
if (first_letter_match != -1):
	try:
		br = mechanize.Browser()
		result = [(root_URL, first_letter_match, first_letter)]
		visited = set([urlnorm.norm(root_URL)])
		br.open(root_URL)
		print root_URL
		result = find_matching_links(br, search_term[1:], result, visited)
		if (result):
			print result
			max_index = max(result, key=lambda u: u[1])[1]
			for l, i, c in result:
				print_url(l, i, max_index)
	except urlnorm.InvalidUrl:
		print "Invalid root URL"
	except urllib2.URLError:
		print "Error opening root URL"
	except Exception, e:
		print e
	finally:
		exit(1)




