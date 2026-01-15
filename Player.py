import increment
import time
from config import SPREADSHEET
from StringBuilder import parse_first_column


class player:
    init_elo = -1
    placement = -1
    new_elo = -1
    column = ""
    Time_Line = ""
    name = ""

    def __init__(self, name, placement, sheet, settings, time_line_range):
        self.placement = placement
        self.name = name.strip()
        self.set_column(sheet, settings, time_line_range)

    def game(self, opponent):
        expected = 1/(pow(10, ((int(opponent.init_elo) - int(self.init_elo)) / 400)) + 1)
        if self.placement < opponent.placement:
            self.new_elo = int(self.new_elo) + 32 * (1 - expected)
        else:
            self.new_elo = int(self.new_elo) + 32 * (0 - expected)


    def set_init_elo(self, init_elo):
        self.init_elo = init_elo
        self.new_elo = init_elo

    def set_column(self, sheet, settings, time_line_range):
        time.sleep(1)
        timeline_data = sheet.values().get(spreadsheetId=SPREADSHEET, range=time_line_range).execute()
        timeline_array = timeline_data.get("values", [[]])[0]
        time.sleep(1)
        column_data = sheet.values().get(spreadsheetId=SPREADSHEET, range=settings[5] + "!" + settings[4] + ":" +
                                                                  settings[4]).execute()
        column_array = column_data.get("values", [[]])[0]

        search_position = parse_first_column(time_line_range)


        for column in timeline_array:
            if column.strip() == self.name:
                self.Time_Line = search_position
                break;
            search_position = increment.incr_str(search_position)

        search_position = "A"
        for column in column_array:
            if column.strip() == self.name:
                self.column = search_position
                break;
            search_position = increment.incr_str(search_position)



    def getcolumn(self):
        return self.column

    def get_Time_Line_column(self):
        return self.Time_Line

    def getNewElo(self):
        return self.new_elo