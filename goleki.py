import re, json
from requests import get
from argparse import ArgumentParser as AP

#intial
parser = AP()
parser.add_argument("-l","--language", help = "Set result language", default = "")
parser.add_argument("-m","--max", help = "Set max result", type = int, default = 0)
parser.add_argument("--safe", help = "Set safe mode (default is 0)", type = int, choices = [0,1], default = 0)
parser.add_argument("-u","--url", help = "Set inurl dork", default = "")
parser.add_argument("-s","--site", help = "Set site dork", default = "")
parser.add_argument("-t","--text", help = "Set intext dork", default = "")
parser.add_argument("--title", help = "Set intitle dork", default = "")
parser.add_argument("-c","--custom", help = "Set custom query", default = "")
args = parser.parse_args()

#init token
def sess():
	req = get("https://cse.google.com/cse.js?cx=007528173954226154940:ws_bsta-as8").content
	token = re.findall(b'"cse_token": "(.*?)"',req)[0].decode('utf-8')
	return(str(token))

#getting information here
def req(payload):
	url = "https://cse.google.com/cse/element/v1?{}&rsz=filtered_cse&cx=007528173954226154940:ws_bsta-as8&callback=cemara".format(payload+"&cse_tok="+str(sess()))
	res = get(url).content
	out = ''.join(res.decode('utf-8').split('\n')[1:])
	return json.loads('{"result" : [' + re.findall(r'"results": \[(.+)\]',out,re.I | re.M)[0] + ']}')

#build parameter payload
if args.custom:
	payload = "q=" + args.custom
else:
	payload = "q=intext:{},inurl:{},intitle:{}".format(args.text,args.url,args.title)
if args.site:
	payload += ",site:"+args.site
if args.safe:
	payload += "&safe=on"
else:
	payload += "&safe=off"
payload += "&hl=" + args.language
if args.max:
	payload += "&num=" + str(args.max)
print(req(payload))

'''
for page in [0,10,20,30,40,50,60,70,80,90]:
	for result in req(payload+"&num=10&start="+str(h))['result']:
		print result['url']
'''
