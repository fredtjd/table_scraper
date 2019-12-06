import requests, csv, re, yaml, pandas, gspread
from bs4 import BeautifulSoup as bs
from oauth2client.service_account import ServiceAccountCredentials 
from df2gspread import df2gspread as d2g

with open("config.yaml", "r") as f:
    cfg = yaml.load(f)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
gc = gspread.authorize(credentials)
spreadsheet_key = '1l7ZXUxE7Ebm433mRDeEM_h5afLkpFzM6W8nEnnc_520'

def league_rip(league):
    page = requests.get(cfg[league]['url'])
    source = page.content.decode('ISO-8859-1')
    soup = bs(page.content, 'html.parser')
    z = re.search('data-reactid="(.*?)"', source)
    id_class = z.group(0).strip()[14:-1] #workaround to get data-reactid of current page as it changes
    for c in range(cfg[league]['pools']):
        l_table = []
        for t in range(cfg[league]['teams']):
            dict_t = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-1.0.0"}
            dict_p = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-2.1"}
            dict_w = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-3.1"}
            dict_l = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-4.1"}
            dict_d = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-5.1"}
            dict_pd = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-8.1"}
            dict_bp = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-9.1"}
            dict_pts = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-10.1"}
            team = soup.find('span', dict_t).get_text()
            played = soup.find('span', dict_p).get_text()
            won = soup.find('span', dict_w).get_text()
            lost = soup.find('span', dict_l).get_text()
            drawn = soup.find('span', dict_d).get_text()
            pd = soup.find('span', dict_pd).get_text()
            bp = soup.find('span', dict_bp).get_text()
            points = soup.find('span', dict_pts).get_text()
            l_table.append([team, played, won, lost, drawn, pd, bp, points])
        df = pandas.DataFrame(l_table, columns=['Team', 'Played', 'W', 'L', 'D', 'PD', 'BP', 'Points'])
        df.index += 1
        if cfg[league]['pools'] == 0:
            wks_name = cfg[league]['out_name']
        else: 
            wks_name = cfg[league]['out_name'] + "_" + chr(c + 97)
        print(df)
        d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, clean=False)

league_rip("engprem")
league_rip("top14")
league_rip("rugbychamp")
league_rip("pro14")
league_rip("champcup")
league_rip("challengecup")
league_rip("engchamp")
league_rip("superrugby")
league_rip("worldcup")
league_rip("sixnations")
