import pygame
import os

class bg_son:
    def __init__(self):
        # Initialiser le mixer pour la musique
        pygame.mixer.init()
        
        # Chemin vers le dossier Musics
        self.music_path = "Musics/"
        
        # Fichier de musique disponible
        self.music_file = "deuslower-dark-fantasy-ambient-dungeon-synth-music-281592.mp3"
        self.music_file2 = "005. Ruins (UNDERTALE Soundtrack) - Toby Fox.mp3"
        self.music_file3 = "Unnerving Vibe.mp3"
        self.epeeslash = "DSGNMisc_MELEE-Sword Slash_HY_PC-001.wav"
        
        # Dictionnaire pour stocker les musiques par map
        self.map_music = {
            1: self.music_file,
            2: self.music_file2,
            3: self.music_file3
        }
        
        # Sons d'effets
        self.sound_effects = {
            "sword_slash": pygame.mixer.Sound(os.path.join(self.music_path, self.epeeslash))
        }
        
        # Dictionnaire pour les effets sonores
        self.bg_son = {
            "background_music": None  # La musique est gérée par pygame.mixer.music
        }
        
        self.current_map = None
        self.current_music = None
    
    def play_music(self, map_number):
        """Joue la musique de la map spécifiée en boucle."""
        # Vérifier si on est déjà sur la même map
        if self.current_map == map_number:
            return
        
        # Obtenir le fichier de musique pour cette map
        if map_number not in self.map_music:
            print(f"Aucune musique définie pour la map {map_number}")
            return
        
        music_file = self.map_music[map_number]
        full_path = os.path.join(self.music_path, music_file)
        
        # Vérifier que le fichier existe
        if not os.path.exists(full_path):
            print(f"Fichier audio non trouvé: {full_path}")
            return
        
        try:
            # Arrêter la musique actuelle
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(500)  # Fadeout de 500ms
            
            # Charger et jouer la nouvelle musique
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play(-1)  # -1 = boucle infinie
            
            self.current_map = map_number
            self.current_music = music_file
            print(f"Musique chargée pour la map {map_number}: {music_file}")
        
        except pygame.error as e:
            print(f"Erreur lors du chargement de la musique: {e}")
    
    def stop_music(self):
        """Arrête la musique avec un fadeout."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
        self.current_map = None
        self.current_music = None
    
    def set_music_volume(self, volume):
        """Définit le volume de la musique (0.0 à 1.0)."""
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    
    def play_sword_slash(self):
        """Joue le son de coup d'épée."""
        try:
            self.sound_effects["sword_slash"].play()
        except Exception as e:
            print(f"Erreur lors du chargement du son d'épée: {e}")
