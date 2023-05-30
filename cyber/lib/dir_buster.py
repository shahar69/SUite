import requests


def dirbust():
    target_url = input("Enter target URL: ")
    wordlist_path = input("Enter path to wordlist: ")
    try:
        wordlist = open(wordlist_path, "r")
        for line in wordlist:
            word = line.strip()
            test_url = target_url + "/" + word
            response = requests.get(test_url)
            if response.status_code == 200:
                print("<+> Discovered URL: " + test_url)
    except FileNotFoundError:
        print("<!> File not found. Exiting.")
