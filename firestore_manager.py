"""
Firestore State Manager for ACAST Ecosystem
Centralized state management using Firebase Firestore
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.client import Client as FirestoreClient
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from typing import Dict, Any, Optional, List
import json
import logging
from datetime import datetime, timedelta
import os

class FirestoreManager:
    """Manages all Firestore operations for the ACAST ecosystem"""
    
    def __init__(self, project_id: str, credential_path: Optional[str] = None):
        """
        Initialize Firestore connection
        
        Args:
            project_id: Firebase project ID
            credential_path: Path to service account key JSON (optional if using ADC)
        """
        self.logger = logging.getLogger(__name__)
        
        try:
            # Initialize Firebase app if not already initialized
            if not firebase_admin._apps:
                if credential_path and os.path.exists(credential_path):
                    cred = credentials.Certificate(credential_path)
                    firebase_admin.initialize_app(cred, {
                        'projectId': project_id
                    })
                    self.logger.info(f"Firebase initialized with service account: {credential_path}")
                else:
                    # Use Application Default Credentials (ADC)
                    firebase_admin.initialize_app()
                    self.logger.info("Firebase initialized with Application Default Credentials")
            
            # Get Firestore client
            self.db: FirestoreClient = firestore.client()
            self.logger.info(f"Firestore client initialized for project: {project_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Firestore: {str(e)}")
            raise
    
    def update_node_state(self, 
                         node_id: str, 
                         state: Dict[str, Any],
                         collection: str = "acast_nodes") -> bool:
        """
        Update ACAST node state in Firestore
        
        Args:
            node_id: Unique node identifier
            state: Node state dictionary
            collection: Firestore collection name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Add timestamp to state
            state_with_meta = {
                **state,
                'last_updated': SERVER_TIMESTAMP,
                'node_id': node_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Update document
            doc_ref = self.db.collection(collection).document(node_id)
            doc_ref.set(state_with_meta, merge=True)
            
            self.logger.debug(f"Updated state for node {node_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update node state for {node_id}: {str(e)}")
            return False
    
    def get_node_state(self, 
                      node_id: str,
                      collection: str = "acast_nodes") -> Optional[Dict[str, Any]]:
        """
        Retrieve ACAST node state from Firestore
        
        Args:
            node_id: Unique node identifier
            collection: Firestore collection name
            
        Returns:
            Optional[Dict]: Node state if found, None otherwise
        """
        try:
            doc_ref = self.db.collection(collection).document(node_id)
            doc =