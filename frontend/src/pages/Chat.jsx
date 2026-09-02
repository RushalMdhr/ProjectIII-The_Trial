import chatWithOllama from chatwithme.js

const Chat = () => {

  // In your React component
  const messages = [
    { role: 'system', content: 'You are a helpful assistant' },
    { role: 'user', content: 'Hello!' }
  ];

  const reply = chatWithOllama(messages);
  console.log(reply);  // "Hello! How can I help you?"
  return (
    <div>
      
    </div>
  )
}

export default Chat
