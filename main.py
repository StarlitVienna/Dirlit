import requests
import argparse
import threading

parser = argparse.ArgumentParser(description="Brute force wbesite directories")
parser.add_argument("-u", "--url", type=str, help="Target url")
parser.add_argument("-w", "--wordlist", type=str, help="Wordlist")
#parser.add_argument("-i", "--ignore", type=str, help="Status code to ignore")
parser.add_argument("-t", "--threads", type=int, help="Number of threads", default=1)
args = parser.parse_args()

def status(url, directory):
    r = requests.get(f"{url}/{directory}")
    print(f"/{directory} | status code --> [{r.status_code}]")

def main():
    current_line = 1
    wordlist_list = []
    index = 0
    wait = False
    for line in open(args.wordlist, 'r'):
        if threading.active_count() == args.threads+1:
            wait = True
        while wait:
            if threading.active_count() < args.threads+1:
                wait = False
        wordlist_list.append(line[:-1])
        threading.Thread(target=status, args=(args.url, wordlist_list[index])).start()
        index += 1

if __name__ == "__main__":
    main()
# maybe add a loading bar
# filter status code
