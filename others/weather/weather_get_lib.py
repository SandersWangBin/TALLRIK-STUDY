import urllib.request
import codecs
import re

HTML_TAG_CLOCK = 'klokken'
HTML_TAG_TEMP  = 'temperature plus'
REG_LAST_ITEM  = r'.*>(.*)</td>'

def write_to_file(output):
    file = codecs.open("Output.txt", "w", "utf-8")
    file.write(output)
    file.close()

def weather_fetch_from_web():
    full_api_url = 'https://www.yr.no/sted/Sverige/Stockholm/Stockholm/'
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    url.close()
    return output

def get_info_by_tag(line, tag):
    if tag in line:
        matchObj = re.match(REG_LAST_ITEM, line)
        if matchObj: return matchObj.group(1)
    return None
        
def weather_info_analyze(output):
    weather_info_list = list()
    clock_info = None
    for line in output.split('\n'):
        if clock_info == None:
            clock_info = get_info_by_tag(line, HTML_TAG_CLOCK)
        else:
            info = get_info_by_tag(line, HTML_TAG_TEMP)
            if info != None:
                weather_info_list.append((clock_info.strip(), info))
                clock_info = None
    return weather_info_list



print(weather_info_analyze(weather_fetch_from_web()))

