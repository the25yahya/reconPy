import subprocess


def append_file_contents(source_file, destination_file):
    try:
        with open(source_file, 'r') as src:
            data = src.read()
        
        with open(destination_file, 'a') as dest:
            dest.write(data)
        print(f"[*] Successfully appended contents of {source_file} to {destination_file}")
    except Exception as e:
        print(f"[*] An error occurred: {e}")

#js_discovery######################################
def js_discovery(domain,directory):
    print("[*] starting website js discovery ...")
    print("[*] running SubDomainizer ...")
    subdomainizer = subprocess.run(f"python3 /home/kali/SubDomainizer/SubDomainizer.py -u https://{domain} -o SubDomainizer_{domain}.txt",shell=True,stdout=subprocess.PIPE,
                                   text=True,stderr=True)
    if subdomainizer.returncode == 0 :
        print("[*] got subdomains ...")
        print("[*] adding subdomains to output file ...")
        append_file_contents(f"SubDomainizer_{domain}.txt", f"{directory}/subdomains/subdomains.txt")

    else:
        print(f"[*] error running subdomainizer : {subdomainizer.stderr}")

#scraping########################################
def scraping(domain,directory):
    print("[*] starting subdomain scraping ...")
    print("[*] running subfinder ...")
    subfinder = subprocess.run(f"subfinder -d {domain} -o subfinder_{domain}.txt",shell=True,stdout=subprocess.PIPE,
                               text=True,stderr=True)
    if subfinder.returncode == 0:
        print("[*] got subfinder results...")
        print("[*] adding subdomains to output file ...")
        with open(f"{directory}/subdomains/subdomains.txt","a") as f:
            f.write(subfinder.stdout)
    else:
        print(f"error running subfinder : {subfinder.stderr}")
        print("")
        print("")
    print("[*] running assetfinder ...")
    assetfinder = subprocess.run(f"assetfinder --subs-only {domain}",shell=True,stdout=subprocess.PIPE,
                                 text=True,stderr=True)
    if assetfinder.returncode == 0:
        print("[*] got assetfinder results...")
        print("[*] adding subdomains to output file...")
        with open(f"{directory}/subdomains/subdomains.txt","a") as f:
            f.write(assetfinder.stdout)
    else:
        print(f"error running assetfinder: {assetfinder.stderr}")



#brute forcing#######################################
def brute_forcing(domain, wordlist_path, directory):
    print("[*] Starting DNS brute forcing ...")
    print("[*] Running Gobuster ...")

    # Run Gobuster and capture the output
    gobuster = subprocess.run(
        f"gobuster dns -d {domain} -w {wordlist_path} -t 60 -o gobuster_{domain}.txt --wildcard",
        shell=True,
        stdout=subprocess.PIPE,
        text=True,
        stderr=subprocess.PIPE
    )
    
    if gobuster.returncode == 0:
        print("[*] Gobuster finished successfully.")
        print("[*] Processing Gobuster results ...")

        # Read and process the Gobuster output file
        gobuster_lines = []
        with open(f"gobuster_{domain}.txt", "r") as f:
          for line in f:
            gobuster_lines.append(line.strip().replace("Found: ", ""))
        # Write the processed lines to the subdomains file
        with open(f"{directory}/subdomains/subdomains.txt", "a") as f:
          for line in gobuster_lines:
            f.write(line)
        
        print("[*] Subdomains added to output file.")
    else:
        print(f"Error running Gobuster: {gobuster.stderr}")

