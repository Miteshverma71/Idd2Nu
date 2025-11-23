import uuid
import json
from typing import Dict, Optional


class TokenManager:
    def __init__(self):
        # Forward and reverse lookup
        self.tokens: Dict[str, str] = {}
        self._reverse_lookup: Dict[str, str] = {}

    def _generate_token(self, prefix: str) -> str:
        """Generate a unique token with a prefix for readability."""
        return f"{prefix}-{uuid.uuid4().hex}"

    def get(self, name: str, create_if_missing: bool = True) -> Optional[str]:
        """
        Get a token by name. If it doesn't exist and create_if_missing is True,
        create a new token with a prefix based on the name.
        """
        if name in self.tokens:
            return self.tokens[name]

        if not create_if_missing:
            return None

        # Extract prefix from name (e.g., 'scene_1' -> 'scene')
        prefix = name.split('_')[0]
        while True:
            new_token = self._generate_token(prefix)
            if new_token not in self._reverse_lookup:
                break

        self.tokens[name] = new_token
        self._reverse_lookup[new_token] = name
        return new_token

    def get_name(self, token: str) -> Optional[str]:
        """Get the name associated with a token."""
        return self._reverse_lookup.get(token)

    def ensure_consistent(self, name: str, token: str) -> str:
        """
        Ensure consistent token usage. If the name already has a different token,
        return the existing one. If another name has this token, generate a new one.
        Otherwise, register this token.
        """
        if name in self.tokens:
            return self.tokens[name]

        if token in self._reverse_lookup and self._reverse_lookup[token] != name:
            # Token already used by another name, generate a new one
            prefix = name.split('_')[0]
            while True:
                new_token = self._generate_token(prefix)
                if new_token not in self._reverse_lookup:
                    self.tokens[name] = new_token
                    self._reverse_lookup[new_token] = name
                    return new_token

        # Otherwise, register this token
        self.tokens[name] = token
        self._reverse_lookup[token] = name
        return token

    # Specialized methods for dataset entities
    def get_or_create_scene_token(self, scene_num: int) -> str:
        return self.get(f"scene_{scene_num}")

    def get_or_create_sample_token(self, scene_num: int, frame_num: int) -> str:
        return self.get(f"sample_{scene_num}_{frame_num}")

    def get_or_create_ego_pose_token(self, scene_num: int, frame_num: int) -> str:
        return self.get(f"ego_pose_{scene_num}_{frame_num}")

    def get_or_create_sensor_token(self, sensor_name: str) -> str:
        return self.get(f"sensor_{sensor_name}")

    def get_or_create_calibrated_sensor_token(self, sensor_name: str) -> str:
        return self.get(f"calib_{sensor_name}")
    

    def get_or_create_log_token(self, scene_num: int) -> str:
        return self.get(f"log_{scene_num}")

    # Persistence methods
    def save(self, path: str):
        """Save tokens to a JSON file."""
        with open(path, "w") as f:
            json.dump(self.tokens, f, indent=4)
        print(f"✅ Tokens saved to {path}")

    def load(self, path: str):
        """Load tokens from a JSON file and rebuild reverse lookup."""
        with open(path, "r") as f:
            self.tokens = json.load(f)
        self._reverse_lookup = {v: k for k, v in self.tokens.items()}
        print(f"✅ Tokens loaded from {path}")
