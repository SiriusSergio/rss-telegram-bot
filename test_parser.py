from parser.junglergg import fetch_champions_by_role

if __name__ == "__main__":
    champions = fetch_champions_by_role("lane_jungle")
        for champ in champions:
            print(f"{champ['name']}: Win Rate {champ['win_rate']}")