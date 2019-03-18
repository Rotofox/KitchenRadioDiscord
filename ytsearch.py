import urllib.parse, urllib.request, re
class Search():
# Searches youtube for string 'query' and plays the first result on the page
    def findvid(search):
        query_string = urllib.parse.urlencode({
            'search_query': search
            })
        htm_content = urllib.request.urlopen(
            'https://www.youtube.com/results?' + query_string
        )
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
        return 'https://www.youtube.com/watch?v=' + search_results[0]