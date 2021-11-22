from bs4 import BeautifulSoup as bs
import requests
import random 
import string
import argparse
import sys
import html5lib
import os


if not os.path.exists("output"):
    os.mkdir("output")
    print("Directory created.")

class Scraper:
    def __init__(self, debug):
        self.soup = bs
        self.debug = debug
        self.argparse = argparse.ArgumentParser()
        self.session = requests.Session()
        self.failure_image = open("ext/invalid.png", "rb").read()
        self.failure_image2 = open("ext/invalid_2.png", "rb").read()
    
    def random(self):
        return ''.join(random.choice(string.ascii_letters.lower()) for i in range(6))

    def cmp_img(self, first_bytes, second_bytes):
        if first_bytes == second_bytes:
            return True
        else:
            return False

    def get_image(self):
        r = self.random()
        request = self.session.get(f"https://prnt.sc/{r}", headers={'User-Agent': 'Mozilla/5.0'})
        if request.status_code == 200:
            _soup = self.soup(request.content, "html5lib")
            image_url = _soup.findAll('img', id="screenshot-image")[0]['src']
            return image_url
        else:
            if self.debug:
                print("[debug] Failed to get image")

    def download_image(self):
        image_url = self.get_image()
        try:
            request = self.session.get(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        except requests.exceptions.MissingSchema:
            request = self.session.get(f"https://{image_url}", headers={'User-Agent': 'Mozilla/5.0'})
        except:
            print("fail")
        if request.status_code == 200:
            if self.cmp_img(request.content, self.failure_image):
                if self.cmp_img(request.content, self.failure_image2):
                    print("[-] invalid image")
                    return False
            else:
                with open(f"output/{self.random() + self.random()}.png", "wb") as file:
                    file.write(request.content)
                    print(f"[+] Image saved.")

        else:
            if self.debug:
                print(f"[debug] Site responded with {request.status_code} | Image is likely invalid.")


parser = argparse.ArgumentParser()

parser.add_argument("--purge", "-p", help="Purge all images", action="store_true")
parser.add_argument("--download-images", "-d", help="Download images for count.", type=int)
parser.add_argument("--debug", help="Enable some annoying debug messages.", action="store_true")
#parser.add_argument("--threads", "-t", help="Number of threads to use.", type=int)



args = parser.parse_args()
scraper = Scraper(args.debug)

if args.purge is True:
    for f in os.listdir("output"):
        os.remove(f"output/{f}")
    print("[+] All cached images purged.")

for i in range(args.download_images):
    scraper.download_image()
