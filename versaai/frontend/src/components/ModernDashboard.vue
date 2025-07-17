<template>
  <div class="modern-dashboard">
    <!-- Header Navigation -->
    <header class="dashboard-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" class="w-8 h-8">
              <path fill="currentColor" d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <h1 class="logo-text">VersaAI</h1>
        </div>
        
        <nav class="nav-tabs">
          <button class="nav-tab active">Voice</button>
          <button class="nav-tab">Slack</button>
          <button class="nav-tab">Flows & API</button>
          <button class="nav-tab">Apps & Mobile</button>
          <button class="nav-tab">Digital Channels</button>
          <button class="nav-tab">Robotics</button>
        </nav>
        
        <div class="user-section">
          <div class="user-avatar">
            <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=40&h=40&fit=crop&crop=face" alt="User" class="avatar-img">
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="dashboard-main">
      <!-- AI Assistant Cards -->
      <section class="ai-assistants">
        <div class="assistant-card einstein-card">
          <div class="card-header">
            <div class="assistant-avatar">
              <div class="robot-icon">
                🤖
              </div>
            </div>
            <div class="assistant-info">
              <h3>Einstein</h3>
              <p class="status-text">Hi Emma, how can I help you?</p>
            </div>
            <button class="minimize-btn">×</button>
          </div>
          
          <div class="chat-content">
            <div class="message user-message">
              <img src="https://images.unsplash.com/photo-1494790108755-2616b612b786?w=32&h=32&fit=crop&crop=face" alt="User" class="message-avatar">
              <div class="message-bubble">
                Are the order items associated with this case available from another shipping location?
              </div>
            </div>
            
            <div class="message ai-message">
              <div class="ai-avatar">🤖</div>
              <div class="message-bubble ai-bubble">
                Yes, the product items associated with the Store Opening Delay Case are available at our secondary fulfillment center in Portland Oregon.
              </div>
            </div>
            
            <div class="message user-message">
              <img src="https://images.unsplash.com/photo-1494790108755-2616b612b786?w=32&h=32&fit=crop&crop=face" alt="User" class="message-avatar">
              <div class="message-bubble">
                Can I modify this active order to ship from another distribution center?
              </div>
            </div>
          </div>
          
          <div class="chat-input">
            <input type="text" placeholder="Describe your task or ask a question..." class="input-field">
            <button class="send-btn">→</button>
          </div>
        </div>

        <!-- Second Einstein Card -->
        <div class="assistant-card einstein-card-2">
          <div class="card-header">
            <div class="assistant-avatar">
              <div class="robot-icon">🤖</div>
            </div>
            <div class="assistant-info">
              <h3>Einstein</h3>
              <p class="status-text">Hi Jake, how can I help you?</p>
            </div>
            <button class="minimize-btn">×</button>
          </div>
          
          <div class="opportunity-content">
            <div class="user-query">
              <img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=32&h=32&fit=crop&face" alt="User" class="message-avatar">
              <span>What is my top opportunity for today?</span>
            </div>
            
            <div class="ai-response">
              <div class="ai-avatar">🤖</div>
              <div class="opportunity-card">
                <p class="opportunity-text">Trailhead Outfitters - Eco Gear is the highest value open opportunity.</p>
                
                <div class="opportunity-details">
                  <div class="detail-item">
                    <span class="label">Account Name:</span>
                    <span class="value">Trailhead Supplies</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Stage:</span>
                    <span class="value">Proposal / Quote</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Amount:</span>
                    <span class="value">$100,000</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Close Date:</span>
                    <span class="value">10/29/23</span>
                  </div>
                  <div class="detail-item">
                    <span class="label">Opportunity Owner:</span>
                    <span class="value">Carrie Benes</span>
                  </div>
                </div>
                
                <button class="edit-record-btn">Edit Record</button>
              </div>
            </div>
          </div>
          
          <div class="chat-input">
            <input type="text" placeholder="Describe your task or ask a question..." class="input-field">
            <button class="send-btn">→</button>
          </div>
        </div>

        <!-- Sales Email Assistant -->
        <div class="assistant-card sales-card">
          <div class="card-header">
            <h3>Einstein Sales Emails</h3>
            <div class="card-tabs">
              <button class="tab-btn">Related</button>
              <button class="tab-btn active">Compose</button>
            </div>
          </div>
          
          <div class="sales-content">
            <p class="description">Use your sales data and generative AI to quickly draft your next email.</p>
            
            <button class="draft-btn">
              ✨ Draft with Einstein
            </button>
            
            <div class="action-list">
              <h4>What do you want to do?</h4>
              <ul class="actions">
                <li>Introduce Myself</li>
                <li>Send a Meeting Invite</li>
                <li>Nudge for Follow-Up</li>
                <li>Check In</li>
                <li>Reconnect</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Feature Grid -->
      <section class="feature-grid">
        <div class="feature-row">
          <div class="feature-card">
            <h3>Analyze against KPIs</h3>
            <p>Understand how it's working across all areas of your business</p>
          </div>
          <div class="feature-card">
            <h3>Monitor and Trace</h3>
            <p>Make sure guardrails are in place for both functionality and cost</p>
          </div>
          <div class="feature-card">
            <h3>Optimize with AI</h3>
            <p>Investigate issues and get proactive answers to make things better</p>
          </div>
          <div class="feature-card">
            <h3>Monitor Costs</h3>
            <p>Track consumption and cost and drill into specific usage reporting</p>
          </div>
        </div>
      </section>

      <!-- Usage Categories -->
      <section class="usage-categories">
        <div class="category-card">
          <h3>Customers</h3>
          <p>Engages directly with customers, prospects, and partners</p>
        </div>
        <div class="category-card">
          <h3>Employees</h3>
          <p>Working alongside internal teams, making everyone more effective</p>
        </div>
        <div class="category-card">
          <h3>Background</h3>
          <p>Behind-the-scenes, handling deep research and complexity at scale</p>
        </div>
      </section>

      <!-- Action Buttons -->
      <section class="action-buttons">
        <div class="action-btn-group">
          <button class="action-btn primary">
            <span class="btn-icon">🚀</span>
            <div class="btn-content">
              <h4>Build fast with AI</h4>
              <p>Rapidly build AI prompts and agents, enforce guardrails, and handle conversational flows using agent SDKs</p>
            </div>
          </button>
          
          <button class="action-btn secondary">
            <span class="btn-icon">🔗</span>
            <div class="btn-content">
              <h4>Connect tools and agents</h4>
              <p>Connect to 3rd party resources with the latest protocols like MCP and A2A</p>
            </div>
          </button>
          
          <button class="action-btn tertiary">
            <span class="btn-icon">🧪</span>
            <div class="btn-content">
              <h4>Test confidently with AI</h4>
              <p>Test agent behavior at scale, debug issues, and refine your agents before deployment</p>
            </div>
          </button>
          
          <button class="action-btn quaternary">
            <span class="btn-icon">📊</span>
            <div class="btn-content">
              <h4>Deploy and Optimize</h4>
              <p>Deploy agents, monitor behavior in real-time, and uncover performance insights to optimize agents</p>
            </div>
          </button>
        </div>
      </section>

      <!-- Core Principles -->
      <section class="core-principles">
        <div class="principle-card">
          <h3>Reasoning</h3>
          <p>Understand, decide, and act autonomously</p>
        </div>
        <div class="principle-card">
          <h3>Trust</h3>
          <p>Agent guardrails and protection</p>
        </div>
        <div class="principle-card">
          <h3>Performance</h3>
          <p>Low latency, model failover, hosted models</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('Voice')
