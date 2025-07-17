<template>
  <div class="agentforce-container">
    <!-- Video Call Interface -->
    <div class="video-call-section">
      <div class="video-call-card">
        <div class="call-header">
          <div class="salesforce-logo">
            <svg viewBox="0 0 24 24" class="logo-icon">
              <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
            </svg>
            <span>Salesforce</span>
          </div>
          <div class="call-controls">
            <button class="control-btn">📌</button>
            <button class="control-btn">✕</button>
          </div>
        </div>
        
        <div class="search-bar">
          <input type="text" placeholder="🔍 Search" class="search-input">
          <button class="search-btn">+</button>
          <button class="menu-btn">☰</button>
        </div>
        
        <div class="call-info">
          <div class="call-title">
            <div class="call-icon">📅</div>
            <div class="call-details">
              <h3>Negotiation Call</h3>
              <p>Joyce Turner • 8/6/2024 • 12:30 PM</p>
            </div>
          </div>
          
          <div class="deal-info">
            <span class="deal-label">Welo - $25K New Business</span>
            <button class="expand-btn">⌄</button>
          </div>
        </div>
        
        <div class="video-area">
          <div class="participant-video">
            <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=200&fit=crop&crop=face" alt="AI Assistant" class="ai-video">
          </div>
          <div class="participant-video">
            <img src="https://images.unsplash.com/photo-1494790108755-2616b612b786?w=300&h=200&fit=crop&crop=face" alt="Joyce Turner" class="user-video">
          </div>
        </div>
        
        <div class="call-controls-bottom">
          <button class="control-btn mute">🎤</button>
          <button class="control-btn video">📹</button>
          <button class="control-btn chat">💬</button>
          <button class="control-btn screen">📺</button>
          <button class="control-btn emoji">😊</button>
        </div>
        
        <div class="insights-panel">
          <div class="insights-header">
            <span class="insights-title">Real Time Insights</span>
            <span class="status-badge active">Active</span>
            <button class="insights-toggle">✓</button>
          </div>
          
          <div class="notification-card">
            <div class="notification-icon">🔔</div>
            <div class="notification-content">
              <h4>Negotiation Suggestion</h4>
              <p>Consider offering the 15% Sprint Discount to close the deal fast.</p>
              <span class="timestamp">1 min ago</span>
              <button class="transcript-btn">Transcript</button>
            </div>
          </div>
          
          <div class="navigation-controls">
            <button class="nav-btn">‹</button>
            <span class="page-indicator">02/02</span>
            <button class="nav-btn">›</button>
          </div>
          
          <div class="action-buttons">
            <button class="action-btn summarize">🔍 Summarize</button>
            <button class="action-btn explore">🔍 Explore</button>
          </div>
          
          <div class="tabs-section">
            <div class="tab-buttons">
              <button class="tab-btn active">Participants</button>
              <button class="tab-btn">Notes</button>
              <button class="tab-btn">Transcripts</button>
            </div>
            
            <div class="participants-content">
              <h4>Participants</h4>
              <div class="participant-item">
                <span class="participant-label">Outside your Organization (1)</span>
                <div class="participant-info">
                  <img src="https://images.unsplash.com/photo-1494790108755-2616b612b786?w=32&h=32&fit=crop&crop=face" alt="Joyce Turner" class="participant-avatar">
                  <div class="participant-details">
                    <span class="participant-name">Joyce Turner</span>
                    <span class="participant-role">Procurement Head</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Agentforce Selection Interface -->
    <div class="agentforce-selection">
      <div class="selection-card">
        <div class="agentforce-header">
          <div class="agentforce-logo">
            <div class="robot-mascot">🤖</div>
            <h2>Agentforce</h2>
          </div>
          
          <div class="steps-indicator">
            <span class="step-label">Steps</span>
            <div class="step-circle">1</div>
            <span class="step-text">Select Type</span>
          </div>
        </div>
        
        <div class="agent-options">
          <div class="agent-option customer-support">
            <div class="option-icon">🎧</div>
            <span class="option-label">Customer Support</span>
          </div>
          
          <div class="agent-option sales-coach">
            <div class="option-icon">🎯</div>
            <span class="option-label">Sales Coach</span>
          </div>
          
          <div class="agent-option sales-development">
            <div class="option-icon">📈</div>
            <span class="option-label">Sales Development</span>
          </div>
        </div>
        
        <div class="mascot-characters">
          <div class="mascot left-mascot">🤖</div>
          <div class="mascot right-mascot">🦾</div>
        </div>
      </div>
    </div>

    <!-- Dreamforce Chat Interface -->
    <div class="dreamforce-chat">
      <div class="chat-card">
        <div class="chat-header">
          <h3>Ask Astro</h3>
        </div>
        
        <div class="chat-messages">
          <div class="message ai-message">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <div class="message-bubble ai-bubble">
                Hi! I'm your guide to Dreamforce.
              </div>
            </div>
          </div>
          
          <div class="message user-message">
            <div class="message-content">
              <div class="message-bubble user-bubble">
                I'm looking for some sessions on emerging AI trends. Can you please help me find some?
              </div>
            </div>
            <div class="message-avatar user-avatar">
              <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&crop=face" alt="User">
            </div>
          </div>
          
          <div class="message ai-message">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <div class="message-bubble ai-bubble">
                <p>Sure thing! Check these sessions out:</p>
                
                <div class="session-cards">
                  <div class="session-card">
                    <h4>Services Industry & Service: Preparing for the Future of AI</h4>
                    <div class="session-time">
                      <span>Sept 18</span>
                      <span>4:00 PM - 5:00 PM</span>
                    </div>
                  </div>
                  
                  <div class="session-card">
                    <h4>High Tech & Service: Preparing for the Future of AI</h4>
                    <div class="session-time">
                      <span>Sept 18</span>
                      <span>1:30 PM - 2:30 PM</span>
                    </div>
                  </div>
                </div>
                
                <p>Let me know which ones you are interested in, and I can add them to your schedule!</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chat-input">
          <div class="input-container">
            <input type="text" placeholder="Type your message..." class="chat-input-field">
            <button class="send-button">🤖</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('Participants')
