document.addEventListener('DOMContentLoaded', () => {
  const socket = io.connect('http://' + document.domain + ':' + location.port);
  const messageInput = document.getElementById('message-input');
  const chatHistory = document.getElementById('chat-history');
  const chatForm = document.getElementById('chat-form');
  const spinner = document.getElementById('spinner');

  function appendMessage(message) {
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.textContent = message;
    messageContainer.appendChild(messageElement);
    chatHistory.appendChild(messageContainer);
    chatHistory.scrollTop = chatHistory.scrollHeight;
  }

  chatForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const message = messageInput.value;
    messageInput.value = '';
    socket.emit('message', message);
    spinner.style.display = 'block';
  });

  socket.on('response', (data) => {
    spinner.style.display = 'none';
    const message = data.message;
    appendMessage(message);
  });
});
