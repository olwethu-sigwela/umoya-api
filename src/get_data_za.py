import mtn_scraper_za
import cell_c_scraper_za
import telkom_scraper_za
import vodacom_scraper_za
import rain_scraper_za

def main():
    mtn_scraper_za.get_prepaid()
    cell_c_scraper_za.get_prepaid()
    telkom_scraper_za.get_prepaid()
    vodacom_scraper_za.get_prepaid()
    rain_scraper_za.get_prepaid()
    
if __name__ == "__main__":
    main()