import subprocess
bashCommand = "curl -Ls -o /dev/null -w %{{url_effective}} http://web.archive.org/web/20120202/{}"

def iterate_docs():
	with open("lookup", "r") as f:
		for row in f:
			query_id, doc_id, url = row.rsplit().split(" ")
			yield query_id, doc_id, url

if __name__ == '__main__':
	with open("final_urls", "w") as f:
		for query_id, doc_id, url in iterate_docs():
			request = bashCommand.format(url)
			process = subprocess.Popen(request.split(), stdout=subprocess.PIPE)
			output, error = process.communicate()
			f.write("{} {} {}\n".format(query_id, doc_id, output))
			print(output)
