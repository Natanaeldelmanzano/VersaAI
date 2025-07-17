from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
import json
import asyncio
from datetime import datetime, timedelta

from src.models.chatbot import Chatbot
from src.models.conversation import Conversation
from src.schemas.chatbot import (
    ChatbotTraining, ChatbotStats, ChatbotStatus
)
from src.services.ai_service import AIService
from src.services.document_service import DocumentService
from src.core.config import settings
from src.utils.file_utils import save_uploaded_file, validate_file_type
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ChatbotService:
    def __init__(self):
        self.ai_service = AIService()
        self.document_service = DocumentService()
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_file_types = [
            'text/plain', 'application/pdf', 'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/csv', 'application/json'
        ]
    
    async def train_chatbot(
        self, 
        chatbot: Chatbot, 
        training_data: ChatbotTraining
    ) -> Dict[str, Any]:
        """
        Train chatbot with provided training data
        """
        try:
            logger.info(f"Starting training for chatbot {chatbot.id}")
            
            # Update chatbot status
            chatbot.status = ChatbotStatus.TRAINING
            
            # Prepare training data
            training_content = {
                "text_data": training_data.text_data or [],
                "qa_pairs": training_data.qa_pairs or [],
                "documents": training_data.documents or [],
                "urls": training_data.urls or []
            }
            
            # Process different types of training data
            processed_data = await self._process_training_data(training_content)
            
            # Train the AI model
            training_result = await self.ai_service.train_model(
                chatbot_id=chatbot.id,
                training_data=processed_data,
                config=chatbot.config or {}
            )
            
            # Update chatbot with training results
            chatbot.status = ChatbotStatus.TRAINED
            chatbot.training_data = training_content
            chatbot.model_version = training_result.get('model_version')
            chatbot.training_metrics = training_result.get('metrics', {})
            
            logger.info(f"Training completed for chatbot {chatbot.id}")
            
            return {
                "status": "completed",
                "model_version": training_result.get('model_version'),
                "metrics": training_result.get('metrics', {}),
                "training_time": training_result.get('training_time')
            }
            
        except Exception as e:
            logger.error(f"Training failed for chatbot {chatbot.id}: {str(e)}")
            chatbot.status = ChatbotStatus.TRAINING_FAILED
            raise HTTPException(
                status_code=500,
                detail=f"Training failed: {str(e)}"
            )
    
    async def process_training_documents(
        self, 
        chatbot: Chatbot, 
        files: List[UploadFile]
    ) -> List[Dict[str, Any]]:
        """
        Process uploaded training documents
        """
        try:
            processed_files = []
            
            for file in files:
                # Validate file
                if not self._validate_uploaded_file(file):
                    continue
                
                # Save file
                file_path = await save_uploaded_file(
                    file, 
                    f"chatbots/{chatbot.id}/training"
                )
                
                # Extract content
                content = await self.document_service.extract_content(
                    file_path, file.content_type
                )
                
                # Process content for training
                processed_content = await self.document_service.process_for_training(
                    content, file.filename
                )
                
                processed_files.append({
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "size": file.size,
                    "path": file_path,
                    "processed_content": processed_content,
                    "status": "processed"
                })
                
                logger.info(f"Processed training document: {file.filename}")
            
            return processed_files
            
        except Exception as e:
            logger.error(f"Failed to process training documents: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process documents: {str(e)}"
            )
    
    # async def deploy_chatbot(
    #     self, 
    #     chatbot: Chatbot, 
    #     deployment_config: Dict[str, Any]
    # ) -> Dict[str, Any]:
    #     """
    #     Deploy chatbot to production
    #     """
    #     try:
    #         logger.info(f"Deploying chatbot {chatbot.id}")
    #         
    #         # Validate chatbot is ready for deployment
    #         if chatbot.status != ChatbotStatus.TRAINED:
    #             raise HTTPException(
    #                 status_code=400,
    #                 detail="Chatbot must be trained before deployment"
    #             )
    #         
    #         # Prepare deployment configuration
    #         deploy_config = {
    #             "chatbot_id": chatbot.id,
    #             "name": chatbot.name,
    #             "model_version": chatbot.model_version,
    #             "config": chatbot.config or {},
    #             "deployment_settings": deployment_config
    #         }
    #         
    #         # Deploy to AI service
    #         deployment_result = await self.ai_service.deploy_model(
    #             deploy_config
    #         )
    #         
    #         # Update chatbot deployment info
    #         chatbot.deployment_config = deployment_config
    #         chatbot.deployment_url = deployment_result.get('endpoint_url')
    #         chatbot.deployment_id = deployment_result.get('deployment_id')
    #         chatbot.status = ChatbotStatus.DEPLOYED
    #         
    #         logger.info(f"Chatbot {chatbot.id} deployed successfully")
    #         
    #         return {
    #             "deployment_id": deployment_result.get('deployment_id'),
    #             "endpoint_url": deployment_result.get('endpoint_url'),
    #             "status": "deployed",
    #             "deployment_time": datetime.utcnow().isoformat()
    #         }
    #         
    #     except Exception as e:
    #         logger.error(f"Deployment failed for chatbot {chatbot.id}: {str(e)}")
    #         raise HTTPException(
    #             status_code=500,
    #             detail=f"Deployment failed: {str(e)}"
    #         )
        pass
    
    async def get_chatbot_stats(
        self, 
        chatbot: Chatbot,
        db: Optional[Session] = None
    ) -> ChatbotStats:
        """
        Get comprehensive chatbot statistics
        """
        try:
            # Get conversation statistics
            if db:
                conversations = db.query(Conversation).filter(
                    Conversation.chatbot_id == chatbot.id
                ).all()
                
                messages = db.query(Message).join(Conversation).filter(
                    Conversation.chatbot_id == chatbot.id
                ).all()
            else:
                conversations = []
                messages = []
            
            # Calculate basic stats
            total_conversations = len(conversations)
            total_messages = len(messages)
            user_messages = [m for m in messages if m.sender_type == 'user']
            bot_messages = [m for m in messages if m.sender_type == 'bot']
            
            # Calculate time-based stats
            now = datetime.utcnow()
            last_24h = now - timedelta(hours=24)
            last_7d = now - timedelta(days=7)
            last_30d = now - timedelta(days=30)
            
            conversations_24h = len([
                c for c in conversations 
                if c.created_at and c.created_at >= last_24h
            ])
            conversations_7d = len([
                c for c in conversations 
                if c.created_at and c.created_at >= last_7d
            ])
            conversations_30d = len([
                c for c in conversations 
                if c.created_at and c.created_at >= last_30d
            ])
            
            # Calculate response metrics
            avg_response_time = self._calculate_avg_response_time(messages)
            satisfaction_score = self._calculate_satisfaction_score(conversations)
            
            # Get AI model metrics
            model_metrics = chatbot.training_metrics or {}
            
            return ChatbotStats(
                total_conversations=total_conversations,
                total_messages=total_messages,
                user_messages=len(user_messages),
                bot_messages=len(bot_messages),
                conversations_24h=conversations_24h,
                conversations_7d=conversations_7d,
                conversations_30d=conversations_30d,
                avg_response_time=avg_response_time,
                satisfaction_score=satisfaction_score,
                model_accuracy=model_metrics.get('accuracy', 0.0),
                model_confidence=model_metrics.get('confidence', 0.0),
                training_data_size=len(chatbot.training_data or {}),
                last_trained=chatbot.updated_at,
                deployment_status=chatbot.status.value,
                is_active=chatbot.is_active
            )
            
        except Exception as e:
            logger.error(f"Failed to get stats for chatbot {chatbot.id}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve statistics: {str(e)}"
            )
    
    async def test_chatbot_response(
        self, 
        chatbot: Chatbot, 
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Test chatbot with a message and return response
        """
        try:
            # Generate response using AI service
            response = await self.ai_service.generate_response(
                chatbot_id=chatbot.id,
                message=message,
                context=context or {},
                test_mode=True
            )
            
            return {
                "input_message": message,
                "response": response.get('text', ''),
                "confidence": response.get('confidence', 0.0),
                "intent": response.get('intent'),
                "entities": response.get('entities', []),
                "response_time": response.get('response_time', 0),
                "test_mode": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Test failed for chatbot {chatbot.id}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Test failed: {str(e)}"
            )
    
    def _validate_uploaded_file(self, file: UploadFile) -> bool:
        """
        Validate uploaded file
        """
        # Check file size
        if file.size and file.size > self.max_file_size:
            logger.warning(f"File {file.filename} too large: {file.size} bytes")
            return False
        
        # Check file type
        if file.content_type not in self.allowed_file_types:
            logger.warning(f"File {file.filename} has invalid type: {file.content_type}")
            return False
        
        return True
    
    async def _process_training_data(
        self, 
        training_content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process and normalize training data
        """
        processed = {
            "text_chunks": [],
            "qa_pairs": [],
            "metadata": {}
        }
        
        # Process text data
        if training_content.get('text_data'):
            for text in training_content['text_data']:
                chunks = await self.document_service.chunk_text(text)
                processed['text_chunks'].extend(chunks)
        
        # Process Q&A pairs
        if training_content.get('qa_pairs'):
            processed['qa_pairs'] = training_content['qa_pairs']
        
        # Process documents
        if training_content.get('documents'):
            for doc in training_content['documents']:
                if doc.get('processed_content'):
                    chunks = await self.document_service.chunk_text(
                        doc['processed_content']
                    )
                    processed['text_chunks'].extend(chunks)
        
        # Process URLs (if any)
        if training_content.get('urls'):
            for url in training_content['urls']:
                try:
                    content = await self.document_service.extract_from_url(url)
                    chunks = await self.document_service.chunk_text(content)
                    processed['text_chunks'].extend(chunks)
                except Exception as e:
                    logger.warning(f"Failed to process URL {url}: {str(e)}")
        
        processed['metadata'] = {
            "total_chunks": len(processed['text_chunks']),
            "total_qa_pairs": len(processed['qa_pairs']),
            "processed_at": datetime.utcnow().isoformat()
        }
        
        return processed
    
    def _calculate_avg_response_time(self, messages: List[dict]) -> float:
        """
        Calculate average response time from messages
        """
        # TODO: Implement when Message model is available
        return 0.0
        # try:
        #     response_times = []
        #     
        #     for i in range(len(messages) - 1):
        #         current_msg = messages[i]
        #         next_msg = messages[i + 1]
        #         
        #         if (current_msg.sender_type == 'user' and 
        #             next_msg.sender_type == 'bot' and
        #             current_msg.created_at and next_msg.created_at):
        #             
        #             response_time = (
        #                 next_msg.created_at - current_msg.created_at
        #             ).total_seconds()
        #             response_times.append(response_time)
        #     
        #     return sum(response_times) / len(response_times) if response_times else 0.0
        #     
        # except Exception:
        #     return 0.0
    
    def _calculate_satisfaction_score(self, conversations: List[dict]) -> float:
        """
        Calculate satisfaction score from conversations
        """
        # TODO: Implement when Conversation model is available
        return 0.0
        # try:
        #     ratings = [
        #         c.rating for c in conversations 
        #         if c.rating is not None
        #     ]
        #     
        #     return sum(ratings) / len(ratings) if ratings else 0.0
        #     
        # except Exception:
        #     return 0.0
    
    async def update_chatbot_config(
        self, 
        chatbot: Chatbot, 
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update chatbot configuration
        """
        try:
            # Validate configuration
            validated_config = self._validate_config(config)
            
            # Update chatbot
            chatbot.config = validated_config
            
            # If chatbot is deployed, update deployment
            if chatbot.status == ChatbotStatus.DEPLOYED:
                await self.ai_service.update_deployment_config(
                    chatbot.deployment_id,
                    validated_config
                )
            
            return validated_config
            
        except Exception as e:
            logger.error(f"Failed to update config for chatbot {chatbot.id}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update configuration: {str(e)}"
            )
    
    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and normalize chatbot configuration
        """
        validated = {
            "ai_settings": config.get('ai_settings', {}),
            "appearance": config.get('appearance', {}),
            "behavior": config.get('behavior', {}),
            "widget_settings": config.get('widget_settings', {})
        }
        
        # Validate AI settings
        ai_settings = validated['ai_settings']
        ai_settings['temperature'] = max(0.0, min(2.0, 
            ai_settings.get('temperature', 0.7)
        ))
        ai_settings['max_tokens'] = max(1, min(4000, 
            ai_settings.get('max_tokens', 1000)
        ))
        
        # Validate appearance settings
        appearance = validated['appearance']
        if 'primary_color' in appearance:
            # Validate hex color
            color = appearance['primary_color']
            if not (color.startswith('#') and len(color) == 7):
                appearance['primary_color'] = '#007bff'
        
        return validated