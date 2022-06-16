import time
from threading import *
from tkinter import *
from bs4 import BeautifulSoup  # parsing module
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# instance of Options class allows
# us to configure Headless Chrome
options = Options()
# this parameter tells Chrome that
# it should be run without UI (Headless)
options.headless = True


def threading():
    t1 = Thread(target=scrape)
    t1.start()


def begin():
    startLabel.grid(row=4, column=1)


def scrape():
    # link to the website, use browser headers to connect
    driver = webdriver.Chrome(options=options)

    driver.get('http://soundcloud.com/' + textField.get() + '/likes')  # target URL
    # driver.get('http://soundcloud.com/scrapertest/likes')  # test target URL
    time.sleep(5)  # allows 5 seconds for webpage to load
    html = driver.page_source
    BeautifulSoup(html, 'lxml')

    track_artists = []
    track_names = []
    complete = []

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(5)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    items4 = soup.find_all('li', class_='soundList__item')
    items = soup.find_all('div', class_='soundTitle__usernameTitleContainer')
    items2 = soup.find_all('a', class_='sc-link-primary soundTitle__title sc-link-dark sc-text-h4')
    items3 = soup.find_all('a',
                           class_='sc-link-primary soundTitle__title g-opacity-transition-500 g-type-shrinkwrap-block '
                                  'g-type-shrinkwrap-primary theme-dark sc-text-h4')

    i = 0  # Iterating through each li tag which each song is placed in dynamically
    j = 0  # Iterating through each song with a fancy background
    k = 0  # Iterating through each song without fancy background

    if len(items3) == 0:
        while i < len(items4):
            track_names.append(items2[k].find('span').get_text().strip())
            i += 1
            k += 1
    elif len(items3) > 0:
        while i < len(items4):
            if items3[j].get_text() in items4[i].get_text():
                track_names.append(items3[j].find('span', class_='sc-truncate').get_text().strip())
                i += 1
                if j == len(items3) - 1:
                    j += 0
                else:
                    j += 1
            else:
                track_names.append(items2[k].find('span').get_text().strip())
                i += 1
                k += 1

    for item in items:
        track_artists.append(item.find('span', class_='soundTitle__usernameText').get_text().strip())

    for x in range(len(track_artists)):
        complete.append(f"{track_artists[x] + ' - ' + track_names[x]}")
        Output.insert(END, complete[x] + '\n')
        time.sleep(.1)
    completeLabel.config(text="Scrapped All Songs")
    startLabel.destroy()
    with open('Soundcloud Likes.txt', 'w', encoding="utf-8") as f:
        for item in complete:
            f.write("%s\n" % item)
    totalLikes = "Total likes: %d" % len(complete)
    totLikesLabel = Label(root, text=totalLikes, font=("Arial", 25))
    totLikesLabel.grid(row=2, column=1)
    finishedLabel = Label(root, text="Finished. You may now quit", font=("Arial", 25))
    finishedLabel.grid(row=4, column=1)
    driver.quit()


root = Tk()
v = StringVar()
root.geometry("1200x800")
root.title("Soundcloud Likes Scraper")
startLabel = Label(root, text="Started Scrape...", font=("Arial", 25))
completeLabel = Label(root, text="", font=("Arial", 25))
nameLabel = Label(root, text="Enter the users URL profile name: ", relief="sunken", font=("Arial", 25))
textField = Entry(root, font=("Arial", 25))
runButton = Button(text="Run",
                   height=2,
                   width=20,
                   font=("Arial", 13),
                   bg='white',
                   fg='black',
                   command=lambda: [begin(), threading()])

completeLabel.grid(row=3, column=0, padx=0, pady=0)
nameLabel.grid(row=0, column=0, ipadx=10, ipady=5, padx=10, pady=10)
textField.grid(row=1, column=0,
               ipadx=5,
               ipady=5, pady=20)
runButton.grid(row=2, column=0, pady=10)
Output = Text(root, width=75, height=30)
Output.grid(row=3, column=1, padx=20, pady=5)
root.mainloop()
