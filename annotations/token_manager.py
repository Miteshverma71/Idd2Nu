import uuid
from typing import Dict, Optional, Union

class TokenManager:
    def __init__(self):
        self.tokens: Dict[str, str] = {}
        self._reverse_lookup: Dict[str, str] = {}

    def get(self, name: str, create_if_missing: bool = True) -> Optional[str]:
        """
        Get a token by name. If it doesn't exist and create_if_missing is True,
        create a new token.
        
        Args:
            name: The name of the token to get or create
            create_if_missing: Whether to create the token if it doesn't exist
            
        Returns:
            The token string, or None if the token doesn't exist and create_if_missing is False
        """
        if name in self.tokens:
            return self.tokens[name]
            
        if not create_if_missing:
            return None
            
        # Generate a new token and ensure it's unique across all tokens
        while True:
            new_token = uuid.uuid4().hex
            if new_token not in self._reverse_lookup:
                break
                
        self.tokens[name] = new_token
        self._reverse_lookup[new_token] = name
        return new_token
        
    def get_name(self, token: str) -> Optional[str]:
        """Get the name of a token."""
        return self._reverse_lookup.get(token)
        
    def ensure_consistent(self, name: str, token: str) -> str:
        """
        Ensure consistent token usage. If the name already has a different token,
        return the existing one. If another name has this token, generate a new one.
        Otherwise, register this token for the name.
        """
        # If name already has a token, return it
        if name in self.tokens:
            return self.tokens[name]
            
        # If token is already used by another name, generate a new one
        if token in self._reverse_lookup and self._reverse_lookup[token] != name:
            while True:
                new_token = uuid.uuid4().hex
                if new_token not in self._reverse_lookup:
                    self.tokens[name] = new_token
                    self._reverse_lookup[new_token] = name
                    return new_token
        
        # Otherwise, register this token
        self.tokens[name] = token
        self._reverse_lookup[token] = name
        return token
        
    def get_or_create_scene_token(self, scene_num: int) -> str:
        """Get or create a token for a scene."""
        return self.get(f"scene_{scene_num-1}")
        
    def get_or_create_sample_token(self, scene_num: int, frame_num: int) -> str:
        """Get or create a token for a sample (frame) in a scene."""
        return self.get(f"sample_{frame_num}_scene_{scene_num-1}")
        
    def get_or_create_ego_pose_token(self, scene_num: int, frame_num: int) -> str:
        """Get or create a token for an ego pose."""
        return self.get(f"ego_pose_{frame_num}_scene_{scene_num-1}")
        
    def get_or_create_sensor_token(self, sensor_name: str) -> str:
        """Get or create a token for a sensor."""
        return self.get(f"sensor_{sensor_name}")
        
    def get_or_create_calibrated_sensor_token(self, sensor_name: str) -> str:
        """Get or create a token for a calibrated sensor."""
        return self.get(f"calib_{sensor_name}")
