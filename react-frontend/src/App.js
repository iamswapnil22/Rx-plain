import React, { useState, useRef, useEffect } from 'react';
import styled, { createGlobalStyle } from 'styled-components';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

const API_URL = 'http://localhost:8000/api';

const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    background-color: #0f1419;
    color: #e6e6e6;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }
`;

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  background-color: #0f1419;
`;

const Sidebar = styled.div`
  width: 260px;
  background-color: #1a1f2e;
  border-right: 1px solid #2d3748;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  
  @media (max-width: 768px) {
    width: ${props => props.isOpen ? '260px' : '0'};
    position: fixed;
    z-index: 1000;
    height: 100vh;
  }
`;

const SidebarHeader = styled.div`
  padding: 16px;
  border-bottom: 1px solid #2d3748;
`;

const NewChatButton = styled.button`
  width: 100%;
  padding: 12px 16px;
  background-color: transparent;
  border: 1px solid #4299e1;
  border-radius: 8px;
  color: #e6e6e6;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: background-color 0.2s;

  &:hover {
    background-color: #2b6cb0;
  }

  svg {
    width: 16px;
    height: 16px;
  }
`;

const ChatHistory = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 8px;
`;

const ChatItem = styled.div`
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #e6e6e6;
  margin-bottom: 2px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: background-color 0.2s;

  &:hover {
    background-color: #2d3748;
  }

  &.active {
    background-color: #4299e1;
  }

  svg {
    width: 16px;
    height: 16px;
    opacity: 0.7;
  }
`;

const SidebarFooter = styled.div`
  padding: 16px;
  border-top: 1px solid #2d3748;
`;

const SettingsButton = styled.button`
  width: 100%;
  padding: 8px 12px;
  background-color: transparent;
  border: none;
  border-radius: 8px;
  color: #e6e6e6;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: background-color 0.2s;

  &:hover {
    background-color: #2d3748;
  }

  svg {
    width: 16px;
    height: 16px;
  }
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
`;

const Header = styled.div`
  padding: 16px 24px;
  border-bottom: 1px solid #2d3748;
  background-color: #0f1419;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const HeaderTitle = styled.h1`
  font-size: 20px;
  font-weight: 600;
  color: #e6e6e6;
  margin: 0;
`;

const MobileMenuButton = styled.button`
  display: none;
  background: none;
  border: none;
  color: #e6e6e6;
  cursor: pointer;
  padding: 8px;

  @media (max-width: 768px) {
    display: block;
  }

  svg {
    width: 20px;
    height: 20px;
  }
`;

const ChatArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 0;
  scroll-behavior: smooth;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    background-color: #565869;
    border-radius: 3px;
  }
`;

const MessageWrapper = styled.div`
  padding: 24px;
  background-color: ${props => props.isUser ? '#0f1419' : '#1a1f2e'};
  border-bottom: 1px solid rgba(255,255,255,0.1);
`;

const MessageContent = styled.div`
  max-width: 768px;
  margin: 0 auto;
  display: flex;
  gap: 20px;
  align-items: flex-start;
`;

const Avatar = styled.div`
  width: 30px;
  height: 30px;
  border-radius: 4px;
  background-color: ${props => props.isUser ? '#4299e1' : '#48bb78'};
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
  font-weight: bold;
  font-size: 14px;
`;

const MessageBubble = styled.div`
  flex-grow: 1;
  font-size: 16px;
  line-height: 1.6;
  color: #e6e6e6;
  
  pre {
    margin: 1em 0;
    padding: 16px;
    background-color: #1a1f2e !important;
    border-radius: 8px;
    overflow-x: auto;
    border: 1px solid #2d3748;
  }

  code {
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    background-color: rgba(255,255,255,0.1);
    padding: 2px 4px;
    border-radius: 3px;
  }

  p {
    margin: 0 0 1em 0;
    &:last-child {
      margin-bottom: 0;
    }
  }

  ul, ol {
    margin: 0.5em 0;
    padding-left: 1.5em;
  }

  li {
    margin: 0.25em 0;
  }
`;

const MessageActions = styled.div`
  display: flex;
  gap: 8px;
  margin-top: 12px;
  opacity: 0;
  transition: opacity 0.2s;

  ${MessageWrapper}:hover & {
    opacity: 1;
  }
`;

const ActionButton = styled.button`
  background: none;
  border: none;
  color: #a0a0a0;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: background-color 0.2s;

  &:hover {
    background-color: rgba(255,255,255,0.1);
    color: #e6e6e6;
  }

  svg {
    width: 14px;
    height: 14px;
  }
`;

const InputContainer = styled.div`
  padding: 24px;
  background: linear-gradient(180deg, rgba(15,20,25,0) 0%, #0f1419 50%);
  border-top: 1px solid #2d3748;
`;

