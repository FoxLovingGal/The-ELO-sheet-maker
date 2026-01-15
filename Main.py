import os.path
from Player import player
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from StringBuilder import get_timeline
from config import SPREADSHEET
from config import num_players
from increment import incr_str
import time

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def main():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()

    #defining range of the game
    file = open("settings.txt", "r")

    #grabbing info from settings
    time_line_name = file.readline().split()[1]
    row = file.readline().split()[1]
    season_elo = file.readline().split()[1]
    all_time_elo = file.readline().split()[1]
    name_locations = file.readline().split()[1]
    name_sheet = file.readline().split()[1]

    file.close()
    #setting up timeline stuff, getting the ranges ready
    settings = [time_line_name, row, season_elo, all_time_elo, name_locations, name_sheet]
    time_line_start_end = get_timeline(sheet, time_line_name, row)
    start_position = time_line_start_end[0]
    end_position = time_line_start_end[1]
    row_range = time_line_name + "!" + start_position + str(row) + ":" + end_position + str(row)
    people_range = "People!M11:AI11"

    player_names = ['filler']
    offset = 1
    while player_names:
      winners_range = time_line_name + "!A" + str(int(row) + int(offset)) + ":D" + str(int(row) + int(offset))
      update_range = (time_line_name + "!" + start_position + str(int(row) + int(offset)) + ":" + end_position +
                      str(int(row) + int(offset)))
      time.sleep(1)  # basic way to deal with rate limit
      test = sheet.values().get(spreadsheetId=SPREADSHEET, range = update_range).execute()
      test = test.get("values", [])

      if not test:
        #grab that stuff from the api and put it into an actually usable form
        time.sleep(1)
        array = sheet.values().get(spreadsheetId=SPREADSHEET, range = winners_range).execute()
        player_names = array.get("values", [])

        if player_names:
          #set up players, put them in an array
          player1 = player(name = player_names[0][0], placement = 1, sheet = sheet, settings = settings,
                           time_line_range=row_range)
          player2 = player(name = player_names[0][1], placement = 2, sheet = sheet, settings = settings,
                           time_line_range=row_range)
          player3 = player(name = player_names[0][2], placement = 3, sheet = sheet, settings = settings,
                           time_line_range=row_range)
          player4 = player(name = player_names[0][3], placement = 4, sheet = sheet, settings = settings,
                           time_line_range=row_range)
          player_array = [player1, player2, player3, player4]



          previous_row = int(row) - 1 + offset
          #sets up the row, either with all 800s if first run through or with values from previous row
          if previous_row < 31:
            basic_values = [[800] * num_players["count"]]
            starting_elo = {"values": basic_values}

            time.sleep(1)
            sheet.values().update(spreadsheetId=SPREADSHEET, range=update_range,
                                  valueInputOption="USER_ENTERED", body=starting_elo).execute()
            time.sleep(1)
            sheet.values().update(spreadsheetId=SPREADSHEET, range=people_range,
                                  valueInputOption="USER_ENTERED", body=starting_elo).execute()
          else:
            time.sleep(1)
            previous_row_values = sheet.values().get(spreadsheetId=SPREADSHEET, range =time_line_name + "!" + start_position +
                                                                                       str(previous_row) + ":" +
                                                                                       end_position +
                                                                                       str(previous_row)).execute()
            previous_row_array = previous_row_values.get("values", [])
            prev_row_send = {"values": previous_row_array}
            time.sleep(1)
            sheet.values().update(spreadsheetId=SPREADSHEET, range=update_range,
                                  valueInputOption="USER_ENTERED", body=prev_row_send).execute()

          info_row = [season_elo, all_time_elo]
          for z in info_row:
          #acquire initial elo for all players
            for x in player_array:
              time.sleep(1)
              season_elo_raw = sheet.values().get(spreadsheetId=SPREADSHEET,
                                              range = "People!" + x.getcolumn() + z).execute()
              player_elo = season_elo_raw.get("values", [])
              x.set_init_elo(player_elo[0][0])

            for x in player_array:
              for y in player_array:
                if x != y:
                  x.game(y)

            for x in player_array:
              elo_body = {"values": [[round(x.getNewElo())]]}
              if z == "11":
                time.sleep(1)
                sheet.values().update(spreadsheetId=SPREADSHEET, range=time_line_name + "!" + x.get_Time_Line_column() +
                                      str(int(row) + offset), valueInputOption="USER_ENTERED", body=elo_body).execute()
                time.sleep(1)
                sheet.values().update(spreadsheetId=SPREADSHEET, range="People!" + x.getcolumn() + z,
                                      valueInputOption="USER_ENTERED", body=elo_body).execute()

      offset += 1
      print("line complete, current offset: " + str(offset))


  except HttpError as err:
    print(err)



if __name__ == "__main__":
  main()
