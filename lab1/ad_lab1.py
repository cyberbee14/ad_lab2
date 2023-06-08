import requests
import pandas as pd
import glob
import os

def download_all_files(directory):
    if(not os.path.exists(directory)):
        print("Create dir...")
        os.makedirs(directory)
    else:
        print("Dir already exists.")
    
    if(len(os.listdir(directory))):
        print("Files already exist.")
    else:
        print("Download files...")
        for index in range(1, 29):
            print("Downloading for ID:{}".format(index))
            filename = 'NOA_ID_{}.csv'.format(index)
            url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean'.format(index)
            download_file(url,directory+"/"+filename)


def download_file(url,destination):
    response = requests.get(url)
    response.raise_for_status()
    with open(destination,'wb') as file:
        file.write(response.content)

def collect_dataframe_from_files(directory):
    headers = ['year', 'week', ' SMN', 'SMT', 'VCI', 'TCI', ' VHI<br>', 'empty']  
    clear_headers = ['year', 'week', ' SMN', 'SMT', 'VCI', 'TCI', ' VHI<br>']  

    dir_files = glob.glob(directory+"/" + "NOA_ID_*.csv") 
    dir_files = sorted(dir_files, key=lambda x: int(x[-6:-4].strip('_'))) 

    li = []
    i = 1

    for filename in dir_files: 
        df = pd.read_csv(filename, index_col=None, header=1, names=headers, usecols=clear_headers)
        df = df.rename(columns={' SMN': 'SMN', ' VHI<br>': 'VHI'}) 
        df = df.drop(df.loc[df['VHI'] == -1].index) 
        df = df.dropna()

        df['area'] = i 

        li.append(df)
        i += 1

    frame = pd.concat(li, axis=0, ignore_index=True) 
    frame["year"].replace({"<tt><pre>1982": "1982"}, inplace=True)
    return frame

def change_indexes(frame):
    indexes = ["22", "24", "23", "25", "3", "4", "8", "19", "20", "21", "9", "26", "10", "11",
                            "12", "13", "14", "15", "16", "27", "17", "18", "6", "1", "2", "7", "5"]
    old = 1
    for new in indexes:
        frame["area"].replace({old: new}, inplace=True)  
        old += 1
    frame.to_csv("FULL_NOAA_IDobl_UKR_ALL.csv")    
    return frame

def find_hvi_extremums(frame, area_index, year):
    # Отримання ряду vhi для area_index і year
    frame_search = frame[(frame["area"] == area_index) & (frame["year"] == year)]['VHI']
    llist = []
    for i in frame_search:
        llist.append(i)
    print(f"Here are VHI for province **{area_index}** in {year}")
    print(llist)
    print("================================")

    max_v = frame[(frame.year.astype(str) == str(year)) & (frame.area == area_index)]['VHI'].max()
    min_v = frame[(frame.year.astype(str) == str(year)) & (frame.area == area_index)]['VHI'].min()
    print(f'The MAX value is: {max_v}')
    print(f'The MIN value is: {min_v}')
    print("================================")
    return

def find_extreme_mid_weeks(frame,area_index,percent):
    severity_type = {'1':'extreme','2':'mild'}
    severity = input("Choose type of searching:\n1:*extreme*\t2:*mild*: ")
    if severity == '1':  
        severity_real = 35
    elif severity == '2':
        severity_real = 60
    else:
        print('Wrong severity')
        return

    output = []
    all_possible_years = frame.year.unique()[:]  
    frame_search = frame[(frame['area'] == area_index)]  
    llist = []
    for i in frame_search["VHI"]:
        llist.append(i)
    print(f"Here are drought VHI for province **{area_index}** in all years")
    print(llist)
    print()

    for year in all_possible_years:
        current_year = frame_search[(frame_search['year'] == year)]  
        all_weeks = len(current_year.index)  

        if severity_real == 35:
            df_drought = current_year[(current_year.VHI <= severity_real)] 
        else:
            df_drought = current_year[(current_year.VHI >= severity_real)]  

        extreme_weeks = len(df_drought.index)  
        percentage = extreme_weeks / all_weeks * 100  
        if percentage >= percent:
            output.append(year)
    print(f"Years with the {severity_type[severity]} droughts with more than {percent}% area: ")
    print(output)

directory = 'csv_files_dir'
download_all_files(directory)
frame = collect_dataframe_from_files(directory)
frame = change_indexes(frame)
provinceID = input("Enter the region index: ")
year = input("Enter the year: ")
find_hvi_extremums(frame,provinceID,year)
percent = float(input("Type percent for searching droughts in province({}): ".format(provinceID)))
find_extreme_mid_weeks(frame,provinceID,percent)