const InputWrapper = styled.div`
  max-width: 768px;
  margin: 0 auto;
  position: relative;
`;

const ModelSelector = styled.div`
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
`;

const ModelButton = styled.button`
  padding: 6px 12px;
  background-color: ${props => props.active ? '#48bb78' : 'transparent'};
  border: 1px solid ${props => props.active ? '#48bb78' : '#555555'};
  border-radius: 8px;
  color: #e6e6e6;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background-color: ${props => props.active ? '#48bb78' : '#2d3748'};
  }
`;

const InputBox = styled.textarea`
  width: 100%;
  padding: 16px 45px 16px 16px;
  border-radius: 12px;
  border: 1px solid #555555;
  background-color: #1a1f2e;
  color: #e6e6e6;
  font-size: 16px;
  line-height: 1.5;
  resize: none;
  outline: none;
  max-height: 200px;
  transition: border-color 0.3s;
  
  &:focus {
    border-color: #48bb78;
  }

  &::placeholder {
    color: #a0a0a0;
  }
`;

const SendButton = styled.button`
  position: absolute;
  right: 10px;
  bottom: 10px;
  padding: 6px;
  background: none;
  border: none;
  color: ${props => props.disabled ? '#555555' : '#e6e6e6'};
  cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
  transition: color 0.3s;
  border-radius: 6px;

  &:hover:not(:disabled) {
    background-color: rgba(255,255,255,0.1);
  }

  svg {
    width: 20px;
    height: 20px;
  }
`;

const TypingIndicator = styled.div`
  display: flex;
  gap: 4px;
  padding: 12px 0;
  
  span {
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background-color: #e6e6e6;
    animation: bounce 1.4s infinite ease-in-out;
    
    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
  }

  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
`;

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  z-index: 999;
  display: ${props => props.isOpen ? 'block' : 'none'};

  @media (min-width: 769px) {
    display: none;
  }
`;

const ApiKeyModal = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #1a1f2e;
  border: 1px solid #2d3748;
  border-radius: 12px;
  padding: 24px;
  width: 90%;
  max-width: 500px;
  z-index: 1001;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
`;

const ModalTitle = styled.h2`
  color: #e6e6e6;
  margin: 0 0 16px 0;
  font-size: 18px;
  font-weight: 600;
`;

const ApiKeyInput = styled.input`
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #2d3748;
  background-color: #0f1419;
  color: #e6e6e6;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
  margin-bottom: 16px;

  &:focus {
    border-color: #4299e1;
  }

  &::placeholder {
    color: #a0a0a0;
  }
`;

const ModalButton = styled.button`
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  margin-right: 12px;

  &.primary {
    background-color: #4299e1;
    color: white;

    &:hover {
      background-color: #2b6cb0;
    }
  }

  &.secondary {
    background-color: transparent;
    color: #e6e6e6;
    border: 1px solid #2d3748;

    &:hover {
      background-color: #2d3748;
    }
  }
`;

const MedicalIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: #4299e1;
  border-radius: 8px;
  margin-right: 12px;

  svg {
    width: 24px;
    height: 24px;
    color: white;
  }
`;

const ImageUploadButton = styled.button`
  background: transparent;
  color: #48bb78;
  border: 2px dashed #48bb78;
  border-radius: 8px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;

  svg {
    width: 18px;
    height: 18px;
  }

  &:hover {
    background: #48bb78;
    color: white;
    border-color: #48bb78;
  }
`;

const ImagePreview = styled.div`
  position: relative;
  display: inline-block;
  margin: 8px 0;
  
  img {
    max-width: 100px;
    max-height: 75px;
    border-radius: 8px;
    border: 2px solid #48bb78;
  }
`;

const RemoveImageButton = styled.button`
  position: absolute;
  top: -8px;
  right: -8px;
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;

  &:hover {
    background: #c53030;
    transform: scale(1.1);
  }
`;

const FileInput = styled.input`
  display: none;
`;

const ImageUploadContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
`;

