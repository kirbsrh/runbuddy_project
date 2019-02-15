import geocoder


def create_address_list():


    address_list = []
    address_file = open("test_data.txt")
    for row in address_file:
        row = row.rstrip()
        address_list.append(row)

    
    address_file.close()
    return address_list


def get_lat_lng_pairs():

    address_list = ['417 California Dr, Burlingame, CA 94010',
         '501 Primrose Rd, Burlingame, CA 94010',
        '20 Park Rd, Burlingame, CA 94010',
        '398 Primrose Rd, Burlingame, CA 94010',
        '1204 Burlingame Ave, Burlingame, CA 94010',
        '533 Airport Blvd, Burlingame, CA 94010',
        '1440 Chapin Ave, Burlingame, CA 94010',
        '851 Burlway Rd, Burlingame, CA 94010',
        '112 Anita Rd, Burlingame, CA 94010',
        '500 Airport Blvd, Burlingame, CA 94010',
        '1229 Burlingame Ave, Burlingame, CA 94010',
        '1027 California Dr, Burlingame, CA 94010',
        '1099 California Dr, Burlingame, CA 94010',
        '533 Airport Blvd, Burlingame, CA 94010',
        '1419 Burlingame Ave, Burlingame, CA 94010',
        '111 Anza Blvd, Burlingame, CA 94010',
        '714 Laurel Ave, Burlingame, CA 94010',
        '2480 Poppy Dr, Burlingame, CA 94010',
        '1799 Old Bayshore, Burlingame, CA 94010',
        '330 Primrose Rd, Burlingame, CA 94010',
        '1561 Ralston Ave, Burlingame, CA 94010',
        '1561 Ralston Ave, Burlingame, CA 94010', 
        '621 Magnolia Ave, Millbrae, CA 94030',
        '630 Hillcrest Blvd, Millbrae, CA 94030',
        '50 Victoria Ave, Millbrae, CA 94030',
        '214 Broadway, Millbrae, CA 94030',
        '370 Loyola Dr, Millbrae, CA 94030',
        '475 El Camino Real, Millbrae, CA 94030',
        '621 Magnolia Ave, Millbrae, CA 94030',
        '50 Victoria Ave, Millbrae, CA 94030',
        '423 Broadway, Millbrae, CA 94030',
        '485 Broadway, Millbrae, CA 94030',
        '501 Broadway, Millbrae, CA 94030',
        '10 Rollins Rd, Millbrae, CA 94030',
        '10 Guittard Rd, Burlingame, CA 94010',
        '130 S El Camino Real, Millbrae, CA 94030',
        '330 W 20th Ave, San Mateo, CA 94403',
        '477 9th Ave, San Mateo, CA 94402',
        '1400 Fashion Island Blvd, San Mateo, CA 94404',
        '675 Mariners Island Blvd, San Mateo, CA 94404',
           '181 2nd Ave, San Mateo, CA 94401',
            '1855 S Grant St, San Mateo, CA 94402',
             '1009 S Railroad Ave, San Mateo, CA 94402',
              '1650 Borel Pl, San Mateo, CA 94402',
               '2555 Flores St, San Mateo, CA 94403',
                '1710 S Amphlett Blvd, San Mateo, CA 94402',
                 '110 E 20th Ave, San Mateo, CA 94403',
                  '151 W 3rd Ave, San Mateo, CA 94402',
                   '220 Baldwin Ave, San Mateo, CA 94401',
                   '341 N Delaware St, San Mateo, CA 94401',
                    '525 N El Camino Real, San Mateo, CA 94401',
                    '2755 Campus Dr, San Mateo, CA 94403',
                     '181 2nd Ave, San Mateo, CA 94401',
                            '100 S Ellsworth Ave, San Mateo, CA 94401',
                            '618 San Mateo Ave, San Bruno, CA 94066',
                            '458 San Mateo Ave, San Bruno, CA 94066',
                             '851 Cherry Ave, San Bruno, CA 94066',
                              '1250 Bayhill Dr, San Bruno, CA 94066',
                               '1111 Bayhill Dr, San Bruno, CA 94066',
                                '398 El Camino Real, San Bruno, CA 94066',
                                 '1100 Grundy Ln, San Bruno, CA 94066',
                                  '851 Traeger Ave, San Bruno, CA 94066',
                                   '1212 El Camino Real, San Bruno, CA 94066',
                                    '1001 Bayhill Dr, San Bruno, CA 94066',
                                     '1245 San Mateo Ave, San Bruno, CA 94066',
                                      '671 San Mateo Ave, San Bruno, CA 94066',
               '1099 Sneath Ln, San Bruno, CA 94066',
                '1212 El Camino Real, San Bruno, CA 94066',
                 '851 Cherry Ave, San Bruno, CA 94066',
                  '723 Camino Plaza, San Bruno, CA 94066',
                   '280 E Grand Ave, South San Francisco, CA 94080',
                    '137 S Linden Ave, South San Francisco, CA 94080',
                     '142 Utah Ave, South San Francisco, CA 94080',
                     '1 Tower Pl, South San Francisco, CA 94080',
                      '451 E Jamie Ct, South San Francisco, CA 94080',
                       '5000 Shoreline Ct, South San Francisco, CA 94080',
                        '410 Allerton Ave, South San Francisco, CA 94080',
                         '415 Grand Ave, South San Francisco, CA 94080',
                          '333 Point San Bruno Blvd, South San Francisco, CA 94080',
                           '229 Utah Ave, South San Francisco, CA 94080',
                            '269 E Grand Ave, South San Francisco, CA 94080',
                             '450 E Jamie Ct, South San Francisco, CA 94080',
                              '900 Dubuque Ave, South San Francisco, CA 94080',
                               '275 S Maple Ave, South San Francisco, CA 94080',
                                '240 E Grand Ave, South San Francisco, CA 94080',
                                 '170 Harbor Way, South San Francisco, CA 94080',
                                  '400 Oyster Point Blvd, South San Francisco, CA 94080',
                                   '60 Airport Blvd, South San Francisco, CA 94080',
                                    '80 Tanforan Ave, South San Francisco, CA 94080',
                                     '270 E Grand Ave, South San Francisco, CA 94080',
                                      '151 Haskins Way, South San Francisco, CA 94080',
                                       '360 Shaw Rd, South San Francisco, CA 94080',
                                        '415 Browning Way, South San Francisco, CA 94080',
                                         '5 S Linden Ave, South San Francisco, CA 94080']

    lat_long_list = []

    for item in address_list:
        g = geocoder.osm(item)
        pair = g.latlng 
        lat_long_list.append(pair)
        # lat = g.latlng[0]
        # lng = g.latlng[1]
    print(lat_long_list)
    

        # lat_long_string = str(lat_long[0] + " " + lat_long[1])
        # lat_long_list.append(lat_long_string)

    
    # return lat_long_list

def read_lat_lng_file():

    lat_lng_file = open("lat_long_data.txt")
    for row in lat_lng_file:
        row = row.rstrip()
        lat, lng = row.split(",")
       
        lat = lat[1:]
        
        lng = lng[:-1]
        
    print(row)
    print(lat)
    print(lng)




