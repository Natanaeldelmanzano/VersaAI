<template>
  <div class="api-testing-chat">
    <div class="header">
      <h1>API Testing Chat</h1>
      <p>Herramienta para probar y validar la API de VersaAI</p>
    </div>
    
    <div class="content">
      <div class="chat-section">
        <div class="logs" ref="logsContainer">
          <div v-for="(log, index) in logs" :key="index" :class="['log-entry', log.type]">
            <span class="timestamp">{{ formatTime(log.timestamp) }}</span>
            <span class="message">{{ log.message }}</span>
          </div>
        </div>
        
        <div class="input-section">
          <input 
            v-model="chatMessage" 
            @keyup.enter="sendChatMessage"
            placeholder="Escribe un mensaje o comando (/help para ayuda)"
            class="chat-input"
          />
          <button @click="sendChatMessage" class="send-btn">Enviar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const API_BASE_URL = 'http://localhost:8000'

const logs = ref([])
const chatMessage = ref('')
const logsContainer = ref(null)

const addLog = (type, data) => {
  logs.value.push({
    type,
    timestamp: new Date(),
    message: data.message || JSON.stringify(data),
    ...data
  })
  
  nextTick(() => {
    if (logsContainer.value) {
      logsContainer.value.scrollTop = logsContainer.value.scrollHeight
    }
  })
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString()
}

const checkApiStatus = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`)
    if (response.ok) {
      addLog('success', { message: '✅ API is running and healthy' })
    } else {
      addLog('error', { message: `API returned status: ${response.status}` })
    }
  } catch (error) {
    addLog('error', { message: `Failed to connect to API: ${error.message}` })
  }
}

const sendChatMessage = async () => {
  if (!chatMessage.value.trim()) return
  
  if (chatMessage.value.startsWith('/')) {
    handleCommand(chatMessage.value)
    chatMessage.value = ''
    return
  }
  
  const message = chatMessage.value
  chatMessage.value = ''
  
  const startTime = Date.now()
  
  try {
    addLog('request', {
      message: `Sending chat message: ${message.substring(0, 50)}...`
    })
    
    const response = await fetch(`${API_BASE_URL}/api/v1/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    })
    
    const responseTime = Date.now() - startTime
    
    if (response.ok) {
      const data = await response.json()
      addLog('success', {
        message: `🤖 AI Response (${responseTime}ms): ${data.response || data.message || 'No response'}`
      })
    } else {
      const errorData = await response.text()
      addLog('error', {
        message: `❌ Chat failed with status: ${response.status}`
      })
    }
  } catch (error) {
    addLog('error', {
      message: `❌ Chat failed: ${error.message}`
    })
  }
}

const handleCommand = (command) => {
  const cmd = command.toLowerCase().trim()
  
  switch (cmd) {
    case '/clear':
      logs.value = []
      addLog('chat', { message: '🧹 Logs cleared' })
      break
      
    case '/status':
      checkApiStatus()
      break
      
    case '/help':
      addLog('chat', {
        message: '📚 Available commands:\n/clear - Clear all logs\n/status - Check API status\n/help - Show this help'
      })
      break
      
    default:
      addLog('error', { message: `❌ Unknown command: ${command}. Type /help for available commands.` })
  }
}

onMounted(() => {
  checkApiStatus()
  addLog('chat', {
    message: '🚀 API Testing Chat iniciado. Usa /help para ver comandos disponibles.'
  })
})
</script>

<style scoped>
.api-testing-chat {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #1f2937;
  margin-bottom: 10px;
}

.header p {
  color: #6b7280;
}

.content {
  display: grid;
  gap: 20px;
}

.chat-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.logs {
  height: 400px;
  overflow-y: auto;
  padding: 20px;
  background: #f9fafb;
}

.log-entry {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 14px;
}

.log-entry.success {
  background: #d1fae5;
  color: #065f46;
}

.log-entry.error {
  background: #fee2e2;
  color: #991b1b;
}

.log-entry.request {
  background: #dbeafe;
  color: #1e40af;
}

.log-entry.chat {
  background: #f3e8ff;
  color: #7c3aed;
}

.timestamp {
  color: #6b7280;
  font-size: 12px;
  min-width: 80px;
}

.message {
  flex: 1;
  white-space: pre-wrap;
}

.input-section {
  display: flex;
  padding: 20px;
  gap: 10px;
  border-top: 1px solid #e5e7eb;
}

.chat-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}

.chat-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.send-btn {
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.send-btn:hover {
  background: #2563eb;
}
</style>