const WelcomeMessage = styled.div`
  text-align: center;
  color: #a0a0a0;
  font-size: 16px;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
`;

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [selectedModel, setSelectedModel] = useState("gemini");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showApiKeyModal, setShowApiKeyModal] = useState(false);
  const [apiKey, setApiKey] = useState(localStorage.getItem('openai_api_key') || '');
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
const [selectedImage, setSelectedImage] = useState(null);
const [imagePreview, setImagePreview] = useState(null);
  
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    loadConversations();
  }, []);

  const handleInputChange = (e) => {
    setInput(e.target.value);
    adjustTextareaHeight();
  };

  const adjustTextareaHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px';
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = input.trim();
    setInput("");
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }

    // Create new chat if none exists
    if (!currentChatId) {
      const newChatId = Date.now();
      setCurrentChatId(newChatId);
      setChatHistory(prev => [{
        id: newChatId,
        title: userMessage.substring(0, 50) + (userMessage.length > 50 ? '...' : ''),
        timestamp: new Date()
      }, ...prev]);
    }

    setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
    setIsTyping(true);

    try {
      // Create FormData for image upload
      const formData = new FormData();
      formData.append('prompt', userMessage);
      formData.append('model', 'gemini');
      formData.append('conversation_id', currentChatId);
      
      // Add image if selected
      if (selectedImage) {
        formData.append('image', selectedImage);
      }
      
      const response = await axios.post(`${API_URL}/chat`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setIsTyping(false);
      setMessages(prev => [...prev, { text: response.data.response, isUser: false }]);
      
      // Clear image after successful send
      if (selectedImage) {
        setSelectedImage(null);
        setImagePreview(null);
      }
      
      // Update conversation ID if it's a new conversation
      if (!currentChatId) {
        setCurrentChatId(response.data.conversation_id);
      }
      
      // Reload conversations to update sidebar
      await loadConversations();
    } catch (error) {
      console.error("Error in sending message:", error);
      setIsTyping(false);
      
      // Handle specific error cases
      let errorMessage = "I apologize, but I'm having trouble connecting to the server. Please try again later.";
      
      if (error.response?.status === 400 && error.response?.data?.detail?.includes("API key")) {
        errorMessage = "Please add your OpenAI API key in the settings to use GPT model.";
        setShowApiKeyModal(true);
      } else if (error.response?.status === 401) {
        errorMessage = "Invalid API key. Please check your OpenAI API key in the settings.";
        setShowApiKeyModal(true);
      } else if (error.response?.status === 429) {
        errorMessage = "Rate limit exceeded. Please try again later.";
      }
      
      setMessages(prev => [...prev, { 
        text: errorMessage, 
        isUser: false 
      }]);
    }
  };

  const newChat = () => {
    setMessages([]);
    setCurrentChatId(null);
    setSidebarOpen(false);
    setSelectedImage(null);
    setImagePreview(null);
  };

  const selectChat = async (chatId) => {
    try {
      const response = await axios.get(`${API_URL}/conversations/${chatId}`);
      setMessages(response.data.messages.map(msg => ({
        text: msg.content,
        isUser: msg.role === 'user'
      })));
      setCurrentChatId(chatId);
      setSelectedModel(response.data.model);
      setSidebarOpen(false);
    } catch (error) {
      console.error("Error loading conversation:", error);
    }
  };

  const loadConversations = async () => {
    try {
      const response = await axios.get(`${API_URL}/conversations`);
      setChatHistory(response.data);
    } catch (error) {
      console.error("Error loading conversations:", error);
    }
  };

  const deleteConversation = async (chatId) => {
    try {
      await axios.delete(`${API_URL}/conversations/${chatId}`);
      await loadConversations();
      if (currentChatId === chatId) {
        setMessages([]);
        setCurrentChatId(null);
      }
    } catch (error) {
      console.error("Error deleting conversation:", error);
    }
  };

  const copyMessage = (text) => {
    navigator.clipboard.writeText(text);
  };

  const regenerateResponse = () => {
    // Remove the last AI message and regenerate
    const lastUserMessage = messages.filter(m => m.isUser).pop();
    if (lastUserMessage) {
      setMessages(prev => prev.filter((_, index) => index < prev.length - 1));
      setInput(lastUserMessage.text);
    }
  };

  // Removed model selection and API key handling

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
      }
      
      // Validate file size (5MB limit)
      if (file.size > 5 * 1024 * 1024) {
        alert('Image size must be less than 5MB');
        return;
      }
      
      setSelectedImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setSelectedImage(null);
    setImagePreview(null);
  };

  const renderMessage = (msg) => (
    <ReactMarkdown
      components={{
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || '');
          return !inline && match ? (
            <SyntaxHighlighter
              language={match[1]}
              style={vscDarkPlus}
              PreTag="div"
              {...props}
            >
              {String(children).replace(/\n$/, '')}
            </SyntaxHighlighter>
          ) : (
            <code className={className} {...props}>
              {children}
            </code>
          );
        }
      }}
    >
      {msg.text}
    </ReactMarkdown>
  );

  return (
    <>
      <GlobalStyle />
      <AppContainer>
        <Overlay isOpen={sidebarOpen} onClick={() => setSidebarOpen(false)} />
        <Sidebar isOpen={sidebarOpen}>
          <SidebarHeader>
            <NewChatButton onClick={newChat}>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              New chat
            </NewChatButton>
          </SidebarHeader>
          
          <ChatHistory>
            {chatHistory.map(chat => (
              <ChatItem 
                key={chat.id}
                className={currentChatId === chat.id ? 'active' : ''}
                onClick={() => selectChat(chat.id)}
                style={{ position: 'relative' }}
              >
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
                <span style={{ flex: 1 }}>{chat.title}</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteConversation(chat.id);
                  }}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#a0a0a0',
                    cursor: 'pointer',
                    padding: '2px',
                    borderRadius: '4px',
                    opacity: 0,
                    transition: 'opacity 0.2s'
                  }}
                  onMouseEnter={(e) => e.target.style.opacity = 1}
                  onMouseLeave={(e) => e.target.style.opacity = 0}
                >
                  <svg width="12" height="12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </ChatItem>
            ))}
          </ChatHistory>
          
          <SidebarFooter>
            <SettingsButton>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Settings
            </SettingsButton>
          </SidebarFooter>
        </Sidebar>

        <MainContent>
                  <Header>
          <MobileMenuButton onClick={() => setSidebarOpen(!sidebarOpen)}>
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </MobileMenuButton>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <MedicalIcon>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </MedicalIcon>
            <HeaderTitle>Rxplain - Medical AI Assistant</HeaderTitle>
          </div>
          <div></div>
        </Header>

          <ChatArea>
            {messages.length === 0 && (
              <div style={{ 
                display: 'flex', 
                flexDirection: 'column',
                alignItems: 'center', 
                justifyContent: 'center', 
                height: '100%',
                padding: '40px'
              }}>
                <MedicalIcon style={{ marginBottom: '24px' }}>
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                  </svg>
                </MedicalIcon>
                <WelcomeMessage>
                  <h2 style={{ color: '#e6e6e6', marginBottom: '16px' }}>Welcome to Rxplain</h2>
                  <p style={{ marginBottom: '16px' }}>
                    Your AI-powered medical assistant for understanding prescriptions, medications, and health information.
                  </p>
                  <p style={{ fontSize: '14px', color: '#a0a0a0' }}>
                    Ask me about any medication, its side effects, interactions, or usage instructions.
                  </p>
                </WelcomeMessage>
              </div>
            )}
            
            {messages.map((msg, index) => (
              <MessageWrapper key={index} isUser={msg.isUser}>
                <MessageContent>
                  <Avatar isUser={msg.isUser}>
                    {msg.isUser ? 'U' : 'A'}
                  </Avatar>
                  <div style={{ flexGrow: 1 }}>
                    <MessageBubble>
                      {renderMessage(msg)}
                    </MessageBubble>
                    {!msg.isUser && (
                      <MessageActions>
                        <ActionButton onClick={() => copyMessage(msg.text)}>
                          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                          </svg>
                          Copy
                        </ActionButton>
                        <ActionButton onClick={regenerateResponse}>
                          <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                          </svg>
                          Regenerate
                        </ActionButton>
                      </MessageActions>
                    )}
                  </div>
                </MessageContent>
              </MessageWrapper>
            ))}
            
            {isTyping && (
              <MessageWrapper isUser={false}>
                <MessageContent>
                  <Avatar isUser={false}>A</Avatar>
                  <TypingIndicator>
                    <span></span>
                    <span></span>
                    <span></span>
                  </TypingIndicator>
                </MessageContent>
              </MessageWrapper>
            )}
            <div ref={messagesEndRef} />
          </ChatArea>

          <InputContainer>
            <InputWrapper>
              {/* Removed model selector */}
              
              <ImageUploadContainer>
                <ImageUploadButton onClick={() => document.getElementById('image-upload').click()}>
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Upload Prescription Image
                </ImageUploadButton>
                <FileInput
                  id="image-upload"
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                />
                
                {imagePreview && (
                  <ImagePreview>
                    <img src={imagePreview} alt="Preview" />
                    <RemoveImageButton onClick={removeImage}>
                      ×
                    </RemoveImageButton>
                  </ImagePreview>
                )}
              </ImageUploadContainer>
              
              <InputBox
                ref={textareaRef}
                value={input}
                onChange={handleInputChange}
                onKeyDown={handleKeyPress}
                placeholder="Message Rxplain... (e.g., 'What medications are in this prescription?')"
                rows={1}
              />
              <SendButton 
                onClick={sendMessage}
                disabled={!input.trim()}
              >
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </SendButton>
            </InputWrapper>
          </InputContainer>
        </MainContent>
      </AppContainer>

      {showApiKeyModal && (
        <>
          <Overlay isOpen={true} onClick={() => setShowApiKeyModal(false)} />
        </>
      )}
    </>
  );
}

export default App;