const isInsightsActive = ref(true)

console.log('🚀 AgentforceChat cargado - Interfaz de chat AI profesional')
</script>

<style scoped>
.agentforce-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #f0f4ff 0%, #e6f3ff 100%);
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Video Call Section */
.video-call-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.call-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.salesforce-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #0176d3;
  font-weight: 600;
}

.logo-icon {
  width: 1.5rem;
  height: 1.5rem;
}

.call-controls {
  display: flex;
  gap: 0.5rem;
}

.control-btn {
  width: 2rem;
  height: 2rem;
  border: none;
  background: #f3f4f6;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.search-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  outline: none;
}

.search-btn,
.menu-btn {
  width: 2rem;
  height: 2rem;
  border: none;
  background: #f3f4f6;
  border-radius: 0.5rem;
  cursor: pointer;
}

.call-info {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.call-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.call-icon {
  width: 2.5rem;
  height: 2.5rem;
  background: #e0e7ff;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.call-details h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.call-details p {
  margin: 0.25rem 0 0 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.deal-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f9fafb;
  padding: 0.75rem;
  border-radius: 0.5rem;
}

.deal-label {
  font-weight: 500;
  color: #374151;
}

.expand-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1rem;
}

.video-area {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
}

.participant-video {
  aspect-ratio: 16/9;
  border-radius: 0.5rem;
  overflow: hidden;
  background: #e5e7eb;
}

