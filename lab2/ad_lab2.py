from spyre import server
import pandas as pd


class StockExample(server.App):
    title = "NOAA data dropdown"

    region_mapping = {
            "1": "Вінничини",
            "2": "Волині",
            "3": "Дніпропетровщини",
            "4": "Донеччини",
            "5": "Житомирщини",
            "6": "Закарпаття",
            "7": "Запоріжжя",
            "8": "Івано-Франківщини",
            "9": "Київщини",
            "10": "Кіровоградщини",
            "11": "Луганщини",
            "12": "Львівщини",
            "13": "Миколаївщини",
            "14": "Одещини",
            "15": "Полтавщини",
            "16": "Рівенщини",
            "17": "Сумщини",
            "18": "Тернопільщини",
            "19": "Харківщини",
            "20": "Херсонщини",
            "21": "Хмельницька",
            "22": "Черкащини",
            "23": "Чернівецька",
            "24": "Чернігівщини",
            "25": "Криму"
        }

    inputs = [
        {
            "type": "dropdown",
            "label": "Оберіть тип індексу для графіку",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}
            ],
            "key": "data_type",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Оберіть область України:",
            "options": [
                {"label": "Вінницька", "value": "1"},
                {"label": "Волинська", "value": "2"},
                {"label": "Дніпропетровська", "value": "3"},
                {"label": "Донецька", "value": "4"},
                {"label": "Житомирська", "value": "5"},
                {"label": "Закарпатська", "value": "6"},
                {"label": "Запорізька", "value": "7"},
                {"label": "Івано-Франківська", "value": "8"},
                {"label": "Київська", "value": "9"},
                {"label": "Кіровоградська", "value": "10"},
                {"label": "Луганська", "value": "11"},
                {"label": "Львівська", "value": "12"},
                {"label": "Миколаївська", "value": "13"},
                {"label": "Одеська", "value": "14"},
                {"label": "Полтавська", "value": "15"},
                {"label": "Рівенська", "value": "16"},
                {"label": "Сумська", "value": "17"},
                {"label": "Тернопільська", "value": "18"},
                {"label": "Харківська", "value": "19"},
                {"label": "Херсонська", "value": "20"},
                {"label": "Хмельницька", "value": "21"},
                {"label": "Черкаська", "value": "22"},
                {"label": "Чернівецька", "value": "23"},
                {"label": "Чернігівська", "value": "24"},
                {"label": "Крим", "value": "25"}
            ],
            "key": "region",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "Оберіть інтервал тижнів:",
            "key": "weeks",
            "value": "9-10",
            "action_id": "update_data"
        },

        {
            "type":'slider',
            "label": 'Оберіть рік:',
            "min" : 1981,
            "max" : 2023,
            "key": 'year',
            "action_id" : "update_data"
            
        },
    ]

    controls = [{"type": "hidden", "id": "update_data"},{"type":"button","id":"update_data","label":'Submit'}]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]
    def getData(self, params):
        region = params['region']
        year = params['year']
        weeks = params['weeks']
        
        df = pd.read_csv("../lab1/FULL_NOAA_IDobl_UKR_ALL.csv")
        start_week, end_week = map(int, weeks.split('-'))
        frame = df[(df.area.astype(str)==str(region))&(df['week'] >= start_week) & (df['week'] <= end_week) & (df['year'] == int(year))]
        #df['Date'] = pd.to_datetime(df['Date'],format='%Y%m%d')
        frame = frame.drop('area',axis=1).drop('year',axis=1).drop(frame.columns[0],axis=1)
        return frame

    def getPlot(self, params):
        df = self.getData(params)
        df.set_index(df.columns[0])
        plt_obj = df.plot(y=params['data_type'],x='week',legend=False)
        plt_obj.set_ylabel(params['data_type'])
        plt_obj.set_title("Графік для "+self.region_mapping[params['region']]+ " за {} рік в інтервалі тижнів {}".format(params['year'],params['weeks']))
        fig = plt_obj.get_figure()
        return fig

app = StockExample()
app.launch(port=9090)