const isMinimized = ref(false)

console.log('🎨 ModernDashboard cargado - Interfaz profesional activa')
</script>

<style scoped>
.modern-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Header Styles */
.dashboard-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 2rem;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 2rem;
  height: 2rem;
  color: white;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.nav-tabs {
  display: flex;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.25rem;
  border-radius: 2rem;
}

.nav-tab {
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
  border-radius: 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-tab.active,
.nav-tab:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.user-section {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Main Content */
.dashboard-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* AI Assistants */
.ai-assistants {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.assistant-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease;
}

.assistant-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.assistant-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.robot-icon {
  font-size: 1.25rem;
}

.assistant-info {
  flex: 1;
}

.assistant-info h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.status-text {
  margin: 0.25rem 0 0 0;
  font-size: 0.875rem;
  color: #6b7280;
}

.minimize-btn {
  width: 1.5rem;
  height: 1.5rem;
  border: none;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  color: #6b7280;
}

/* Chat Content */
.chat-content {
  padding: 1rem;
  max-height: 300px;
  overflow-y: auto;
}

.message {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  align-items: flex-start;
}

.message-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: cover;
}

.ai-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
}

.message-bubble {
  background: #f3f4f6;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  max-width: 280px;
  font-size: 0.875rem;
  line-height: 1.4;
}

.ai-bubble {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

/* Opportunity Content */
.opportunity-content {
  padding: 1rem;
}

.user-query {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  color: #374151;
}

.ai-response {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.opportunity-card {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 1rem;
  border-radius: 1rem;
  flex: 1;
}

.opportunity-text {
  margin: 0 0 1rem 0;
  font-weight: 500;
}

.opportunity-details {
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.label {
  font-weight: 500;
}

.edit-record-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Sales Card */
.sales-card .card-header {
  justify-content: space-between;
}

.card-tabs {
  display: flex;
  gap: 0.5rem;
}

.tab-btn {
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: #6b7280;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
}

.tab-btn.active {
  background: #667eea;
  color: white;
}

.sales-content {
  padding: 1rem;
}

.description {
  margin: 0 0 1rem 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.draft-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-list h4 {
  margin: 0 0 0.75rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.actions {
  list-style: none;
  padding: 0;
  margin: 0;
}

.actions li {
  padding: 0.5rem 0;
  color: #6b7280;
  font-size: 0.875rem;
  cursor: pointer;
}

.actions li:hover {
  color: #667eea;
}

/* Chat Input */
.chat-input {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.input-field {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  outline: none;
}

.send-btn {
  width: 2.5rem;
  height: 2.5rem;
  border: none;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
}

/* Feature Grid */
.feature-grid {
  margin-top: 2rem;
}

.feature-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.feature-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.feature-card p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
}

/* Usage Categories */
.usage-categories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.category-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.category-card h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.category-card p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
}

/* Action Buttons */
.action-buttons {
  margin-top: 2rem;
}

.action-btn-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.action-btn {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 1.5rem;
  border-radius: 1rem;
  cursor: pointer;
  text-align: left;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  transition: all 0.2s ease;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.btn-icon {
  font-size: 1.5rem;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.btn-content p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
}

/* Core Principles */
.core-principles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.principle-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.principle-card h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.principle-card p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-header {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav-tabs {
    overflow-x: auto;
    white-space: nowrap;
  }
  
  .dashboard-main {
    padding: 1rem;
  }
  
  .ai-assistants {
    grid-template-columns: 1fr;
  }
  
  .feature-row,
  .action-btn-group,
  .usage-categories,
  .core-principles {
    grid-template-columns: 1fr;
  }
}
</style>