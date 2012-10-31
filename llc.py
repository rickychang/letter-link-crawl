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
		current_URL = urlnorm.norm(br.geturl())
		current_letter = target_word[0].lower()
		if (current_letter.isspace()):
			return find_matching_links(br, target_word[1:], result + [('', -1, ' ')], visited)
		else:
			matching_index = current_URL[7:].find(current_letter)
			if (matching_index == -1):
				return []
			else:
				new_result = result + [(current_URL, matching_index + 7, current_letter)]
				links = list(br.links())
				for link in links:
					try:
						link_URL = urlnorm.norm(link.absolute_url)
						if (link_URL not in visited):
							br.open(link_URL)
							visited.add(link_URL)
							print "visiting: " + urlnorm.norm(br.geturl())
							visited.add(urlnorm.norm(br.geturl()))
							child_result = find_matching_links(br, target_word[1:], new_result, visited)
							if (child_result):
								return child_result
 					except Exception, e:
						continue
	# print "backtracking"
	return []


def main():
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
			br._factory.is_html = True
			result = []
			br.open(root_URL)
			print "visiting: " + urlnorm.norm(br.geturl())
			visited = set([urlnorm.norm(br.geturl()), urlnorm.norm(root_URL)])
			result = find_matching_links(br, search_term, result, visited)
			if (result):
				max_index = max(result, key=lambda u: u[1])[1]
				for l, i, c in result:
					print_url(l, i, max_index)
		except urlnorm.InvalidUrl:
			print "Invalid root URL"
		except urllib2.URLError, e:
			print "Error opening root URL"
			print e
		except Exception, e:
			print e
		finally:
			exit(1)

if __name__ == "__main__":
    main()


