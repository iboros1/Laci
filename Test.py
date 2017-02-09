def met1():
    a = 1
    b = 2  +c
    return a, b
a, b = met1()



def met2(a ,b):
    c = a + b
    print(c)

met2(a ,b)



def write_to_db(get_db_bike_list,brows_pages):
        if 'olx' in beautiful_page_result.attrs['href']:
            bike_url, diez, unused_id = dirty_bike_link.partition('#')
            title = beautiful_page_result.find_all('strong')
            web_bike_list.append((bike_url, title))
    return beautiful_page_result,web_bike_list


def write_to_db(get_db_bike_list,web_bike_list):
    db_add_date = strftime("%Y-%m-%d")
    get_db_bike_list.db_cursor.execute(
       "INSERT INTO Page (DateAdded, HtmlBike, AdName) VALUES ('%s','%s', '%s')" % (db_add_date, brows_pages.bike_url, brows_pages.title))


def compare_lists(db_bike_list, web_bike_list):

    unique_bike_list = []
    for bike in web_bike_list:
        if bike not in db_bike_list:
         unique_bike_list.append(bike)


    for bike in web_bike_list[1]:
        if bike[0] not in db_bike_list[0]:
            unique_bike_list.append(bike)
        else:
            pass


