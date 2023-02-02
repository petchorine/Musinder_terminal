import requests
from bs4 import BeautifulSoup


URL_WIKI = r"https://fr.wikipedia.org/wiki/Les_1001_albums_qu%27il_faut_avoir_%C3%A9cout%C3%A9s_dans_sa_vie"

def get_albums_content(URL_WIKI):
    page = requests.get(URL_WIKI)
    soup = BeautifulSoup(page.content, 'html.parser')
    tab_by_decade = soup.select("h3 + table")
    return tab_by_decade

def process_album_content(tab_by_decade):
    all_albums = []
    for idx1 in range(1, 9):
        for idx2 in range(idx1):        
            list_wthout_sort = []
            all_albums_by_decade = []
            lines_td = tab_by_decade[idx2].select("td")

            for line in lines_td:
                if line.a is None:
                    line = line.string.strip()
                else:
                    line = line.a.get("title")
                list_wthout_sort.append(line)

            lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
            list_decade = lol(list_wthout_sort, 4)
        
            for album_line in list_decade:
                index_id, artist, title, year = album_line
                new_entry = {"index_id": index_id, "artist": artist, "title": title, "year": year}
                all_albums_by_decade.append(new_entry)

        all_albums.append(all_albums_by_decade)
    return all_albums

def get_albums(URL_WIKI):
    tab_by_decade = get_albums_content(URL_WIKI)
    all_albums = process_album_content(tab_by_decade)
    nbr_total_album = sum([len(decade) for decade in all_albums])
    return all_albums, nbr_total_album

print(get_albums(URL_WIKI)[1])      # nbr d'albums
print(len(get_albums(URL_WIKI)[0][0]))
