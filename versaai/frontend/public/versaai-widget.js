/**
 * VersaAI Chat Widget
 * Embeddable chat widget for websites
 * Version: 1.0.0
 */

(function() {
  'use strict';

  // Configuración por defecto
  const defaultConfig = {
    // Básico
    botName: 'VersaAI Assistant',
    welcomeMessage: '¡Hola! ¿En qué puedo ayudarte hoy?',
    inputPlaceholder: 'Escribe tu mensaje...',
    language: 'es',
    
    // Apariencia
    primaryColor: '#3B82F6',
    backgroundColor: '#FFFFFF',
    textColor: '#1F2937',
    position: 'bottom-right',
    size: 'medium',
    buttonShape: 'circle',
    avatarUrl: '',
    
    // Comportamiento
    autoOpen: false,
    autoOpenDelay: 5,
    showNotifications: true,
    enableSounds: true,
    showPoweredBy: true,
    maxHeight: 500,
    
    // API
    apiUrl: 'https://api.versaai.com',
    widgetId: null,
    
    // Mensajes predefinidos
    predefinedMessages: [
      { text: '¿Cómo funciona?' },
      { text: 'Ver precios' },
      { text: 'Contactar soporte' }
    ]
  };

  // Configuración global
  const config = Object.assign({}, defaultConfig, window.VersaAIConfig || {});

  // Estado del widget
  let isOpen = false;
  let isMinimized = false;
  let unreadCount = 0;
  let messages = [];
  let isTyping = false;
  let sessionId = null;

  // Elementos DOM
  let widgetContainer = null;
  let chatContainer = null;
  let messagesContainer = null;
  let inputField = null;
  let notificationBadge = null;

  // Utilidades
  const utils = {
    // Generar ID único
    generateId: () => {
      return 'versaai_' + Math.random().toString(36).substr(2, 9);
    },

    // Escapar HTML
    escapeHtml: (text) => {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    },

    // Formatear tiempo
    formatTime: (date) => {
      return date.toLocaleTimeString(config.language === 'es' ? 'es-ES' : 'en-US', {
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    // Detectar dispositivo móvil
    isMobile: () => {
      return window.innerWidth <= 768;
    },

    // Reproducir sonido
    playSound: () => {
      if (!config.enableSounds) return;
      
      const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT');
      audio.volume = 0.3;
      audio.play().catch(() => {});
    },

    // Almacenamiento local
    storage: {
      set: (key, value) => {
        try {
          localStorage.setItem(`versaai_${key}`, JSON.stringify(value));
        } catch (e) {}
      },
      get: (key) => {
        try {
          const item = localStorage.getItem(`versaai_${key}`);
          return item ? JSON.parse(item) : null;
        } catch (e) {
          return null;
        }
      },
      remove: (key) => {
        try {
          localStorage.removeItem(`versaai_${key}`);
        } catch (e) {}
      }
    }
  };

  // API
  const api = {
    // Inicializar sesión
    initSession: async () => {
      try {
        const response = await fetch(`${config.apiUrl}/widget/session`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            widgetId: config.widgetId,
            url: window.location.href,
            userAgent: navigator.userAgent
          })
        });
        
        const data = await response.json();
        sessionId = data.sessionId;
        
        // Cargar mensajes previos si existen
        if (data.messages) {
          messages = data.messages;
          renderMessages();
        }
        
        return data;
      } catch (error) {
        console.error('Error initializing session:', error);
        return null;
      }
    },

    // Enviar mensaje
    sendMessage: async (message) => {
      try {
        const response = await fetch(`${config.apiUrl}/widget/message`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            sessionId: sessionId,
            message: message,
            timestamp: new Date().toISOString()
          })
        });
        
        const data = await response.json();
        return data;
      } catch (error) {
        console.error('Error sending message:', error);
        return {
          success: false,
          error: 'Error de conexión. Por favor, inténtalo de nuevo.'
        };
      }
    }
  };

  // Renderizado
  const render = {
    // Crear estilos CSS
    createStyles: () => {
      const styles = `
        .versaai-widget {
          position: fixed;
          z-index: 999999;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          font-size: 14px;
          line-height: 1.4;
        }
        
        .versaai-widget * {
          box-sizing: border-box;
        }
        
        .versaai-widget-button {
          width: ${config.size === 'small' ? '50px' : config.size === 'large' ? '70px' : '60px'};
          height: ${config.size === 'small' ? '50px' : config.size === 'large' ? '70px' : '60px'};
          background-color: ${config.primaryColor};
          border: none;
          border-radius: ${config.buttonShape === 'circle' ? '50%' : config.buttonShape === 'rounded' ? '12px' : '0'};
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          transition: all 0.3s ease;
          position: relative;
        }
        
        .versaai-widget-button:hover {
          transform: scale(1.05);
          box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }
        
        .versaai-widget-button svg {
          width: 24px;
          height: 24px;
          fill: white;
        }
        
        .versaai-notification-badge {
          position: absolute;
          top: -5px;
          right: -5px;
          background: #EF4444;
          color: white;
          border-radius: 50%;
          width: 20px;
          height: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 11px;
          font-weight: 600;
          animation: versaai-pulse 2s infinite;
        }
        
        @keyframes versaai-pulse {
          0% { transform: scale(1); }
          50% { transform: scale(1.1); }
          100% { transform: scale(1); }
        }
        
        .versaai-chat-container {
          width: ${utils.isMobile() ? '100vw' : '350px'};
          height: ${utils.isMobile() ? '100vh' : Math.min(config.maxHeight, 600) + 'px'};
          background: white;
          border-radius: ${utils.isMobile() ? '0' : '12px'};
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          position: ${utils.isMobile() ? 'fixed' : 'absolute'};
          ${utils.isMobile() ? 'top: 0; left: 0;' : 'bottom: 80px; right: 0;'}
          animation: versaai-slideUp 0.3s ease-out;
        }
        
        @keyframes versaai-slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .versaai-chat-header {
          background: ${config.primaryColor};
          color: white;
          padding: 16px;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        
        .versaai-chat-header-info {
          display: flex;
          align-items: center;
        }
        
        .versaai-chat-avatar {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          margin-right: 12px;
          background: rgba(255, 255, 255, 0.2);
          display: flex;
          align-items: center;
          justify-content: center;
        }
        
        .versaai-chat-avatar img {
          width: 100%;
          height: 100%;
          border-radius: 50%;
          object-fit: cover;
        }
        
        .versaai-chat-title {
          font-weight: 600;
          font-size: 16px;
        }
        
        .versaai-chat-status {
          font-size: 12px;
          opacity: 0.8;
        }
        
        .versaai-chat-close {
          background: none;
          border: none;
          color: white;
          cursor: pointer;
          padding: 4px;
          border-radius: 4px;
          transition: background-color 0.2s;
        }
        
        .versaai-chat-close:hover {
          background: rgba(255, 255, 255, 0.1);
        }
        
        .versaai-chat-messages {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
          background: #F9FAFB;
        }
        
        .versaai-message {
          margin-bottom: 16px;
          display: flex;
          align-items: flex-start;
        }
        
        .versaai-message.user {
          flex-direction: row-reverse;
        }
        
        .versaai-message-avatar {
          width: 28px;
          height: 28px;
          border-radius: 50%;
          margin: 0 8px;
          flex-shrink: 0;
        }
        
        .versaai-message-content {
          max-width: 70%;
          padding: 12px 16px;
          border-radius: 18px;
          word-wrap: break-word;
        }
        
        .versaai-message.bot .versaai-message-content {
          background: white;
          color: ${config.textColor};
          border-bottom-left-radius: 4px;
        }
        
        .versaai-message.user .versaai-message-content {
          background: ${config.primaryColor};
          color: white;
          border-bottom-right-radius: 4px;
        }
        
        .versaai-message-time {
          font-size: 11px;
          color: #6B7280;
          margin-top: 4px;
          text-align: center;
        }
        
        .versaai-typing-indicator {
          display: flex;
          align-items: center;
          padding: 12px 16px;
          background: white;
          border-radius: 18px;
          border-bottom-left-radius: 4px;
          margin-bottom: 16px;
          max-width: 70%;
        }
        
        .versaai-typing-dots {
          display: flex;
          align-items: center;
        }
        
        .versaai-typing-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #9CA3AF;
          margin: 0 2px;
          animation: versaai-typing 1.4s infinite;
        }
        
        .versaai-typing-dot:nth-child(2) {
          animation-delay: 0.2s;
        }
        
        .versaai-typing-dot:nth-child(3) {
          animation-delay: 0.4s;
        }
        
        @keyframes versaai-typing {
          0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.4;
          }
          30% {
            transform: translateY(-10px);
            opacity: 1;
          }
        }
        
        .versaai-chat-input {
          padding: 16px;
          background: white;
          border-top: 1px solid #E5E7EB;
        }
        
        .versaai-input-container {
          display: flex;
          align-items: center;
          background: #F3F4F6;
          border-radius: 24px;
          padding: 4px;
        }
        
        .versaai-input-field {
          flex: 1;
          border: none;
          background: none;
          padding: 12px 16px;
          outline: none;
          font-size: 14px;
          resize: none;
          max-height: 100px;
        }
        
        .versaai-send-button {
          width: 36px;
          height: 36px;
          border-radius: 50%;
          background: ${config.primaryColor};
          border: none;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background-color 0.2s;
        }
        
        .versaai-send-button:hover {
          background: ${config.primaryColor}dd;
        }
        
        .versaai-send-button:disabled {
          background: #D1D5DB;
          cursor: not-allowed;
        }
        
        .versaai-send-button svg {
          width: 16px;
          height: 16px;
          fill: white;
        }
        
        .versaai-quick-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin-top: 12px;
        }
        
        .versaai-quick-action {
          background: #E5E7EB;
          border: none;
          border-radius: 16px;
          padding: 6px 12px;
          font-size: 12px;
          cursor: pointer;
          transition: background-color 0.2s;
        }
        
        .versaai-quick-action:hover {
          background: #D1D5DB;
        }
        
        .versaai-powered-by {
          padding: 8px 16px;
          background: #F9FAFB;
          border-top: 1px solid #E5E7EB;
          text-align: center;
          font-size: 11px;
          color: #6B7280;
        }
        
        .versaai-powered-by a {
          color: ${config.primaryColor};
          text-decoration: none;
          font-weight: 500;
        }
        
        /* Posicionamiento */
        .versaai-widget.bottom-right {
          bottom: 20px;
          right: 20px;
        }
        
        .versaai-widget.bottom-left {
          bottom: 20px;
          left: 20px;
        }
        
        .versaai-widget.top-right {
          top: 20px;
          right: 20px;
        }
        
        .versaai-widget.top-left {
          top: 20px;
          left: 20px;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
          .versaai-widget {
            bottom: 10px;
            right: 10px;
          }
          
          .versaai-chat-container {
            width: 100vw;
            height: 100vh;
            border-radius: 0;
            position: fixed;
            top: 0;
            left: 0;
          }
        }
      `;
      
      const styleSheet = document.createElement('style');
      styleSheet.textContent = styles;
      document.head.appendChild(styleSheet);
    },

    // Crear estructura HTML
    createHTML: () => {
      const html = `
        <div class="versaai-widget-button" id="versaai-toggle">
          <svg viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
          </svg>
          ${config.showNotifications ? '<div class="versaai-notification-badge" id="versaai-badge" style="display: none;">0</div>' : ''}
        </div>
        
        <div class="versaai-chat-container" id="versaai-chat" style="display: none;">
          <div class="versaai-chat-header">
            <div class="versaai-chat-header-info">
              <div class="versaai-chat-avatar">
                ${config.avatarUrl ? 
                  `<img src="${config.avatarUrl}" alt="${config.botName}">` : 
                  '<svg width="16" height="16" viewBox="0 0 24 24" fill="white"><path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>'
                }
              </div>
              <div>
                <div class="versaai-chat-title">${config.botName}</div>
                <div class="versaai-chat-status">En línea</div>
              </div>
            </div>
            <button class="versaai-chat-close" id="versaai-close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>
          
          <div class="versaai-chat-messages" id="versaai-messages"></div>
          
          <div class="versaai-chat-input">
            <div class="versaai-input-container">
              <textarea 
                id="versaai-input" 
                class="versaai-input-field" 
                placeholder="${config.inputPlaceholder}"
                rows="1"
              ></textarea>
              <button class="versaai-send-button" id="versaai-send">
                <svg viewBox="0 0 24 24">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                </svg>
              </button>
            </div>
            
            ${config.predefinedMessages.length > 0 ? `
              <div class="versaai-quick-actions" id="versaai-quick-actions">
                ${config.predefinedMessages.map(msg => 
                  `<button class="versaai-quick-action" data-message="${utils.escapeHtml(msg.text)}">${utils.escapeHtml(msg.text)}</button>`
                ).join('')}
              </div>
            ` : ''}
          </div>
          
          ${config.showPoweredBy ? `
            <div class="versaai-powered-by">
              Powered by <a href="https://versaai.com" target="_blank">VersaAI</a>
            </div>
          ` : ''}
        </div>
      `;
      
      return html;
    },

    // Renderizar mensajes
    renderMessages: () => {
      if (!messagesContainer) return;
      
      messagesContainer.innerHTML = '';
      
      // Mensaje de bienvenida
      if (messages.length === 0) {
        addMessage({
          type: 'bot',
          content: config.welcomeMessage,
          timestamp: new Date()
        }, false);
      }
      
      // Renderizar mensajes existentes
      messages.forEach(message => {
        addMessage(message, false);
      });
      
      // Indicador de escritura
      if (isTyping) {
        showTypingIndicator();
      }
      
      scrollToBottom();
    }
  };

  // Funciones de mensajes
  const addMessage = (message, save = true) => {
    if (!messagesContainer) return;
    
    const messageEl = document.createElement('div');
    messageEl.className = `versaai-message ${message.type}`;
    
    const avatarEl = document.createElement('div');
    avatarEl.className = 'versaai-message-avatar';
    
    if (message.type === 'bot') {
      if (config.avatarUrl) {
        avatarEl.innerHTML = `<img src="${config.avatarUrl}" alt="${config.botName}">`;
      } else {
        avatarEl.style.background = config.primaryColor;
        avatarEl.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="white"><path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>';
      }
    } else {
      avatarEl.style.background = '#6B7280';
      avatarEl.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="white"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>';
    }
    
    const contentEl = document.createElement('div');
    contentEl.className = 'versaai-message-content';
    contentEl.innerHTML = utils.escapeHtml(message.content);
    
    const timeEl = document.createElement('div');
    timeEl.className = 'versaai-message-time';
    timeEl.textContent = utils.formatTime(new Date(message.timestamp));
    
    messageEl.appendChild(avatarEl);
    messageEl.appendChild(contentEl);
    messageEl.appendChild(timeEl);
    
    messagesContainer.appendChild(messageEl);
    
    if (save) {
      messages.push(message);
      utils.storage.set('messages', messages);
    }
    
    scrollToBottom();
  };

  const showTypingIndicator = () => {
    if (!messagesContainer) return;
    
    // Remover indicador existente
    const existing = messagesContainer.querySelector('.versaai-typing-indicator');
    if (existing) existing.remove();
    
    const typingEl = document.createElement('div');
    typingEl.className = 'versaai-typing-indicator';
    typingEl.innerHTML = `
      <div class="versaai-typing-dots">
        <div class="versaai-typing-dot"></div>
        <div class="versaai-typing-dot"></div>
        <div class="versaai-typing-dot"></div>
      </div>
    `;
    
    messagesContainer.appendChild(typingEl);
    scrollToBottom();
  };

  const hideTypingIndicator = () => {
    if (!messagesContainer) return;
    
    const typingEl = messagesContainer.querySelector('.versaai-typing-indicator');
    if (typingEl) typingEl.remove();
  };

  const scrollToBottom = () => {
    if (!messagesContainer) return;
    
    setTimeout(() => {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 100);
  };

  // Funciones de interacción
  const sendMessage = async (content) => {
    if (!content.trim()) return;
    
    // Agregar mensaje del usuario
    addMessage({
      type: 'user',
      content: content,
      timestamp: new Date()
    });
    
    // Limpiar input
    if (inputField) {
      inputField.value = '';
      inputField.style.height = 'auto';
    }
    
    // Mostrar indicador de escritura
    isTyping = true;
    showTypingIndicator();
    
    // Enviar a la API
    const response = await api.sendMessage(content);
    
    // Ocultar indicador de escritura
    isTyping = false;
    hideTypingIndicator();
    
    // Agregar respuesta del bot
    if (response && response.success) {
      addMessage({
        type: 'bot',
        content: response.message || 'Gracias por tu mensaje. Te responderé pronto.',
        timestamp: new Date()
      });
      
      utils.playSound();
    } else {
      addMessage({
        type: 'bot',
        content: response?.error || 'Lo siento, ha ocurrido un error. Por favor, inténtalo de nuevo.',
        timestamp: new Date()
      });
    }
  };

  const toggleWidget = () => {
    if (!chatContainer) return;
    
    isOpen = !isOpen;
    
    if (isOpen) {
      chatContainer.style.display = 'flex';
      if (inputField) inputField.focus();
      
      // Resetear contador de no leídos
      unreadCount = 0;
      updateNotificationBadge();
      
      // Marcar como visto
      utils.storage.set('lastSeen', new Date().toISOString());
    } else {
      chatContainer.style.display = 'none';
    }
  };

  const updateNotificationBadge = () => {
    if (!notificationBadge || !config.showNotifications) return;
    
    if (unreadCount > 0) {
      notificationBadge.textContent = unreadCount > 99 ? '99+' : unreadCount.toString();
      notificationBadge.style.display = 'flex';
    } else {
      notificationBadge.style.display = 'none';
    }
  };

  // Event listeners
  const attachEventListeners = () => {
    // Toggle widget
    const toggleBtn = document.getElementById('versaai-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleWidget);
    }
    
    // Cerrar chat
    const closeBtn = document.getElementById('versaai-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', toggleWidget);
    }
    
    // Enviar mensaje
    const sendBtn = document.getElementById('versaai-send');
    if (sendBtn) {
      sendBtn.addEventListener('click', () => {
        if (inputField) sendMessage(inputField.value);
      });
    }
    
    // Input field
    inputField = document.getElementById('versaai-input');
    if (inputField) {
      // Auto-resize
      inputField.addEventListener('input', (e) => {
        e.target.style.height = 'auto';
        e.target.style.height = Math.min(e.target.scrollHeight, 100) + 'px';
      });
      
      // Enter para enviar
      inputField.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          sendMessage(inputField.value);
        }
      });
    }
    
    // Acciones rápidas
    const quickActions = document.getElementById('versaai-quick-actions');
    if (quickActions) {
      quickActions.addEventListener('click', (e) => {
        if (e.target.classList.contains('versaai-quick-action')) {
          const message = e.target.getAttribute('data-message');
          if (message) sendMessage(message);
        }
      });
    }
    
    // Cerrar con Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isOpen) {
        toggleWidget();
      }
    });
  };

  // Inicialización
  const init = async () => {
    // Verificar que no esté ya inicializado
    if (document.getElementById('versaai-widget-container')) {
      return;
    }
    
    // Crear estilos
    render.createStyles();
    
    // Crear contenedor principal
    widgetContainer = document.createElement('div');
    widgetContainer.id = 'versaai-widget-container';
    widgetContainer.className = `versaai-widget ${config.position}`;
    widgetContainer.innerHTML = render.createHTML();
    
    // Agregar al DOM
    document.body.appendChild(widgetContainer);
    
    // Obtener referencias
    chatContainer = document.getElementById('versaai-chat');
    messagesContainer = document.getElementById('versaai-messages');
    notificationBadge = document.getElementById('versaai-badge');
    
    // Adjuntar event listeners
    attachEventListeners();
    
    // Cargar mensajes guardados
    const savedMessages = utils.storage.get('messages');
    if (savedMessages) {
      messages = savedMessages;
    }
    
    // Renderizar mensajes
    render.renderMessages();
    
    // Inicializar sesión
    if (config.widgetId) {
      await api.initSession();
    }
    
    // Auto-abrir si está configurado
    if (config.autoOpen) {
      setTimeout(() => {
        if (!isOpen) toggleWidget();
      }, config.autoOpenDelay * 1000);
    }
    
    // Simular mensaje no leído para demo
    setTimeout(() => {
      if (!isOpen && config.showNotifications) {
        unreadCount = 1;
        updateNotificationBadge();
      }
    }, 10000);
  };

  // API pública
  window.VersaAI = {
    init: init,
    open: () => {
      if (!isOpen) toggleWidget();
    },
    close: () => {
      if (isOpen) toggleWidget();
    },
    sendMessage: sendMessage,
    config: config
  };

  // Auto-inicializar cuando el DOM esté listo
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();