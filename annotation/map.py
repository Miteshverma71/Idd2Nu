import json

def generate_map_json(path, tokens):
    maps = [{
        "category": "semantic_prior",
        "token": tokens.get("map_token"),
        "filename": "maps/53992ee3023e5494b90c316c183be829.png",
        "log_tokens": [tokens.get("log")]
    }]
    with open(path, "w") as f:
        json.dump(maps, f, indent=4)
    print("✅ map.json created")
