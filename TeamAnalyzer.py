import sqlite3
import sys

##All the "against" column suffixes:
types = ["bug", "dark", "dragon", "electric", "fairy", "fight",
"fire", "flying", "ghost", "grass", "ground", "ice", "normal",
"poison", "psychic", "rock", "steel", "water"]

##Check if the input is a valid Pokedex number or Pokemon name
def get_pokemon_id(pokemon):
    conn = sqlite3.connect("pokemon.sqlite")
    c = conn.cursor()

    # Check if the input is a valid Pokedex number
    pokemon_id = c.execute(f"SELECT pokedex_number FROM Pokemon WHERE pokedex_number = {pokemon}").fetchone()
    if pokemon_id:
        return pokemon_id[0]

    # Check if the input is a valid Pokemon name
    pokemon_id = c.execute(f"SELECT pokedex_number FROM Pokemon WHERE name = '{pokemon}'").fetchone()
    if pokemon_id:
        return pokemon_id[0]

    # If the input is not valid, return None
    return None
##Take six parameters on the command-line
if len(sys.argv) < 7:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

##Connect to the database
conn = sqlite3.connect("pokemon.sqlite")
c = conn.cursor()

team = []
for i in range(1, 7):
# Check if the input is a valid Pokedex number or Pokemon name
    pokemon_id = get_pokemon_id(sys.argv[i])
    if not pokemon_id:
        print(f"Invalid input for Pokemon {i}: {sys.argv[i]}")
        sys.exit()

    # Analyze the pokemon whose pokedex_number is in "pokemon_id"
    pokemon = c.execute(f"SELECT Pokemon.*,pokemon_types_view.type1,pokemon_types_view.type2,against_bug,against_dark,against_dragon,against_electric,against_fairy,against_fight,against_fire,against_flying,against_ghost,against_grass,against_ground,against_ice,against_normal,against_poison,against_psychic,against_rock,against_steel,against_water FROM Pokemon,pokemon_types_view,battle WHERE Pokemon.name=pokemon_types_view.name and pokemon_types_view.type1=battle.type1name and pokemon_types_view.type2=battle.type2name and pokedex_number={pokemon_id}").fetchone()

    # Check against all the different types of Pokemon
    strong_against = []
    weak_against = []
##    rows = c.fetchall()
    for type in types:
        against_column = f"against_{type}"
        against_value = 1.0
        col_index1 = [description[0] for description in c.description].index('type1')
        col_index2 = [description[0] for description in c.description].index('type2')
        col_index3 = [description[0] for description in c.description].index(against_column)
        if pokemon[col_index1] == type:
            against_value *= 2.0
        if pokemon[col_index2] == type:
            against_value *= 2.0
        against_value *= pokemon[col_index3]
        if against_value > 1:
            strong_against.append(type)
        elif against_value < 1:
            weak_against.append(type)

    # Print the analysis for this Pokemon
    print(f"Analyzing {pokemon_id}")
    print(f"{pokemon[1]} ({pokemon[2]}) is strong against {strong_against} but weak against {weak_against}")
##Ask the user if they want to save the team
answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")
    #Create table teams
    c.execute('''CREATE TABLE IF NOT EXISTS teams
                 (team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  team_name TEXT,
                  pokemon1 INTEGER,
                  pokemon2 INTEGER,
                  pokemon3 INTEGER,
                  pokemon4 INTEGER,
                  pokemon5 INTEGER,
                  pokemon6 INTEGER)''')

    conn.commit()
    # Write the pokemon team to the "teams" table
    c.execute(f"INSERT INTO teams(team_name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6) VALUES ('{teamName}', {get_pokemon_id(sys.argv[1])}, {get_pokemon_id(sys.argv[2])}, {get_pokemon_id(sys.argv[3])}, {get_pokemon_id(sys.argv[4])}, {get_pokemon_id(sys.argv[5])}, {get_pokemon_id(sys.argv[6])})")
    conn.commit()
    print("Saving " + teamName + " ...")
else:
    print("Bye for now!")

##Close the database connection
conn.close()
