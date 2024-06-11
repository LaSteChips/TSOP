import sqlite3
import pygame
from datetime import datetime

# Configuration de la base de données
def setup_database():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER,
        date INTEGER
    )
    ''')
    connection.commit()
    connection.close()

# Fonction pour insérer des données dans la base de données
def insert_data(score):
    # Obtenir la date actuelle au format YYYYMMDD
    current_date = datetime.now().strftime("%Y%m%d")
    
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO game_data (score, date) VALUES (?, ?)", (score, current_date))
    connection.commit()
    connection.close()

# Fonction pour formater la date
def format_date(date):
    date_str = str(date)
    formatted_date = f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:]}"
    return formatted_date

# Fonction pour récupérer les données
def fetch_data():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT score, date FROM game_data")
    data = cursor.fetchall()
    connection.close()
    return data

# Fonction principale de Pygame
def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Affichage des scores")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.Font(None, 36)
    
    data = fetch_data()
    
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        
        y_offset = 50
        for score, date in data:
            formatted_date = format_date(date)
            text = font.render(f"Score: {score}, Date: {formatted_date}", True, BLACK)
            screen.blit(text, (50, y_offset))
            y_offset += 40
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    setup_database()
    # Insérer des données d'exemple
    # insert_data(100)
    main()
