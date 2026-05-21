const chatArea = document.getElementById("chatArea");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

function addMessage(text, type){

  const div = document.createElement("div");

  div.className = type;

  div.innerText = text;

  chatArea.appendChild(div);

  chatArea.scrollTop = chatArea.scrollHeight;
}

async function sendMessage(){

  const message = input.value.trim();

  if(!message) return;

  addMessage(message, "user-msg");

  input.value = "";

  const response = await fetch("http://127.0.0.1:5000/chat",{

    method:"POST",

    headers:{
      "Content-Type":"application/json"
    },

    body:JSON.stringify({
      message:message
    })

  });

  const data = await response.json();

  addMessage(data.reply, "ai-msg");
}

sendBtn.addEventListener("click", sendMessage);