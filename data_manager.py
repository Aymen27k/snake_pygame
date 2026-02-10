import json
import os

class DataManager:
    def __init__(self, filename="game_data.json"):
        self.filename = filename
        self.defaults = {
            "settings": {"music_on": True, "sfx_on": True},
            "high_scores": {} # Your game_mode dict goes here
        }
        self.data = self.load_all()

    def load_all(self):
        if not os.path.exists(self.filename):
            return self.defaults.copy()
        try:
            with open(self.filename, 'r', encoding="UTF-8") as f:
                return json.load(f)
        except:
            return self.defaults.copy()

    def save(self):
        try:
            with open(self.filename, "w", encoding="UTF-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def get_setting(self, key):
        return self.data["settings"].get(key, self.defaults["settings"][key])

    def update_setting(self, key, value):
        self.data["settings"][key] = value
        self.save()


    # Highscore Manager
    def get_high_score(self, game_mode):
        # This replaces your old load_high_score logic
        record = self.data["high_scores"].get(game_mode, 0)

        if isinstance(record, dict):
            return record.get("score", 0), record.get("name", "---")
        else:
            # Graceful handling for old integer-only scores
            return record, "LEGEND"

    def update_high_score(self, game_mode, score, name):
        self.data["high_scores"][game_mode] = {"score": score, "name": name}
        self.save()
