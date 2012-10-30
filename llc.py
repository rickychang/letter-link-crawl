import mechanize
import sys

def find_matching_links(br, target_word, result, visited):
	if (not target_word):
		return result
	else:
		letter = target_word[0]
		if (letter.isspace()):
			return find_matching_links(br, target_word[1:], result + [('', -1, ' ')], visited)
		else:
			matches = [(link, link.absolute_url[7:].find(letter.lower()) + 7) for link in br.links() if link.absolute_url[7:].find(letter.lower())!= -1]
			for m in matches:
				try:
					if (m[0].absolute_url not in visited):
						visited.add(m[0].absolute_url)
						print m[0].absolute_url
						br.follow_link(m[0])
						child_result = find_matching_links(br, target_word[1:], result + [(m[0].absolute_url, m[1], letter)], visited)
						if (child_result):
							return child_result
						else:
							br.back()
				except Exception as e:
					pass
	return []

def print_url(url, letter_index, display_width):
	if (not url or letter_index == -1):
		print ''
	else:
		padding = ' ' * ((display_width / 2) - letter_index)
		print '%s%s %s %s' % (padding, url[0:letter_index], url[letter_index], url[letter_index+1:])


if (len(sys.argv) < 3 ):
	print "usage: ll-print.py <url> <search term>"
	print "example: ll-print.py http://www.hunch.com 'hunch team'"
	exit(0)
root_URL = sys.argv[1]
search_term = sys.argv[2]
first_letter = search_term[0]
first_letter_match = root_URL.find(first_letter.lower())
if (first_letter_match != -1):
	br = mechanize.Browser()
	result = [(root_URL, first_letter_match, first_letter)]
	visited = set([root_URL])
	print root_URL
	try:
		br.open(root_URL)
		result = find_matching_links(br, search_term[1:], result, visited)
		if (result):
			print result
			max_length = len(max(result, key=lambda u: len(u[0]))[0])
			for l, i, c in result:
				print_url(l, i, max_length * 2)
	except Exception as e:
		exit(1)




