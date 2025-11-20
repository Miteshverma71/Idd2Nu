import json
from token_manager import TokenManager

DEFAULT_MAP_IMAGE = "maps/53992ee3023e5494b90c316c183be829.png"

def generate_map_json(path: str, tokens: TokenManager) -> None:
    map_data = [{
        "category": "semantic_prior",
        "token": tokens.get("map_token"),
        "filename": DEFAULT_MAP_IMAGE,
        "log_tokens": [tokens.get("log")]
    }]
    with open(path, "w") as f:
        json.dump(map_data, f, indent=4)  # Changed 'logs' to 'map_data'
    print("✅ map.json created")