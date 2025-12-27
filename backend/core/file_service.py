"""
File upload and management service
"""
import os
import uuid
import logging
from typing import Optional, Tuple
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage
from django.conf import settings
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)


class FileService:
    """Service for file uploads and management"""
    
    # Allowed image extensions
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    # Max file sizes (in bytes)
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def validate_image(file: UploadedFile) -> Tuple[bool, Optional[str]]:
        """
        Validate image file
        
        Args:
            file: Uploaded file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file extension
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in FileService.ALLOWED_IMAGE_EXTENSIONS:
            return False, f"Extension non autorisée. Extensions autorisées: {', '.join(FileService.ALLOWED_IMAGE_EXTENSIONS)}"
        
        # Check file size
        if file.size > FileService.MAX_IMAGE_SIZE:
            return False, f"Fichier trop volumineux. Taille maximale: {FileService.MAX_IMAGE_SIZE / (1024*1024)}MB"
        
        # Check if it's actually an image
        try:
            img = Image.open(file)
            img.verify()
            return True, None
        except Exception as e:
            return False, f"Fichier image invalide: {str(e)}"
    
    @staticmethod
    def validate_document(file: UploadedFile) -> Tuple[bool, Optional[str]]:
        """
        Validate document file
        
        Args:
            file: Uploaded file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file size
        if file.size > FileService.MAX_DOCUMENT_SIZE:
            return False, f"Fichier trop volumineux. Taille maximale: {FileService.MAX_DOCUMENT_SIZE / (1024*1024)}MB"
        
        return True, None
    
    @staticmethod
    def generate_unique_filename(original_filename: str, prefix: str = '') -> str:
        """
        Generate unique filename
        
        Args:
            original_filename: Original filename
            prefix: Optional prefix for the filename
            
        Returns:
            Unique filename
        """
        ext = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())[:8]
        prefix = f"{prefix}_" if prefix else ""
        return f"{prefix}{unique_id}{ext}"
    
    @staticmethod
    def upload_image(file: UploadedFile, upload_path: str, prefix: str = '') -> Optional[str]:
        """
        Upload and process image
        
        Args:
            file: Uploaded file
            upload_path: Path to upload to (e.g., 'vehicles/')
            prefix: Optional prefix for filename
            
        Returns:
            File path if successful, None otherwise
        """
        # Validate image
        is_valid, error = FileService.validate_image(file)
        if not is_valid:
            logger.error(f"Image validation failed: {error}")
            raise ValueError(error)
        
        try:
            # Generate unique filename
            filename = FileService.generate_unique_filename(file.name, prefix)
            file_path = os.path.join(upload_path, filename)
            
            # Process and save image
            img = Image.open(file)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = rgb_img
            
            # Resize if too large (max 1920x1920)
            max_size = (1920, 1920)
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save image
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Save to storage
            saved_path = default_storage.save(file_path, output)
            
            logger.info(f"Image uploaded successfully: {saved_path}")
            return saved_path
            
        except Exception as e:
            logger.error(f"Failed to upload image: {str(e)}")
            raise
    
    @staticmethod
    def upload_document(file: UploadedFile, upload_path: str, prefix: str = '') -> Optional[str]:
        """
        Upload document file
        
        Args:
            file: Uploaded file
            upload_path: Path to upload to
            prefix: Optional prefix for filename
            
        Returns:
            File path if successful, None otherwise
        """
        # Validate document
        is_valid, error = FileService.validate_document(file)
        if not is_valid:
            logger.error(f"Document validation failed: {error}")
            raise ValueError(error)
        
        try:
            # Generate unique filename
            filename = FileService.generate_unique_filename(file.name, prefix)
            file_path = os.path.join(upload_path, filename)
            
            # Save file
            saved_path = default_storage.save(file_path, file)
            
            logger.info(f"Document uploaded successfully: {saved_path}")
            return saved_path
            
        except Exception as e:
            logger.error(f"Failed to upload document: {str(e)}")
            raise
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete file from storage
        
        Args:
            file_path: Path to file
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                logger.info(f"File deleted successfully: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file: {str(e)}")
            return False

