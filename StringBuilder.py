from config import SPREADSHEET, num_players
from increment import incr_str
import re


def get_timeline(sheet, timeline_name, row):
  start_position = ''
  column_array = sheet.values().get(spreadsheetId=SPREADSHEET, range = (timeline_name + "!" + str(row) + ":" + str(row))).execute()
  columns_list = column_array.get("values", [[]])[0]
  search_position = "A"

  for i, column in enumerate(columns_list):
    if column == "Timeline":
        start_position = search_position
        start_position = incr_str(start_position)
    if column == '' and start_position != '':
      break
    if start_position != '' and column != "Timeline":
        num_players["count"] += 1


    search_position = incr_str(search_position)
    if i != len(columns_list) - 1:
        end_position = search_position

  return [start_position, end_position]

def parse_first_column(range_str):
    # "Sheet1!B2:F20" -> "B2"
    range = range_str.split("!")[1].split(":")[0]
    # extract letters -> "B"
    return re.match(r"[A-Za-z]+", range).group()
