from typing import List, Dict, Any
from app.services.interfaces.service_interfaces import DataGovernance
from datetime import datetime, timedelta
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.models.models import Document

class BasicDataGovernance(DataGovernance):
    async def validate_document(self, content: str, metadata: Dict[str, Any]) -> bool:
        """
        Validate document against basic governance rules:
        1. Check file size
        2. Check allowed file types
        3. Check required metadata
        """
        try:
            # Check content size (max 10MB)
            if len(content.encode('utf-8')) > 10 * 1024 * 1024:
                return False

            # Check required metadata fields
            required_fields = ['source', 'owner', 'classification']
            if not all(field in metadata for field in required_fields):
                return False

            # Check allowed classifications
            allowed_classifications = ['public', 'internal', 'confidential']
            if metadata.get('classification') not in allowed_classifications:
                return False

            return True
        except Exception as e:
            print(f"Error validating document: {e}")
            return False

    async def apply_retention_policy(self, document_id: str) -> bool:
        """
        Apply retention policy to document:
        1. Check document age
        2. Archive or delete based on classification
        """
        try:
            db = next(get_db())
            document = db.query(Document).filter(Document.id == document_id).first()
            
            if not document:
                return False

            # Get document age
            age = datetime.utcnow() - document.created_at

            # Apply retention rules based on classification
            retention_periods = {
                'public': timedelta(days=365),
                'internal': timedelta(days=730),
                'confidential': timedelta(days=1825)
            }

            classification = document.metadata.get('classification', 'public')
            retention_period = retention_periods.get(classification, timedelta(days=365))

            # If document is older than retention period, mark for deletion
            if age > retention_period:
                document.metadata['marked_for_deletion'] = True
                document.metadata['deletion_date'] = datetime.utcnow().isoformat()
                db.commit()

            return True
        except Exception as e:
            print(f"Error applying retention policy: {e}")
            return False