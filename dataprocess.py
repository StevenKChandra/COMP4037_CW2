import os
import pandas as pd

datagroups = os.listdir("exposures")
datagroups = [groups.split("_")[1] for groups in datagroups]

countries = os.listdir(f"exposures/exposures_{datagroups[0]}")
countries = [country.split(".")[0] for country in countries]

main_savedir = "compiled"
if not os.path.exists(main_savedir): os.makedirs(main_savedir)

for group in datagroups:
    if not os.path.exists(f"{main_savedir}/{group}"): os.makedirs(f"{main_savedir}/{group}")
    for country in countries:
        exposures = [line.rstrip().split(",") for line in open(f"exposures/Exposures_{group}/{country}.Exposures_{group}.csv", "r")]
        deaths = [line.rstrip().split(",") for line in open(f"deaths/Deaths_{group}/{country}.Deaths_{group}.csv", "r")]
        death_rates = [line.rstrip().split(",") for line in open(f"death_rates/Mx_{group}/{country}.Mx_{group}.csv", "r")]

        compiledcsv = "Year,Age,Deaths Female,Deaths Male,Deaths Total,Exposures Female,Exposures Male,Exposures Total,Death_rates Female,Death_Rates Male,Death_Rates Total\n"

        for linenum in range(len(exposures))[1:]:
            exposures[linenum] = [i if i != "." else "0" for i in exposures[linenum]]
            deaths[linenum] = [i if i != "." else "0" for i in deaths[linenum]]
            death_rates[linenum] = [i  if i != "." else "0" for i in death_rates[linenum]]

            compiledcsv += deaths[linenum][0] + "," + deaths[linenum][1] + "," + deaths[linenum][2] + "," + deaths[linenum][3] + "," + deaths[linenum][4] + "," + exposures[linenum][2] + "," + exposures[linenum][3] + "," + exposures[linenum][4] + "," + death_rates[linenum][2] + "," + death_rates[linenum][3] + "," + death_rates[linenum][4] + "\n"
        
        savefile = open(f"{main_savedir}/{group}/{country}_{group}.csv", "w")
        savefile.write(compiledcsv[:-2])
        savefile.close()
        
country_table = ['Ireland', 'England & Wales Civilian', 'Norway', 'Sweden', 'Denmark', 'France', 'Belgium', 'Netherlands', 'Germany', 'Switzerland', 'Austria', 'Czechia', 'Slovakia', 'Poland']
alias_table = ['IRL', 'GBRCENW', 'NOR', 'SWE', 'DNK', 'FRACNP', 'BEL', 'NLD', 'DEUTNP', 'CHE', 'AUT', 'CZE', 'SVK', 'POL']

years = range(2000, 2020)

countries = [csv[:-4].split("_")[0] for csv in os.listdir() if csv[-4:] == ".csv"]
for country in [csv for csv in os.listdir() if csv[-4:] == ".csv"]:
    globals() [country[:(country.find("1")-1)]] = pd.read_csv(country)



rows_summary = []
rows_ByAge = []

for year in years:
    for country in countries:
        if country not in alias_table: continue

        row_summary = [country_table[alias_table.index(country)], year]

        if year in globals() [country]["Year"]:

            for row in globals() [country][globals() [country]["Year"]==year].values.tolist():
                row_ByAge = [country_table[alias_table.index(country)]]
                for value in row:
                    row_ByAge.append(value)
                rows_ByAge.append(row_ByAge)

            for col in globals() [country].columns[2:-3]:
                row_summary.append(sum(globals() [country][col][globals() [country]["Year"]==year]))

            if row_summary[2] == 0:row_summary[2] = None
            if row_summary [5] == 0:row_summary[5] = None            
            if row_summary[3] == 0:row_summary[3] = None
            if row_summary [6] == 0:row_summary[6] = None
            if row_summary[4] == 0:row_summary[4] = None
            if row_summary [7] == 0:row_summary[7] = None

            if row_summary[2] == None or row_summary [5] == None:row_summary.append(None)
            else:row_summary.append(row_summary[2]/row_summary[5])
            if row_summary[2] == None or row_summary [5] == None:row_summary.append(None)
            else:row_summary.append(row_summary[3]/row_summary[6])
            if row_summary[4] == None or row_summary [7] == None:row_summary.append(None)
            else:row_summary.append(row_summary[4]/row_summary[7])

        if row_summary[2:] == [None for i in range (9)]:continue
        rows_summary.append(row_summary)


df_ByAge = pd.DataFrame (rows_ByAge, columns=['Country','Year','Age','Deaths Female','Deaths Male','Deaths Total','Exposures Female','Exposures Male','Exposures Total','Death_rates Female','Death_Rates Male','Death_Rates Total'])
df_ByAge.to_csv("Data_ByAge.csv", index=False, header=True)

df_summary = pd.DataFrame(rows_summary, columns=['Country','Year','Deaths Female','Deaths Male','Deaths Total','Exposures Female','Exposures Male','Exposures Total','Death_rates Female','Death_Rates Male','Death_Rates Total'])
df_summary.to_csv("Data_Summary.csv", index=False, header=True)
