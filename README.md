# Browserstack
Technical Assignment: Run Selenium Test on BrowserStack


In this assignment we have two files where one is a python script and the other one is a browserstack .yml config file.

This code automatically visits the website https://elpais.com/ and then Prints the title and content of the first 5 article in Spanish
It also downloads the cover image of each article to your local machine and finally uses googletrans (from googletrans import Translator) to translate the title of each article to English
After that it identifies any words that are repeated more than twice across all headers combined and prints each repeated word along with the count of its occurrences.

Now we have also used cross browser Testing using browserstack where I have created a .yml config file for 5 Browsers on BrowserStack across 5 parallel threads. 


Steps are as the below:

Prerequisite
python3 should be installed

Clone the repo

pip3 install -r requirements.txt

browserstack-sdk Dhanvanth_browserstack.py
