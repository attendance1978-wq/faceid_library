"""
Face database management
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
import pickle

class FaceDatabase:
    """
    Database for storing face encodings and person information
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize face database
        
        Args:
            db_path: Path to database file (optional)
        """
        self.db_path = db_path
        self.people = {}  # person_id -> person info
        self.encodings = {}  # person_id -> face encoding
        
        if db_path and Path(db_path).exists():
            self.load(db_path)
    
    def add_person(self, 
                   person_id: str, 
                   name: str, 
                   encoding: np.ndarray,
                   metadata: Dict = None) -> bool:
        """
        Add a person to the database
        
        Args:
            person_id: Unique identifier
            name: Person's name
            encoding: Face encoding vector
            metadata: Additional metadata
            
        Returns:
            True if successful
        """
        if person_id in self.people:
            # Update existing person
            self.people[person_id]['name'] = name
            if metadata:
                self.people[person_id]['metadata'].update(metadata)
        else:
            # Add new person
            self.people[person_id] = {
                'name': name,
                'metadata': metadata or {}
            }
        
        self.encodings[person_id] = encoding
        
        # Auto-save if path provided
        if self.db_path:
            self.save(self.db_path)
        
        return True
    
    def find_matches(self, 
                     encoding: np.ndarray, 
                     threshold: float = 0.6) -> List[Dict]:
        """
        Find matching persons for a given encoding
        
        Args:
            encoding: Face encoding to match
            threshold: Similarity threshold
            
        Returns:
            List of matches sorted by similarity
        """
        matches = []
        
        for person_id, stored_encoding in self.encodings.items():
            similarity = self._cosine_similarity(encoding, stored_encoding)
            
            if similarity >= threshold:
                matches.append({
                    'person_id': person_id,
                    'name': self.people[person_id]['name'],
                    'similarity': similarity,
                    'metadata': self.people[person_id]['metadata']
                })
        
        # Sort by similarity (highest first)
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        
        return matches
    
    def get_encoding(self, person_id: str) -> Optional[np.ndarray]:
        """Get encoding for a person"""
        return self.encodings.get(person_id)
    
    def get_person(self, person_id: str) -> Optional[Dict]:
        """Get person information"""
        return self.people.get(person_id)
    
    def delete_person(self, person_id: str) -> bool:
        """Delete a person from database"""
        if person_id in self.people:
            del self.people[person_id]
            del self.encodings[person_id]
            
            if self.db_path:
                self.save(self.db_path)
            
            return True
        return False
    
    def list_people(self) -> List[Dict]:
        """List all people in database"""
        return [
            {
                'person_id': pid,
                'name': info['name'],
                'metadata': info['metadata']
            }
            for pid, info in self.people.items()
        ]
    
    def save(self, path: str):
        """Save database to file"""
        data = {
            'people': self.people,
            'encodings': {pid: enc.tolist() for pid, enc in self.encodings.items()}
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, path: str):
        """Load database from file"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.people = data['people']
        self.encodings = {
            pid: np.array(enc) for pid, enc in data['encodings'].items()
        }
    
    def clear(self):
        """Clear all data"""
        self.people.clear()
        self.encodings.clear()
    
    def __len__(self):
        return len(self.people)
    
    def __repr__(self):
        return f"FaceDatabase(people={len(self.people)})"
    
    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        similarity = dot_product / (norm_a * norm_b)
        return (similarity + 1) / 2
