import csv
import json
import time
import requests

# The list of Külképviselet provided by the user
data_str = """"Ország, település","Külképviselet címe","Névjegyzékbe vett választópolgárok száma","Akadálymentesség","A szavazás ideje","Kérelem benyújtásának határideje"
"Albánia, Tirana","Magyarország Nagykövetsége, Tirana, Rruga Kuvajt 47.","33","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Algéria, Algír","Konzuli Hivatal, 29, Chemin Ismail Chaalal, El Mouradia, Alger","8","nem akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Amerikai Egyesült Államok, Chicago","Magyarország Főkonzulátusa, 303 East Wacker Drive, Unit: 2050, Chicago, IL 60601","61","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Amerikai Egyesült Államok, Houston","Magyarország Alkonzulátusa, 1980 Post Oak Blvd ste 200, Houston, TX 77056","61","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Amerikai Egyesült Államok, Los Angeles","Magyarország Főkonzulátusa, 11766 Wilshire Blvd, Suite 410, Los Angeles, CA 90025","94","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Amerikai Egyesült Államok, Miami","Miami Alkonzulátus –2121 Ponce de Leon Blvd Suite 732, Coral Gables, FL, 33134","125","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Amerikai Egyesült Államok, New York","New York Főkonzulátus, 223 East 52nd Street, New York, N.Y., 10022-6301.","287","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Amerikai Egyesült Államok, San Francisco","5201 Great America Parkway, Suite 320, Techmart Business Center, Santa Clara, CA 95054","71","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Amerikai Egyesült Államok, Washington","Magyarország Nagykövetsége, 3910 Shoemaker Street, N.W. Washington, D.C. 20008","127","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Angola, Luanda","Magyarország Nagykövetsége, Luanda, Condomínio Zenith Towers, Torre 1., 8. andar, VIA AL-16, Talatona, Angola","1","akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Argentína, Buenos Aires","Embajada de Hungría, Suipacha 1111. 9. emelet C.F. Buenos Aires (CD1008)","18","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ausztrália, Canberra","Magyarország Nagykövetsége, Canberra; 17 Beale Crescent, Deakin, ACT 2600, Ausztrália","17","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ausztrália, Melbourne","Magyarország Konzuli Irodája, Melbourne; 123 St. Georges Road, Fitzroy North, VIC 3068, Ausztrália","53","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ausztrália, Sydney","Ground level, 321 Kent Street, Sydney NSW 2000","104","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ausztria, Bécs","Magyarország Nagykövetsége, 1010 Wien, Bankgasse 6.","412","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ausztria, Innsbruck","Magyarország Főkonzulátusa, 6020 Innsbruck, Speckbacherstrasse 31-33","274","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Azerbajdzsán, Baku","Magyarország Bakui Nagykövetsége, Mirza Mansur 72-74, Icheri Sheher, 1004 Baku, Azerbajdzsán","14","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Banglades, Dakka","Concord I-K Tower, Madani Avenue, 6. emelet, Gulshan 2, Dakka, Banglades - 1212","0","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Belarusz Köztársaság, Minszk","Magyarország Nagykövetsége, Belarusz Köztársaság, 220034 Minszk, Platonova utca 1/B.","4","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Belgium, Brüsszel","Magyarország Nagykövetsége, Brüsszel, 44 Avenue du Vert Chasseur, 1180 Bruxelles","512","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Bosznia-Hercegovina, Szarajevó","Magyarország Nagykövetsége, 71000 Szarajevó, Splitska 2. Bosznia-Hercegovina","21","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Brazília, Brazíliaváros","Magyarország Nagykövetsége, S.E.S Avenida das Nacoes, Quadra 805, Lote 19. CEP: 70413-900 DF-Brasília","6","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Brazília, Sao Paulo","Magyarország Főkonzulátusa, Cidade Jardim Corporate Center Av. Magalhaes de Castro 4800, Edif. Park Tower, 21o and. cj. 212. - 05676-120, Sao Paulo-SP","19","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Bulgária, Szófia","Magyarország Szófiai Nagykövetsége Sofia Center, 6th September St 57, 1000 Sofia","26","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Chile, Santiago de Chile","Magyarország Nagykövetsége, Santiago de Chile, Avenida Los Leones 2279, Providencia, Santiago de Chile","18","nem akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ciprus, Nicosia","72 Lemesou Avenue, (Asteroid Tower, 6. emelet), 2014 Nicosia","69","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Csád, N'Djamena","Magyarország Nagykövetsége, N'Djaména, Rue 1039, Hôtel La Résidence, 4. emelet","1","nem akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Csehország, Prága","Magyarország Nagykövetsége, Prága, Pod Hradbami 17, 16000","121","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Dánia, Koppenhága","Glostrup Hallen, Stadionvej 80, 2600 Glostrup, Dánia","511","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Dél-afrikai Köztársaság, Pretoria","Magyarország Nagykövetsége, Pretoria, 959 Arcadia Street, Hatfield, Pretoria 0083","11","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ecuador, Quito","Magyarország Nagykövetsége, Edificio Multiapoyo, 6. emelet, Pedro Ponce Carrasco E9-25 y Avenida 6 de Diciembre, 170517, Quito, Ecuador","7","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Egyesült Arab Emírségek, Abu Dhabi","Magyarország Nagykövetsége, Al Khazna Tower VI. em. 603-604 iroda, P.O. Box 44450, Abu Dhabi, UAE","136","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2:00, 16:00 (CET)"
"Egyiptom, Kairó","Magyarország Nagykövetsége, Kairó, Mohamed Mazhar st. 29., Zamalek, 11211","26","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Észak-Macedónia, Szkopje","Észak-macedón Köztársaság, Magyarország Nagykövetsége, 1000, Szkopje, Mirka Ginova u. 27.","15","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Észtország, Tallinn","Magyarország Nagykövetsége, Tallinn, Maakri 19/1, 28. emelet, 10145 Tallinn","29","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Etiópia, Addisz-Abeba","Magyarország Nagykövetsége (Addisz-Abeba, Bole sub-city, Woreda 03, House No. 4002. SNAP Plaza 4. emelet","2","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Finnország, Helsinki","Nagyköveti rezidencia, 00340 Helsinki, Intendentinkuja 6.","221","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Franciaország, Lyon","7 rue de la Poudrière, 69001 Lyon, France","80","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Franciaország, Párizs","KONZULI HIVATAL, 7, square Vergennes, 75015 PARIS","365","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Franciaország, Strasbourg","Európa Tanács melletti Állandó Képviselet, 4 rue Richard Brunck, 67000 Strasbourg","43","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Fülöp-szigetek, Manila","8th Floor, DelRosarioLaw Centre, 21st Drive, Bonifacio Global City, 1630 Taguig City, Metro Manila, Fülöp-szigetek","8","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ghána, Accra","Magyarország Nagykövetsége, Accra, Plot No.44, 6th Circular Road, Cantonments, Accra","4","akadálymentes","2026. április 12., 06:00 - 17:00","2026. április 2., 16:00 (CET)"
"Görögország, Athén","Magyarország Nagykövetsége, Athén Konzuli Hivatal, 11635, Athén Vasileos Konstantinou 38. 4. emelet","83","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Grúzia, Tbiliszi","Magyar Nagykövetség Tbiliszi, 83. Lvovi street, Saburtalo, 0160 Tbiliszi (Budapesti str. irányából megközelítve)","18","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Hollandia, Hága","Leonardo Royal Hotel Den Haag Promenade; Van Stolkweg 1, 2585 JL Den Haag","1349","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Horvátország, Eszék","Horvátország, 31000 Eszék, Vijenac Ivana Mažuranića 3.","4","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Horvátország, Zágráb","Liszt Intézet 10000 Zágráb, Augusta Cesarca 10.","18","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"India, Mumbai","TCG Financial Centre, C-53/G-Block, Bandra-Kurla Complex, Mumbai – MH (Maharashtra) 400098, India","11","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"India, Újdelhi","Újdelhi Nagykövetség, 2/50-M, Niti Marg, Chanakyapuri, New Delhi, Delhi 110021","8","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Indonézia, Jakarta","Jalan Rasuna Said X/3. No. 1. Kuningan, Jakarta Selatan 12950 Embassy of Hungary","36","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Irak, Erbil","319/246-5 Gulan Street – Double Side New Baharka Road, Erbil, Kurdistan Region, Iraq","0","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Irán, Teherán","Magyarország Nagykövetsége, Darrous, Yakhchal Street 11., Tehran, 1943964511","2","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Írország, Dublin","St. Christopher’s Primary School, Haddington Road, Ballsbridge, Dublin 4, DO4 FP20","448","akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Izrael, Tel-Aviv","Tel-Aviv 6266108, Pinkas St. 18.","48","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Japán, Osaka","Magyaroszág Oszakai Konzulátusa, 1408, 1-1-27 Dojimahama, Kita Ward, Osaka, 530-0004","56","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Japán, Tokió","Magyarország Nagykövetsége, Tokió, 2-17-14 Mita, Minato-ku, Tokyo 108-0073","156","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Jordánia, Amman","Magyarország Nagykövetsége, Amman, 11181 Jordan, Amman, 24 Hani Al-Akasheh Street","13","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kambodzsa, Phnom Penh","Magyarország Hanoi Nagykövetségének Phnom Penh-i Irodája, 313 Sisowath Quay, Chakto Mukh, Doun Penh, Phnom Penh 120207, Kambodzsa (Hotel Cambodiana)","0","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kanada, Montreal","1155 Metcalfe Street, Salle Cartier, 15th floor, Sun Life Building, Montreal, H3B 2V6, QC, Kanada","24","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kanada, Ottawa","299 Waverley Street, Ottawa, ON K2P 0V9","19","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kanada, Toronto","175 Bloor Street East, #1109, South Tower, Toronto, ON, M4W 3R8","84","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kanada, Vancouver","808 Nelson Street, #701, Vancouver, BC, V6Z 2H2","54","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Katar, Doha","Magyarország Nagykövetsége, Doha, West Bay, Zone 66, Saha 83, Villa No. 15. Qatar","36","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kazahsztán, Almati","Magyarország Almati Főkonzulátusa, 050043 Almati, Muszabajeva utca 4.","6","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kazahsztán, Asztana","Magyarország Nagykövetsége Asztana, 010000 Asztana, Kosmonavtov u. 62. – RENCO irodaház, 9. emelet","6","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kenya, Nairobi","Kabarsiran Gardens (off James Gichuru road), Lavington, Nairobi; P.O. Box: 61146-00200","10","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kína, Csungking","CCOOP International Center 36-A, No. 235 Minsheng Rd., Yuzhong District, 400010 Chongqing, People’s Republic of China","27","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kína, Hongkong","Suites 1208-09, 12/F, ICBC Tower, Three Garden Road, Central, Hongkong","37","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kína, Kuangcsou","Kuangcsou, Yuexiu District, Qiaoguang West Road No. 13, Building T1, Floor 25 Office 2507-09, 510240","7","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kína, Peking","Kínai Népköztársaság, 100600 Peking, San Li Tun, Dong Zhi Men Wai 10.","54","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kína, Sanghaj","200010 Sanghaj, Huangpu kerület, Zhongshan East 2nd út 600., Bund Financial Center, 3503-06-os szobák","30","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kirgizisztán, Biskek","Kyrgyzstan, Bishkek, Gogol str. 77/1, 720011","3","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kolumbia, Bogota","Bogotá, Carrera 7 no. 75-51, 301. iroda (Edificio Terpel)","8","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kongói Demokratikus Köztársaság, Kinshasa","Avenue des Lilas No. 3, Kinshasa/Gombe","1","akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Koreai Köztársaság, Szöul","Szöul, Yongsan-gu (Dongbinggo-dong), Jangmun-ro 58","103","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Koszovó, Pristina","Koszovói Köztársaság, Magyarország Nagykövetsége, 10000 Pristina (Arbëria negyed) , Arben Xheladini utca 157.","39","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kuba, Havanna","Magyarország Nagykövetsége Havanna, Vedado Calle G. No 458. e/19 y 21.","1","nem akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Kuvait, Kuvait","Kuvaitváros, Hawalli Kormányzóság, Bayan kerület, 13. blokk 30. utca 381-es villa","8","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Laosz, Vientián","Royal Square Office Tower, 8. emelet 807, 20 Samsenthai Road, Nongduong Nua Village, Sikhottabong District, Vientiane, Lao PDR","6","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Lengyelország, Gdansk","Magyarország Főkonzulátusa, 80-864 Gdansk, Plac Porozumienia Gdańskiego 1.","22","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Lengyelország, Krakkó","Magyarország Főkonzulátusa, Krakkó, ul. Lubicz 17H, 31-503 Kraków","50","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Lengyelország, Varsó","Magyarország Nagykövetsége – Varsó, Stratos Office Center, ul. Księdza Ignacego Jana Skorupki 5., VI. Emelet, 00-546 Warszawa","73","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Lengyelország, Wroclaw","az Alkonzulátus épülete,ul. Łaciarska 4, 50-104 Wrocław.","16","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Lettország, Riga","Lettország, LV-1010 Riga, Baznicas iela 20/22, 4. emelet","10","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Libanon, Bejrút","Beirut, Sanayeh, Justinien street, BAC building, 9th floor","4","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Litvánia, Vilnius","Jogailos g. 4. Vilnius, 01402 Vilniaus m. sav., Verslo centras 2000 irodaház, 6. emelet","18","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Luxemburg, Luxembourg","Centre Culturel de Bonnevoie, 2 Rue des Ardennes, 1133 Bouneweg-Süd Luxembourg, Luxemburg","237","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Malajzia, Kuala Lumpur","Magyarország Kuala Lumpur-i Nagykövetsége, Level 11, Wisma Goldhill, 67, Jalan Raja Chulan, 50200 Kuala Lumpur, Malajzia","16","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Málta, Valletta","Ascencia Malta Business School, Málta, Floriana település, Vincenzo Dimech út 23.","124","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Marokkó, Rabat","17, Rue Ait Melloul Souissi, Rabat, Maroc 10000","22","nem akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Mexikó, Mexikóváros","Av. Montes Auvernia 310, Lomas de Chapultepec I Secc, Miguel Hidalgo, 11000 Ciudad de México","27","nem akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Moldova, Chisinau","Magyarország Nagykövetsége, Kisinyov, Bulevardul Stefan cel Mare 131.","5","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Mongólia, Ulánbátor","Magyarország Nagykövetsége, J.Sambuu str. 32., BLUEMON Center 6. emelet, Ulánbátor 14200, Mongólia","3","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Montenegró, Podgorica","81000 Podgorica, Kralja Nikole 104., Montenegró","8","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Nagy-Britannia és Észak-Írország, Edinburgh","Assembly Rooms, 54 George Street, Edinburgh EH2 2LR Nagy-Britannia","250","akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Nagy-Britannia és Észak-Írország, London","Novotel London West, 1 Shortlands Hammersmith, London W6 8DR (földszint, Chablis suite)","1624","akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Nagy-Britannia és Észak-Írország, Manchester","1 Portland Street, Manchester M1 3BE","343","akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Németország, Berlin","Berlini Magyar Nagykövetség épülete (10117 Berlin, Unter den Linden 76)","469","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Németország, Düsseldorf","Gerhart-Hauptmann-Haus Düsseldorf, Bismarckstraße 90, 40210 Düsseldorf","404","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Németország, München","Leonardo Hotel Munich City East, 39 Carl-Wery-Strasse, München, 81739, Deutschland","663","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Németország, Nürnberg","Magyarország Müncheni Főkonzulátusának Nürnbergi Konzuli Irodája , 90411 Nürnberg, Flughafenstraße 124.","221","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Németország, Stuttgart","Magyarország Főkonzulátusa Stuttgart, 70178 Stuttgart, Christophstr. 7., földszint","592","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Nigéria, Abuja","11 River Niger Street, Maitama, Abuja (FCT)","1","nem akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Norvégia, Oslo","Magyarország Nagykövetsége Oslo – Sophus Lies gate 3, 0264 Oslo, Norvégia","220","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Olaszország, Milánó","Olaszország, 20123 Milánó, Via Fieno 3. IV. emelet","159","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Olaszország, Róma","Collegium Hungaricum Róma, Via Giulia 1, 00186  Roma","167","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Omán, Maszkat","Muscat, Al-Qurum, Al-Rawaq Building, 2nd Floor, Unit No. 209, Sultanate of Oman","13","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Oroszország, Jekatyerinburg","620075 Jekatyerinburg, Gogol utca 15, I. emelet","5","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Oroszország, Kazan","Kazan, 420107, Szuvár Pláza Üzletközpont, Szpartakovszkaja u. 6. (5. emelet)","4","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Oroszország, Moszkva","115127 Moszkva, Moszfilmovszkaja u. 62.","27","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Oroszország, Szentpétervár","Magyarország Főkonzulátusa Szentpétervár, 191025 Szentpétervár, Marata u. 15.","6","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Örményország, Jereván","Magyarország Nagykövetsége Jereván, 59 Marshal Baghramyan ave, 4. emelet","3","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Pakisztán, Iszlámábád","Magyarország Nagykövetsége, Iszlámábád, House No. 12., Margalla Road, F-6/3, Islamabad","7","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Palesztina, Ramallah","Representative Office of Hungary, Ramallah – Al-Bireh, Municipality street 34. Al Watania Tower Building","0","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Panama, Panamaváros","Panamaváros, Oceania Business Plaza Torre 1000, 30-D, C. Isaac Hanono Missri, Panamá, Provincia de Panamá","8","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Peru, Lima","Avenida Jorge Basadre 1580, San Isidro, Lima","12","akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Portugália, Lisszabon","Lisszabon 1300-516, Calçada Santo Amaro 85.","178","nem akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Románia, Bukarest","Magyarország Nagykövetsége, Bukarest, Str. Jean Louis Calderon Nr. 63-65., Sector 2 Bukarest 020034","28","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Románia, Csíkszereda","Sapientia Erdélyi Magyar Tudományegyetem, Csíkszeredai Kar, Csíkszereda 530104, Szabadság tér, 1.","294","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Románia, Kolozsvár","400113 Kolozsvár, Főtér 23. (Cluj-Napoca, Piata Unirii nr. 23.)","85","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ruanda, Kigali","Magyarország Nairobi Nagykövetségének Kigali Irodája, Kigali, Kiyovu, KN 78 Str","3","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Spanyolország, Barcelona","Carrer del Pintor Fortuny, 4-6, 08001 Barcelona","313","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Spanyolország, Madrid","Calle Fortuny, 6, Planta 4, Chamberí, 28010 Madrid","230","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Spanyolország, Malaga","Hotel NH Málaga, Calle San Jacinto, 2, Distrito Centro, 29007 Málaga","191","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Svájc, Bern","Kongresszentrum Allresto Bern, Effingerstrasse 20, 3008 Bern","725","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Svájc, Genf","Rue du Grand-Pré 66. (6. emelet), CH-1202 Genf","117","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Svédország, Stockholm","Magyarország Nagykövetsége, Dag Hammarskjölds väg 10, 115 27 Stockholm","277","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Szaúd-Arábia, Rijád","Magyarország Nagykövetsége, Riyadh 11693, King Salman (former Al Waha) District, Ahmad At Tunisi Str. 23., Szaúd-Arábia","14","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Szerbia, Belgrád","Magyarország Nagykövetsége, 11000 Belgrád, Krunska 72.","9","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Szerbia, Szabadka","Magyarország Főkonzulátusa, 24000 Subotica (Szabadka), Đure Đakovića 1-3","73","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Szingapúr, Szingapúr","Embassy of Hungary, 250 North Bridge Road #29-01 Raffles City Tower, Singapore 179101","59","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Szlovákia, Besztercebánya","Magyarország Pozsonyi Nagykövetségének Besztercebányai Alkonzulátusa, 974 01 Besztercebánya, Horná 5.","2","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Szlovákia, Kassa","Magyarország Főkonzulátusa, 04001 Kosice, Hlavná 72","4","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Szlovákia, Pozsony","Magyarország Nagykövetsége, Pozsony - 81106 Bratislava, Stefánikova 1","13","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Szlovénia, Lendva","Magyarország Főkonzulátusa, Fő utca 30. 9220 Lendva, Szlovénia","2","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Szlovénia, Ljubljana","Magyarország Nagykövetsége, 1210 Ljubljana-Šentvid, Ulica Konrada Babnika 5.","40","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Tanzánia, Dar Es-Salaam","Magyarország Nairobi Nagykövetségének Dar es-Salaami Irodája, 2nd floor, Peninsula House, Toure Dr., Masaki","1","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Thaiföld, Bangkok","Park Ventures Ecoplex 14th Floor, 57 Thanon Witthayu (Wireless Road), Lumpini, Pathumwan, Bangkok 10330","89","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Törökország, Ankara","Magyarország Nagykövetsége, Ankara, 06680 Çankaya, Kavaklıdere, Remzi Oğuz Arık Mahallesi, Paris Caddesi No. 43/2","16","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Törökország, Isztambul","POLAT OFIS B Blok, İmrahor Cad. No: 23 Gürsel Mah., Kağıthane – 34400 ISTANBUL;","44","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Tunézia, Tunisz","Magyarország Nagykövetsége, 12 Rue Achtart, Nord Hilton, 1082 Tunis","11","nem akadálymentes","2026. április 12., 06:00 - 18:00","2026. április 2., 16:00 (CET)"
"Uganda, Kampala","Acacia Mall Business Centre, 4th Floor, office No. 322, Cooper Road, off Acacia Avenue, Plot 14-18, Kololo, Kampala","0","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Új-Zéland, Wellington","Level 6, 101 Lambton Quay, Wellington –Új-Zéland","29","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ukrajna, Beregszász","Ukrajna 90200 Beregszász, Bogdán Hmelynickij u.53.","44","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ukrajna, Kijev","Magyarország Nagykövetsége, 04053, Kyiv, vul. Reitarska 33. (Посольство Угорщини Київ, вул. Рейтарська 33. м. Київ, 04053)","6","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Ukrajna, Ungvár","Magyarország Főkonzulátusa, 88000, Ungvár, Pravoszláv rkp. 12., Ukrajna","15","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Uruguay, Montevideo","Cooper 2133, 11500 Montevideo, Uruguay","0","nem akadálymentes","2026. április 11., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Üzbegisztán, Taskent","Magyarország Nagykövetsége, Taskent, 100057 Taskent, Bogiravon u. 63-65.,","3","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Vietnám, Hanoi","Magyarország Hanoi Nagykövetsége, 28 Thanh Niên, Tay Ho, Hanoi, Vietnám, (Hanoi Lake View épület)","52","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Vietnám, Ho Si Minh-város","Magyarország Főkonzulátusa, 21st Floor, LIM Tower, 9-11 Ton Duc Thang Street, Sai Gon Ward, Ho Chi Minh City 700000, Vietnam","20","akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"Zambia, Lusaka","Magyaroszág Pretoriai Nagykövetségének Irodája, Lusaka 5216 Independence Ave 33379, Lusaka, Zambia","1","nem akadálymentes","2026. április 12., 06:00 - 19:00","2026. április 2., 16:00 (CET)"
"""

def geocode_address(address):
    # Use Nominatim API for geocoding
    # We add a delay to respect the usage policy
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "KulkepviseletiSzavazasWebapp/1.0"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            results = response.json()
            if results:
                return float(results[0]["lat"]), float(results[0]["lon"])
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None, None

def main():
    reader = csv.DictReader(data_str.strip().splitlines())
    results = []
    
    for row in reader:
        city_country = row["Ország, település"]
        address = row["Külképviselet címe"]
        
        # Try to geocode the address first, if fails try city_country
        print(f"Geocoding: {address} ({city_country})")
        lat, lon = geocode_address(address)
        if lat is None:
            lat, lon = geocode_address(city_country)
            
        row["lat"] = lat
        row["lon"] = lon
        results.append(row)
        
        # Sleep to be nice to OSM
        time.sleep(1.1)
        
    # Write to data.js
    with open("data.js", "w") as f:
        f.write("const KULKEPVISELETEK = ")
        json.dump(results, f, indent=2, ensure_ascii=False)
        f.write(";")

if __name__ == "__main__":
    main()
