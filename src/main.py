import os

def gameSelect():
  print("""Select a game:

  1. Snake
  2. Life
  """)

  game = input("Choice: ")

  # Run the game
  if game == "1":
      import src.games.snake
  elif game == "2":
      import src.games.life
  else:
      print("Invalid game number!")

gameSelect()
