import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

// Styled Components
const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 80vh;
  width: 100%;
  max-width: 600px;
  margin: 20px auto;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const MessageContainer = styled.div`
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 10px;
`;

const MessageBubble = styled.div`
  background-color: ${props => (props.isUser ? '#007bff' : '#e5e5e5')};
  color: ${props => (props.isUser ? '#fff' : '#000')};
  max-width: 80%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 20px;
  align-self: ${props => (props.isUser ? 'flex-end' : 'flex-start')};
  word-wrap: break-word;
`;

const InputContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const InputBox = styled.input`
  width: 80%;
  padding: 10px;
  border-radius: 20px;
  border: 1px solid #ccc;
  font-size: 16px;
`;

const SendButton = styled.button`
  padding: 10px 20px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 20px;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }
`;

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (input.trim() === "") return;

    // Add user message to the chat
    setMessages([...messages, { text: input, isUser: true }]);

    // Call OpenAI API or handle backend logic here
    try {
      const response = await axios.post('/api/chat', { message: input });

      setMessages(prevMessages => [
        ...prevMessages,
        { text: input, isUser: true },
        { text: response.data.reply, isUser: false },
      ]);
    } catch (error) {
      console.error("Error in sending message:", error);
    }
    
    // Clear input field
    setInput("");
  };

  return (
    <ChatContainer>
      <MessageContainer>
        {messages.map((msg, index) => (
          <MessageBubble key={index} isUser={msg.isUser}>
            {msg.text}
          </MessageBubble>
        ))}
      </MessageContainer>

      <InputContainer>
        <InputBox
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message"
        />
        <SendButton onClick={sendMessage}>Send</SendButton>
      </InputContainer>
    </ChatContainer>
  );
}

export default App;