.ai-video,
.user-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.call-controls-bottom {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.control-btn.mute,
.control-btn.video,
.control-btn.chat,
.control-btn.screen,
.control-btn.emoji {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  border: none;
  cursor: pointer;
}

.insights-panel {
  padding: 1rem;
}

.insights-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.insights-title {
  font-weight: 600;
  color: #1f2937;
}

.status-badge {
  background: #10b981;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.insights-toggle {
  width: 1.5rem;
  height: 1.5rem;
  border: none;
  background: #3b82f6;
  color: white;
  border-radius: 0.25rem;
  cursor: pointer;
}

.notification-card {
  background: #f0f9ff;
  border: 1px solid #0ea5e9;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  gap: 0.75rem;
}

.notification-icon {
  font-size: 1.25rem;
}

.notification-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
}

.notification-content p {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.4;
}

.timestamp {
  font-size: 0.75rem;
  color: #6b7280;
  margin-right: 1rem;
}

.transcript-btn {
  background: transparent;
  border: 1px solid #3b82f6;
  color: #3b82f6;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  cursor: pointer;
}

.navigation-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.nav-btn {
  width: 2rem;
  height: 2rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.25rem;
  cursor: pointer;
}

.page-indicator {
  font-size: 0.875rem;
  color: #6b7280;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.action-btn {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.875rem;
}

.tabs-section {
  border-top: 1px solid #e5e7eb;
  padding-top: 1rem;
}

.tab-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tab-btn {
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: #6b7280;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.875rem;
}

.tab-btn.active {
  background: #3b82f6;
  color: white;
}

.participants-content h4 {
  margin: 0 0 0.75rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
}

.participant-label {
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
  display: block;
}

.participant-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.participant-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: cover;
}

.participant-name {
  font-weight: 500;
  color: #1f2937;
  display: block;
  font-size: 0.875rem;
}

.participant-role {
  color: #6b7280;
  font-size: 0.75rem;
}

/* Agentforce Selection */
.selection-card {
  background: linear-gradient(135deg, #a855f7, #ec4899);
  border-radius: 1rem;
  padding: 2rem;
  color: white;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(168, 85, 247, 0.3);
}

.agentforce-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.agentforce-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.robot-mascot {
  font-size: 2rem;
}

.agentforce-logo h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.steps-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
}

.step-circle {
  width: 1.5rem;
  height: 1.5rem;
  background: white;
  color: #a855f7;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
}

.step-label,
.step-text {
  font-size: 0.875rem;
  font-weight: 500;
}

.agent-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.agent-option {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 1rem;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.agent-option:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.option-icon {
  width: 2.5rem;
  height: 2.5rem;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.option-label {
  font-size: 1rem;
  font-weight: 500;
}

.mascot-characters {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  padding: 0 2rem;
  pointer-events: none;
}

.mascot {
  font-size: 3rem;
  opacity: 0.3;
}

/* Dreamforce Chat */
.chat-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 600px;
}

.chat-header {
  background: #f8fafc;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  text-align: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.message-content {
  flex: 1;
  max-width: 80%;
}

.message-bubble {
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  line-height: 1.4;
}

.ai-bubble {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border-bottom-left-radius: 0.25rem;
}

.user-bubble {
  background: #f3f4f6;
  color: #1f2937;
  border-bottom-right-radius: 0.25rem;
}

.session-cards {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 1rem 0;
}

.session-card {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.5rem;
  padding: 1rem;
}

.session-card h4 {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  font-weight: 600;
}

.session-time {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  opacity: 0.9;
}

.chat-input {
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.input-container {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.chat-input-field {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  outline: none;
  font-size: 0.875rem;
}

.send-button {
  width: 2.5rem;
  height: 2.5rem;
  border: none;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .agentforce-container {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
  
  .video-area {
    grid-template-columns: 1fr;
  }
  
  .call-controls-bottom {
    gap: 0.5rem;
  }
  
  .agent-options {
    gap: 0.75rem;
  }
  
  .chat-card {
    height: 500px;
  }
}
</style>