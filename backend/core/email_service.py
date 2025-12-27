"""
Email notification service
"""
import logging
from typing import List, Optional, Dict, Any
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails"""
    
    DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@rent4you.com'
    
    @staticmethod
    def send_email(
        subject: str,
        message: str,
        recipient_list: List[str],
        html_message: Optional[str] = None,
        from_email: Optional[str] = None,
        fail_silently: bool = False
    ) -> bool:
        """
        Send email
        
        Args:
            subject: Email subject
            message: Plain text message
            recipient_list: List of recipient emails
            html_message: Optional HTML message
            from_email: Sender email
            fail_silently: If True, don't raise exceptions
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            from_email = from_email or EmailService.DEFAULT_FROM_EMAIL
            
            if html_message:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    from_email=from_email,
                    to=recipient_list
                )
                email.attach_alternative(html_message, "text/html")
                email.send()
            else:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    fail_silently=fail_silently
                )
            
            logger.info(f"Email sent successfully to {recipient_list}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            if not fail_silently:
                raise
            return False
    
    @staticmethod
    def send_reservation_confirmation(reservation, user_email: str) -> bool:
        """Send reservation confirmation email"""
        subject = f"Confirmation de réservation #{reservation.id}"
        context = {
            'reservation': reservation,
            'user_email': user_email,
        }
        
        html_message = f"""
        <html>
        <body>
            <h2>Confirmation de réservation</h2>
            <p>Votre réservation a été confirmée avec succès.</p>
            <p><strong>Réservation #:</strong> {reservation.id}</p>
            <p><strong>Véhicule:</strong> {reservation.vehicule.marque} {reservation.vehicule.model}</p>
            <p><strong>Date de début:</strong> {reservation.date_debut}</p>
            <p><strong>Date de fin:</strong> {reservation.date_fin}</p>
            <p><strong>Prix:</strong> {reservation.prix} MAD</p>
            <p>Merci d'avoir choisi Rent4You!</p>
        </body>
        </html>
        """
        
        message = strip_tags(html_message)
        
        return EmailService.send_email(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[user_email]
        )
    
    @staticmethod
    def send_reservation_cancellation(reservation, user_email: str) -> bool:
        """Send reservation cancellation email"""
        subject = f"Annulation de réservation #{reservation.id}"
        
        html_message = f"""
        <html>
        <body>
            <h2>Réservation annulée</h2>
            <p>Votre réservation a été annulée.</p>
            <p><strong>Réservation #:</strong> {reservation.id}</p>
            <p><strong>Véhicule:</strong> {reservation.vehicule.marque} {reservation.vehicule.model}</p>
            <p>Si vous avez des questions, n'hésitez pas à nous contacter.</p>
        </body>
        </html>
        """
        
        message = strip_tags(html_message)
        
        return EmailService.send_email(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[user_email]
        )
    
    @staticmethod
    def send_contract_ready(contract, user_email: str) -> bool:
        """Send contract ready for signature email"""
        subject = f"Contrat prêt à signer - Réservation #{contract.reservation.id}"
        
        html_message = f"""
        <html>
        <body>
            <h2>Contrat prêt à signer</h2>
            <p>Votre contrat de location est prêt à être signé.</p>
            <p><strong>Réservation #:</strong> {contract.reservation.id}</p>
            <p>Veuillez vous connecter à votre compte pour signer le contrat.</p>
        </body>
        </html>
        """
        
        message = strip_tags(html_message)
        
        return EmailService.send_email(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[user_email]
        )
    
    @staticmethod
    def send_complaint_received(complaint, owner_email: str) -> bool:
        """Send complaint received notification to agency owner"""
        subject = f"Nouvelle réclamation #{complaint.id}"
        
        html_message = f"""
        <html>
        <body>
            <h2>Nouvelle réclamation</h2>
            <p>Une nouvelle réclamation a été reçue.</p>
            <p><strong>Réclamation #:</strong> {complaint.id}</p>
            <p><strong>Locataire:</strong> {complaint.locataire.user.email}</p>
            <p><strong>Contenu:</strong> {complaint.contenu_reclamation[:200]}...</p>
            <p>Veuillez vous connecter pour traiter cette réclamation.</p>
        </body>
        </html>
        """
        
        message = strip_tags(html_message)
        
        return EmailService.send_email(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[owner_email]
        )
    
    @staticmethod
    def send_partnership_approved(partnership, owner_email: str) -> bool:
        """Send partnership approval email"""
        subject = f"Demande de partenariat approuvée - {partnership.nom_agence}"
        
        html_message = f"""
        <html>
        <body>
            <h2>Demande de partenariat approuvée</h2>
            <p>Félicitations! Votre demande de partenariat a été approuvée.</p>
            <p><strong>Agence:</strong> {partnership.nom_agence}</p>
            <p>Vous pouvez maintenant vous connecter avec vos identifiants.</p>
        </body>
        </html>
        """
        
        message = strip_tags(html_message)
        
        return EmailService.send_email(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[owner_email]
        )
    
    @staticmethod
    def send_welcome_email(user_email: str, username: str) -> bool:
        """Send welcome email to new user"""
        subject = "Bienvenue sur Rent4You"
        
        html_message = f"""
        <html>
        <body>
            <h2>Bienvenue sur Rent4You!</h2>
            <p>Bonjour {username},</p>
            <p>Merci de vous être inscrit sur Rent4You.</p>
            <p>Vous pouvez maintenant réserver des véhicules et profiter de nos services.</p>
            <p>Bonne journée!</p>
        </body>
        </html>
        """
        
        message = strip_tags(html_message)
        
        return EmailService.send_email(
            subject=subject,
            message=message,
            html_message=html_message,
            recipient_list=[user_email]
        )

