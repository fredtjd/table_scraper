import requests, csv, re
from bs4 import BeautifulSoup as bs
import pandas
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from df2gspread import df2gspread as d2g

l_ep="https://www.bbc.co.uk/sport/rugby-union/english-premiership/table"
l_6n="https://www.bbc.co.uk/sport/rugby-union/six-nations/table"
l_t14="https://www.bbc.co.uk/sport/rugby-union/top-14/table"
l_rc="https://www.bbc.co.uk/sport/rugby-union/rugby-championship/table"
l_p14="https://www.bbc.co.uk/sport/rugby-union/pro-tournament/table" #2 conferences x 7
l_sr="https://www.bbc.co.uk/sport/rugby-union/super-rugby/table" #3 pools x 5
l_rwc="https://www.bbc.co.uk/sport/rugby-union/world-cup/table" #4 pools x 6
l_champcup="https://www.bbc.co.uk/sport/rugby-union/european-cup/table" #5 pools x 4
l_challengecup="https://www.bbc.co.uk/sport/rugby-union/european-challenge-cup/table" #5 pools x 4
l_engchamp="https://www.bbc.co.uk/sport/rugby-union/the-english-championship/table"
l_prod2=""

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
gc = gspread.authorize(credentials)
spreadsheet_key = '1l7ZXUxE7Ebm433mRDeEM_h5afLkpFzM6W8nEnnc_520'

def league_rip(league):
    page = requests.get(league)
    source = page.content.decode('ISO-8859-1')
    soup = bs(page.content, 'html.parser')
    z = re.search('data-reactid="(.*?)"', source)
    id_class = z.group(0).strip()[14:-1]
    if league == l_ep:
        teams = 12
        out_name = "english_premiership"
        conf = 0
    elif league == l_6n:
        teams = 6
        out_name = "six_nations"
        conf = 0
    elif league == l_t14:
        teams = 14
        out_name = "top_14"
        conf = 0
    elif league == l_p14:
        teams = 7
        conf = 1
        out_name= "pro_14"
    elif league == l_rwc:
        teams = 5
        conf = 3
        out_name="rwc"
    elif league == l_sr:
        teams = 5
        conf = 2
        out_name="super_rugby"
    elif league == l_champcup:
        teams = 4
        conf = 4
        out_name= "champions_cup"
    elif league == l_challengecup:
        teams = 4
        conf = 4
        out_name = "challenge_cup"
    elif league == l_engchamp:
        teams = 12
        conf = 0
        out_name = "english_championship"
    else:
        pass
    if conf == 0:
        rows = []
        #rows.append(['Rank', 'Team', 'Played', 'Won', 'Lost', 'Drawn', 'PD', 'BP', 'Points'])
        for t in range(0,teams):
            dict_t = {'data-reactid': id_class + ".2.0.0.0.0.$0.1.1.$row-" + str(t) + ".$td-1.0.0"}
            dict_p = {'data-reactid': id_class + ".2.0.0.0.0.$0.1.1.$row-" + str(t) + ".$td-2.1"}
            dict_w = {'data-reactid': id_class + ".2.0.0.0.0.$0.1.1.$row-" + str(t) + ".$td-3.1"}
            dict_l = {'data-reactid': id_class + ".2.0.0.0.0.$0.1.1.$row-" + str(t) + ".$td-4.1"}
            dict_d = {'data-reactid': id_class + ".2.0.0.0.0.$0.1.1.$row-" + str(t) + ".$td-5.1"}
            dict_pd = {'data-reactid': id_class + ".2.0.0.0.0.$0.1.1.$row-" + str(t) + ".$td-8.1"}
            dict_bp = {'data-reactid': id_class + ".2.0.0.0.0.$0.1.1.$row-" + str(t) + ".$td-9.1"}
            dict_pts = {'data-reactid': id_class + ".2.0.0.0.0.$0.1.1.$row-" + str(t) + ".$td-10.1"}
            #rank = t + 1
            team = soup.find('span', dict_t).get_text()
            played = soup.find('span', dict_p).get_text()
            won = soup.find('span', dict_w).get_text()
            lost = soup.find('span', dict_l).get_text()
            drawn = soup.find('span', dict_d).get_text()
            pd = soup.find('span', dict_pd).get_text()
            bp = soup.find('span', dict_bp).get_text()
            points = soup.find('span', dict_pts).get_text()
            rows.append([team, played, won, lost, drawn, pd, bp, points])
        df = pandas.DataFrame(rows, columns=['Team', 'Played', 'W', 'L', 'D', 'PD', 'BP', 'Points'])
        df.index += 1
        wks_name = out_name
        d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
        #with open(out_folder + out_name + ".csv",'w', newline='')  as f_output:
        #    csv_output = csv.writer(f_output)
        #    csv_output.writerows(rows)
    elif conf >= 1:
        for c in range(0,conf+1):
            rows = []
            #rows.append(['Rank', 'Team', 'Played', 'Won', 'Lost', 'Drawn', 'PD', 'BP', 'Points'])
            for t in range(0,teams):
                dict_t = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-1.0.0"}
                dict_p = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-2.1"}
                dict_w = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-3.1"}
                dict_l = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-4.1"}
                dict_d = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-5.1"}
                dict_pd = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-8.1"}
                dict_bp = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-9.1"}
                dict_pts = {'data-reactid': id_class + ".2.0.0.0.0.$" + str(c) + ".1.1.$row-" + str(t) + ".$td-10.1"}
                #rank = t + 1
                team = soup.find('span', dict_t).get_text()
                played = soup.find('span', dict_p).get_text()
                won = soup.find('span', dict_w).get_text()
                lost = soup.find('span', dict_l).get_text()
                drawn = soup.find('span', dict_d).get_text()
                pd = soup.find('span', dict_pd).get_text()
                bp = soup.find('span', dict_bp).get_text()
                points = soup.find('span', dict_pts).get_text()
                rows.append([team, played, won, lost, drawn, pd, bp, points])
            df = pandas.DataFrame(rows, columns=['Team', 'Played', 'W', 'L', 'D', 'PD', 'BP', 'Points'])
            df.index += 1
            wks_name = out_name + "_" + str(c)
            d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
            #with open(out_folder + out_name + "_" + str(c) + ".csv",'w', newline='')  as f_output:
            #    csv_output = csv.writer(f_output)
            #    csv_output.writerows(rows)
    else:
        pass

league_rip(l_ep)
league_rip(l_t14)
league_rip(l_p14)
league_rip(l_champcup)
league_rip(l_challengecup)
league_rip(l_6n)
league_rip(l_sr)
league_rip(l_rwc)

