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
    background-color: #343541;
    color: #ECECF1;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  }
`;

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 20px;
`;

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: calc(100vh - 140px);
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  gap: 20px;
  padding: 0;
  background-color: transparent;
`;

const MessageContainer = styled.div`
  flex-grow: 1;
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
  display: flex;
  flex-direction: column;
  padding: 24px;
  background-color: ${props => props.isUser ? '#343541' : '#444654'};
  border-bottom: 1px solid rgba(255,255,255,0.1);
`;

const MessageContent = styled.div`
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  gap: 20px;
  align-items: flex-start;
`;

const Avatar = styled.div`
  width: 30px;
  height: 30px;
  border-radius: 2px;
  background-color: ${props => props.isUser ? '#5436DA' : '#11A37F'};
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
  line-height: 1.5;
  
  pre {
    margin: 1em 0;
    padding: 10px;
    background-color: #1e1e1e !important;
    border-radius: 6px;
    overflow-x: auto;
  }

  code {
    font-family: 'Fira Code', monospace;
    font-size: 14px;
  }

  p {
    margin: 0 0 1em 0;
    &:last-child {
      margin-bottom: 0;
    }
  }
`;

const InputContainer = styled.div`
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  padding: 24px;
  background: linear-gradient(180deg, rgba(52,53,65,0) 0%, #343541 50%);
`;

const InputWrapper = styled.div`
  display: flex;
  width: 100%;
  max-width: 800px;
  position: relative;
`;

const InputBox = styled.textarea`
  width: 100%;
  padding: 16px 45px 16px 16px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.2);
  background-color: #40414F;
  color: #ECECF1;
  font-size: 16px;
  line-height: 1.5;
  resize: none;
  outline: none;
  max-height: 200px;
  transition: border-color 0.3s;
  
  &:focus {
    border-color: rgba(255,255,255,0.4);
  }

  &::placeholder {
    color: rgba(255,255,255,0.5);
  }
`;

const SendButton = styled.button`
  position: absolute;
  right: 10px;
  bottom: 10px;
  padding: 6px;
  background: none;
  border: none;
  color: ${props => props.disabled ? '#565869' : '#ECECF1'};
  cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
  transition: color 0.3s;

  &:hover:not(:disabled) {
    color: white;
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
    background-color: #ECECF1;
    animation: bounce 1.4s infinite ease-in-out;
    
    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
  }

  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }
`;

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

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

    setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
    setIsTyping(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, { 
        prompt: userMessage,
        model: "gemini"  // using gemini model by default
      });
      setIsTyping(false);
      setMessages(prev => [...prev, { text: response.data.response, isUser: false }]);
    } catch (error) {
      console.error("Error in sending message:", error);
      setIsTyping(false);
      setMessages(prev => [...prev, { 
        text: "I apologize, but I'm having trouble connecting to the server. Please try again later.", 
        isUser: false 
      }]);
    }
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
        <ChatContainer>
          <MessageContainer>
            {messages.map((msg, index) => (
              <MessageWrapper key={index} isUser={msg.isUser}>
                <MessageContent>
                  <Avatar isUser={msg.isUser}>
                    {msg.isUser ? 'U' : 'A'}
                  </Avatar>
                  <MessageBubble>
                    {renderMessage(msg)}
                  </MessageBubble>
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
          </MessageContainer>

          <InputContainer>
            <InputWrapper>
              <InputBox
                ref={textareaRef}
                value={input}
                onChange={handleInputChange}
                onKeyDown={handleKeyPress}
                placeholder="Send a message..."
                rows={1}
              />
              <SendButton 
                onClick={sendMessage}
                disabled={!input.trim()}
              >
                <svg
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M7 11L12 6L17 11M12 18V7"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    transform="rotate(90 12 12)"
                  />
                </svg>
              </SendButton>
            </InputWrapper>
          </InputContainer>
        </ChatContainer>
      </AppContainer>
    </>
  );
}

export default App;
