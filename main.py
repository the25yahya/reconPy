import argparse
import threading
import recon
import os



parser = argparse.ArgumentParser(
    description="reconnaisance framework",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

##adding arguments
parser.add_argument('-d',"--domain",type=str,help="domain to perform recon")
parser.add_argument('-l',"--linked",action="store_true",help="linked discovery mode")
parser.add_argument('-j',"--js",action="store_true",help="js discovery mode")
parser.add_argument('-s',"--scrape",action="store_true",help="scraping mode")
parser.add_argument('-b',"--brute",action="store_true",help="brute forcing mode")
parser.add_argument('-w','--wordlist',type=str,help="a wordlist for bruteforcing mode")
parser.add_argument('-o','--output',type=str,help="a directory path to add subdomains to")
args = parser.parse_args()
threads = []


##creating neccessary files and dirs
if args.output:
    DIR = str(args.output)
else :
    DIR = f"{args.domain}_recon"

print(f"making output directory : {DIR}")
os.makedirs(f"{DIR}/subdomains",exist_ok=True)
print("starting recon ...")
print("")
print("")



if args.scrape:
    t1 = threading.Thread(target=recon.scraping, args=(args.domain,DIR,))
    t1.start()
    threads.append(t1)


if args.js:
    t3 = threading.Thread(target=recon.js_discovery, args=(args.domain,DIR,))
    t3.start()
    threads.append(t3)

if args.brute and args.wordlist:
    t4 = threading.Thread(target=recon.brute_forcing,args=(args.domain,args.wordlist,DIR,))
    t4.start()
    threads.append(t4)

for t in threads :
    t.join()

print("all tasks completed")
