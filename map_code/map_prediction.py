import json
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

def load_token_map(data_dir: Path) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Load and separate instance and sample tokens from the tokens_map.json file."""
    token_map_file = data_dir / "annotation" / "tokens_map.json"
    
    print(f"Looking for tokens_map.json in: {token_map_file}")
    if not token_map_file.exists():
        raise FileNotFoundError(
            f"Token map file not found at: {token_map_file}\n"
            f"Please ensure the file exists at: {data_dir / 'annotation' / 'tokens_map.json'}"
        )
    
    print(f"Loading token map from: {token_map_file}")
    with open(token_map_file, 'r', encoding='utf-8') as f:
        token_map = json.load(f)
    
    # Print first 5 items to show the structure
    print("\nFirst 5 items in tokens_map.json:")
    for i, (k, v) in enumerate(list(token_map.items())[:5]):
        print(f"  {k}: {v}")
    
    # Separate instance and sample tokens
    instances = {k: v for k, v in token_map.items() if k.startswith('inst_')}
    samples = {k: v for k, v in token_map.items() if k.startswith('sample_')}
    
    print(f"\nFound {len(instances)} instance tokens and {len(samples)} sample tokens")
    return instances, samples

def create_predictions(
    data_dir: Path,
    output_dir: Path = None,
    scene_numbers: List[int] = [1, 2, 3, 4, 5]
) -> None:
    """Create prediction data by matching instance and sample tokens by scene number."""
    if output_dir is None:
        output_dir = data_dir / "map" / "predictions"
    else:
        output_dir = output_dir / "predictions"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Load and separate tokens
        instances, samples = load_token_map(data_dir)
        
        # Group tokens by scene number
        scene_instances = defaultdict(list)
        scene_samples = defaultdict(list)
        
        # Group instances by scene
        for token, mapped in instances.items():
            try:
                scene_num = int(token.split('_')[1])
                scene_instances[scene_num].append(mapped)  # Store just the UUID
            except (IndexError, ValueError):
                continue  # Skip malformed tokens
            
        # Group samples by scene
        for token, mapped in samples.items():
            try:
                scene_num = int(token.split('_')[1])
                scene_samples[scene_num].append(mapped)  # Store just the UUID
            except (IndexError, ValueError):
                continue  # Skip malformed tokens
        
        # Create the predictions dictionary
        predictions = {}
        
        # Process each scene
        for scene_num in scene_numbers:
            try:
                scene_insts = scene_instances.get(scene_num, [])
                scene_samps = scene_samples.get(scene_num, [])
                
                if not scene_insts or not scene_samps:
                    print(f"⚠ No instances or samples found for scene {scene_num}")
                    continue
                
                # Create predictions for this scene
                scene_predictions = []
                for inst_mapped in scene_insts:
                    for samp_mapped in scene_samps:
                        # Format: "instance_uuid_sample_uuid"
                        scene_predictions.append(f"{inst_mapped}_{samp_mapped}")
                
                # Add to predictions dict with scene name as key
                scene_name = f"scene-{scene_num:04d}"
                predictions[scene_name] = scene_predictions
                
                print(f"✅ Processed scene {scene_name} with {len(scene_predictions)} predictions")
                
            except Exception as e:
                print(f"⚠ Error processing scene {scene_num}: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # Save all predictions to a single JSON file
        output_file = output_dir / "prediction_scenes.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(predictions, f, indent=2)
        print(f"✅ Saved predictions to: {output_file}")
                
    except Exception as e:
        print(f"⚠ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    base_dir = Path(r"C:\Users\mitvi\Downloads\argov2_00000")
    data_dir = base_dir / "output"  # Where tokens_map.json is located
    output_dir = base_dir / "output" / "map"  # Where to save predictions
    
    print(f"Base directory: {base_dir}")
    print(f"Data directory: {data_dir}")
    print(f"Output directory: {output_dir}")
    
    create_predictions(data_dir=data_dir, output_dir=output_dir)s
