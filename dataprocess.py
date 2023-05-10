import os
import pandas as pd

### This part of the code is to compile death, exposures, and death rates data of each country
# find the directories where text data is stored
datagroups = os.listdir("exposures")
datagroups = [groups.split("_")[1] for groups in datagroups]

countries = os.listdir(f"exposures/exposures_{datagroups[0]}")
countries = [country.split(".")[0] for country in countries]

# make a new directory to save the data
main_savedir = "compiled"
if not os.path.exists(main_savedir): os.makedirs(main_savedir)

for group in datagroups:
    if not os.path.exists(f"{main_savedir}/{group}"): os.makedirs(f"{main_savedir}/{group}")
    for country in countries:
        # open the exposures, death, and death rates file
        exposures = [line.rstrip().split(",") for line in open(f"exposures/Exposures_{group}/{country}.Exposures_{group}.csv", "r")]
        deaths = [line.rstrip().split(",") for line in open(f"deaths/Deaths_{group}/{country}.Deaths_{group}.csv", "r")]
        death_rates = [line.rstrip().split(",") for line in open(f"death_rates/Mx_{group}/{country}.Mx_{group}.csv", "r")]

        compiledcsv = "Year,Age,Deaths Female,Deaths Male,Deaths Total,Exposures Female,Exposures Male,Exposures Total,Death_rates Female,Death_Rates Male,Death_Rates Total\n"
        
        # check if there is no data, replace with 0
        for linenum in range(len(exposures))[1:]:
            exposures[linenum] = [i if i != "." else "0" for i in exposures[linenum]]
            deaths[linenum] = [i if i != "." else "0" for i in deaths[linenum]]
            death_rates[linenum] = [i  if i != "." else "0" for i in death_rates[linenum]]

            compiledcsv += deaths[linenum][0] + "," + deaths[linenum][1] + "," + deaths[linenum][2] + "," + deaths[linenum][3] + "," + deaths[linenum][4] + "," + exposures[linenum][2] + "," + exposures[linenum][3] + "," + exposures[linenum][4] + "," + death_rates[linenum][2] + "," + death_rates[linenum][3] + "," + death_rates[linenum][4] + "\n"
        
        savefile = open(f"{main_savedir}/{group}/{country}_{group}.csv", "w")
        savefile.write(compiledcsv[:-2])
        savefile.close()

### This part of the code is to merge the compiled data from the code above into one table, while also calculating overall yearly death rates and saving them into a single table
### the formula for counting death rates is sum(death)/sum(exposure) for each year (https://www.mortality.org/Project/Overview#:~:text=Death%20rates%20are%20always%20a,risk%20in%20the%20same%20interval)
# list the country and aliases
country_table = ['Ireland', 'England & Wales Civilian', 'Norway', 'Sweden', 'Denmark', 'France', 'Belgium', 'Netherlands', 'Germany', 'Switzerland', 'Austria', 'Czechia', 'Slovakia', 'Poland']
alias_table = ['IRL', 'GBRCENW', 'NOR', 'SWE', 'DNK', 'FRACNP', 'BEL', 'NLD', 'DEUTNP', 'CHE', 'AUT', 'CZE', 'SVK', 'POL']

# list the years
years = range(2000, 2020)

# open the compiled file of each countries and save them as variables
countries = [csv[:-4].split("_")[0] for csv in os.listdir() if csv[-4:] == ".csv"]
for country in [csv for csv in os.listdir() if csv[-4:] == ".csv"]:
    globals() [country[:(country.find("1")-1)]] = pd.read_csv(country)

rows_summary = []
rows_ByAge = []

for year in years:
    for country in countries:
        # only process listed countries
        if country not in alias_table: continue
        
        # create a placeholder for summary data
        row_summary = [country_table[alias_table.index(country)], year]

        # only process listed years
        if year in globals() [country]["Year"]:
            # iterate through the data and append it to placeholder
            for row in globals() [country][globals() [country]["Year"]==year].values.tolist():
                # create a placeholder for age distribution data
                row_ByAge = [country_table[alias_table.index(country)]]
                for value in row:
                    row_ByAge.append(value)
                rows_ByAge.append(row_ByAge)
            
            # iterate through the data, summing the death and exposures for each years
            for col in globals() [country].columns[2:-3]:
                row_summary.append(sum(globals() [country][col][globals() [country]["Year"]==year]))
            
            # check if values are 0, change it to none
            if row_summary[2] == 0:row_summary[2] = None
            if row_summary [5] == 0:row_summary[5] = None            
            if row_summary[3] == 0:row_summary[3] = None
            if row_summary [6] == 0:row_summary[6] = None
            if row_summary[4] == 0:row_summary[4] = None
            if row_summary [7] == 0:row_summary[7] = None

            # if values are 0, dont do division if one of them are 0, fill death rates with none
            if row_summary[2] == None or row_summary [5] == None:row_summary.append(None)
            else:row_summary.append(row_summary[2]/row_summary[5])
            if row_summary[2] == None or row_summary [5] == None:row_summary.append(None)
            else:row_summary.append(row_summary[3]/row_summary[6])
            if row_summary[4] == None or row_summary [7] == None:row_summary.append(None)
            else:row_summary.append(row_summary[4]/row_summary[7])
        
        # append the data, if all is none then no need to append
        if row_summary[2:] == [None for i in range (9)]:continue
        rows_summary.append(row_summary)

# save the age distribution data
df_ByAge = pd.DataFrame (rows_ByAge, columns=['Country','Year','Age','Deaths Female','Deaths Male','Deaths Total','Exposures Female','Exposures Male','Exposures Total','Death_rates Female','Death_Rates Male','Death_Rates Total'])
df_ByAge.to_csv("Data_ByAge.csv", index=False, header=True)

# save the summary data
df_summary = pd.DataFrame(rows_summary, columns=['Country','Year','Deaths Female','Deaths Male','Deaths Total','Exposures Female','Exposures Male','Exposures Total','Death_rates Female','Death_Rates Male','Death_Rates Total'])
df_summary.to_csv("Data_Summary.csv", index=False, header=True)
