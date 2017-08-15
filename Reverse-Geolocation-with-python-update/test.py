import shapegeocode
import shapefile
import csv
import threading
import time

class GIS_main(object):
    def __init__(self):
        myshp = open("MEOW/meow_ecos.shp", "rb")
        mydbf = open("MEOW/meow_ecos.dbf", "rb")
        self.gc = shapegeocode.geocoder('World_EEZ_v9_20161021/eez_boundaries.shp')

        self.r = shapefile.Reader(shp=myshp, dbf=mydbf)

        self.fout = open('meow.csv', 'w', encoding='utf8', newline='')
        self.csv_writer = csv.writer(self.fout)

        row = ('id', 'ECO_CODE', 'ECOREGION', 'PROV_CODE', 'PROVINCE', 'RLM_CODE', 'REALM', 'ALT_CODE', 'ECO_CODE_X',
               'Lat_Zone', 'Country1', 'Country2', 'Country3', 'Country4', 'Country5', 'Country6')
        self.csv_writer.writerow(row)

        self.shapes = self.r.shapes()
        self.records = self.r.records()
        self.total_cnt = len(self.shapes)

    def GIS_process_queue(self, i):
        row = [i + 1]
        row.extend(self.records[i])
        row[1] = int(row[1])
        row[3] = int(row[3])
        row[5] = int(row[5])
        row[7] = int(row[7])
        row[8] = int(row[8])

        countries = []
        for point in self.shapes[i].points:
            geocode = self.gc.geocode(point[1], point[0], max_dist=0)
            if geocode is not None:
                if (not geocode['Sovereign1'] in countries) and (geocode['Sovereign1'] is not ''):
                    countries.append(geocode['Sovereign1'])
        row.extend(countries)
        self.csv_writer.writerow(row)
        print(i)

    def threading_GIS(self):
        start_time = time.time()
        self.threads = []
        max_threads = 20

        i = 0
        while self.threads or i < self.total_cnt:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)

            while len(self.threads) < max_threads and i < self.total_cnt:
                # can start some more threads
                thread = threading.Thread(target=self.GIS_process_queue, args=(i,))
                #thread.setDaemon(True)  # set daemon so main thread can exit when receives ctrl-c
                self.threads.append(thread)
                thread.start()
                i += 1

        self.fout.close()
        elapsed_time = time.time() - start_time
        print(elapsed_time)


if __name__ == '__main__':
    gis = GIS_main()
    gis.threading_GIS()