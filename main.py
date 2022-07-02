from tqdm import tqdm
import requests
import argparse
import threading

parser = argparse.ArgumentParser(description="Brute force wbesite directories")
parser.add_argument("-u", "--url", type=str, help="Target url")
parser.add_argument("-w", "--wordlist", type=str, help="Wordlist")
parser.add_argument("-i", "--ignore", type=str, help="Status code to ignore (E.g., -i 400, 304)", default="")
#parser.add_argument("-p", "--progress-bar", type=str, help="Disable/enable progress bar", default="True")
parser.add_argument("-t", "--threads", type=int, help="Number of threads", default=1)
args = parser.parse_args()
ignore_status = []

def status(url, directory):
    try:
        r = requests.get(f"{url}/{directory}")
    except Exception as e:
        return status(url, directory)
    if args.ignore.count(str(r.status_code)):
        return
    tqdm.write(f"/{directory} | status code --> [{r.status_code}]")

def main():
    current_line = 1
    wordlist_list = []
    index = 0
    wait = False
    #for line in open(args.wordlist, 'r'):
    lines = sum(1 for line in open(args.wordlist, encoding="ISO-8859-1"))
    with open(args.wordlist, 'r', encoding="ISO-8859-1") as f:
        for i, line in enumerate(tqdm(f, total=lines)):
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
