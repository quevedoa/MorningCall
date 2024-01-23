#!/bin/bash
cd /Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet
echo -e "\nCron job (scraping) ran at: $(date)" >> /Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/ScrapingCronJob.log
/usr/local/bin/python3 /Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/scraper_articulo_elceo.py
/usr/local/bin/python3 /Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/scraper_articulo_eleconomista.py
/usr/local/bin/python3 /Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/scraper_articulo_elfinanciero.py
/usr/local/bin/python3 /Users/quevedo/Documents/ITAM/Tesis/MorningCall/NewsScraping/CreatingTrainingDataSet/scraper_articulo_forbes.py
