# -*- coding: utf-8 -*-
import os
import json
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import requests
from bs4 import BeautifulSoup
 

def extract_pages_urls(URL):
    """ Get the 5 URL's (pages) that are in the main page
    Input: Main URL
    Output: Set of URL of the different pages """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    pagination = soup.find('div', class_="pagination1")
    pages_urls = set()
    for page in pagination.find_all("a"):
        pages_urls.add(page.attrs['href'])
    return(pages_urls)

def extract_book_links(URL):
    """ Get links of all the books in the page (URL) 
    Input: URL of the given page
    Output: Set of book urls"""
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(id="prod")
    book_links = set()
    for res in results:
        book = res.find("a", rel="noopener noreferrer")
        book_links.add(book.attrs['href'])
    return book_links

def clean_txt(txt, remove_list=['\xa0', '<strong>', '</strong>', '<br/>']):
    """ Remove elements from the remove rist given a txt 
    Input: String text, list of elements to remove
    Output: String clean text"""
    for element in remove_list:
        txt = txt.replace(element, '')
    clean_txt = txt.strip()
    return clean_txt

def get_text(res_line):
    """"""
    try:
        text = '\n'.join([str(cont.text) for cont in res_line.contents if str(cont.text) != '<br/>'])
    except:
        text = '\n'.join([str(cont) for cont in res_line.contents if str(cont) != '<br/>'])
    finally:
        text = clean_txt(text)
    return text

def get_book(URL):
    page = requests.get(URL)
    book_soup = BeautifulSoup(page.content, "html.parser")
    is_book_active = False
    last_turn = 'image'
    book_txt = []
    book_img = []
    results = book_soup.find_all(['div', 'p'], style=['text-align: left;', 'text-align: start;',''])
    for res in results:
        # Check if the html is book story
        if ((res.name == 'p') and (len(res.contents) > 0)):
            if ((
                    ('contents' in vars(res.contents[0]).keys()) and
                    (len(res.contents[0].contents) > 1) and
                    (any(str(cont).find('Click here to read more Free') != -1 for cont in res.contents[0].contents)))
                or
                    any(str(cont).find('Click here to read more Free') != -1 for cont in res.contents)):
                
                is_book_active = True
                continue
            elif ((
                    ('contents' in vars(res.contents[0]).keys()) and
                    (len(res.contents[0].contents) > 1) and
                    (any(str(cont).find('Please share our books') != -1 for cont in res.contents[0].contents)))
                or
                    any(str(cont).find('Please share our books') != -1 for cont in res.contents)):
                
                is_book_active = False
                break
    
        if is_book_active: # Book pages html
        # Check images
            if (    (len(res.contents) > 0) 
                and 
                    (('attrs' in vars(res.contents[0]).keys()) and
                    ('src' in res.contents[0].attrs.keys()))
                or
                    ((len(res.contents) > 1) and
                    ('attrs' in vars(res.contents[1]).keys()) and
                    ('src' in res.contents[1].attrs.keys()))): # Extract image link
                
                try:
                    image_link = res.contents[0]['src']
                except:
                    image_link = res.contents[1]['src']
                book_img.append(image_link)
                last_turn = 'image'
        
            elif (
                    (len(res.contents) > 0) 
                and 
                    (('contents' in vars(res.contents[0]).keys()) and
                    (len(res.contents[0].contents) > 0) and
                    ('attrs' in vars(res.contents[0].contents[0]).keys()) and
                    ('src' in res.contents[0].contents[0].attrs.keys()))): # Extract image link

                image_link = res.contents[0].contents[0]['src']
                book_img.append(image_link)
                last_turn = 'image'

            # Extract text
            else: 
                text = get_text(res)
                if len(text) > 0:
                    if last_turn == 'text': # Add to previous text chunk
                        book_txt[-1] += '\n' + text
                    else: # Add as new text chunk
                        book_txt.append(text)
                        last_turn = 'text'

    return {'book_txt': book_txt[:], 'book_img': book_img[1:]} # The first image is book cover


def main(input_url, output_filepath):
    """ Loads data from URL """
    logger = logging.getLogger(__name__)
    logger.info('Getting Data from URL')

    all_book_links = set()
    for URL in extract_pages_urls(input_url):
        all_book_links = all_book_links.union(extract_book_links(URL))

    logger.info(f'We have obtained {len(all_book_links)} links from different books')

    books = []
    for URL in all_book_links:
        book = get_book(URL)
        book_txt, book_img = book['book_txt'], book['book_img']  

        if abs(len(book_txt) - len(book_img)) > 2:
            continue # Too much differece

        elif len(book_txt) - len(book_img) >= 1:
            while len(book_txt) - len(book_img) != 0:
                book_txt.pop() # Correct extra txt
        
        elif len(book_img) - len(book_txt) >= 1:
            while len(book_img) - len(book_txt) != 0:
                book_img.pop() # Correct extra img

        book = {'book_txt': book_txt, 'book_img': book_img, 'book_url': URL}
        books.append(book)

    books_dict = {i: list(zip(books[i]['book_txt'], books[i]['book_img'])) for i in range(len(books))}
    
    with open(output_filepath, 'w') as f:
        json.dump(books_dict, f)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]
    output_filepath = os.path.join(project_dir, "data", "raw.json")
    print(output_filepath)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    input_url = os.getenv("URL_BOOKS")

    main(input_url, output_filepath)
