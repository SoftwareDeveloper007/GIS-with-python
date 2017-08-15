import shapegeocode
import csv

gc = shapegeocode.geocoder('World_EEZ_v9_20161021/eez.shp')
fin = open('marineregions_input_example.csv', 'r')
fout = open('marineregions_output_example.csv', 'w', encoding='utf8', newline='')

#csv_reader = csv.DictReader(fin)
csv_reader = csv.reader(fin)
csv_writer = csv.writer(fout)
i = 0

print(csv_reader)
for row in csv_reader:
    if i == 0:
        row.extend(['Name', 'Sovereign', 'Success'])
        pass
    else:
        lat = float(row[1])
        lon = float(row[2])
        #lat = float(row['Latitude'])
        #lon = float(row['Longitude'])
        geocode = gc.geocode(lat, lon, max_dist=0)

        if geocode is not None:
            #row['Name'] = geocode['GeoName']
            #row['Sovereign'] = geocode['Sovereign1']
            #row['Success'] = 'FOUND'
            row.extend([geocode['GeoName'], geocode['Sovereign1'], 'FOUND'])
        else:
            #row['Name'] = ''
            #row['Sovereign'] = ''
            #row['Success'] = 'NOT FOUND'
            row.extend(['', '', 'NOT FOUND'])

    #print(row)
    csv_writer.writerow(row)
    #csv_writer.DictWriter(row)
    i += 1

#fclose(fin)
#fclose(fout)