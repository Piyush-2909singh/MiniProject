
const chatContainer = document.getElementById('chat-container');
const chatForm = document.getElementById('chat-form');
const queryInput = document.getElementById('query');
const sendBtn = document.getElementById('send-btn');


let isLoading = false;
let lastRequestTime = 0;
const MIN_REQUEST_INTERVAL = 1200; // ms

function appendMessage(text, sender, sources = []) {
	const row = document.createElement('div');
	row.className = 'message-row';
	const bubble = document.createElement('div');
	bubble.className = 'bubble ' + sender;
	bubble.innerText = text;

	if (sender === 'ai' && Array.isArray(sources) && sources.length > 0) {
		const sourceLine = document.createElement('div');
		sourceLine.className = 'bubble-sources';
		sourceLine.innerText = 'Sources: ' + sources.join(', ');
		bubble.appendChild(sourceLine);
	}

	row.appendChild(bubble);
	chatContainer.appendChild(row);
	
	requestAnimationFrame(() => {
		chatContainer.scrollTop = chatContainer.scrollHeight;
	});
}

function setLoading(loading) {
	isLoading = loading;
	sendBtn.disabled = loading;
	queryInput.disabled = loading;
	if (loading) {
		
		const loadingBubbles = chatContainer.querySelectorAll('.bubble.ai-loading');
		loadingBubbles.forEach(b => b.parentElement.remove());
		appendMessage('Thinking...', 'ai-loading');
	} else {
		
		const loadingBubbles = chatContainer.querySelectorAll('.bubble.ai-loading');
		loadingBubbles.forEach(b => b.parentElement.remove());
	}
}

async function sendMessage() {
	const now = Date.now();
	if (now - lastRequestTime < MIN_REQUEST_INTERVAL) return; // Prevent rapid requests
	const question = queryInput.value.trim();
	if (!question || isLoading) return;
	appendMessage(question, 'user');
	queryInput.value = '';
	setLoading(true);
	lastRequestTime = now;
	let slowTimeout = setTimeout(() => {
		
		const loadingBubbles = chatContainer.querySelectorAll('.bubble.ai-loading');
		loadingBubbles.forEach(b => b.innerText = 'Still thinking...');
	}, 4000);
	try {
		const res = await fetch('/chat', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ message: question })
		});
		clearTimeout(slowTimeout);
		if (!res.ok) {
			let errorMsg = 'Network error';
			try {
				const errData = await res.json();
				errorMsg = errData.error || errorMsg;
			} catch (_e) {
				
			}
			throw new Error(errorMsg);
		}
		const data = await res.json();
		setLoading(false);
		appendMessage(
			data.response || data.answer || 'No response received.',
			'ai',
			Array.isArray(data.sources) ? data.sources : []
		);
	} catch (err) {
		clearTimeout(slowTimeout);
		setLoading(false);
		appendMessage('Error: ' + err.message, 'ai');
	}
}


queryInput.addEventListener('keydown', function(e) {
	if (e.key === 'Enter' && !e.shiftKey) {
		e.preventDefault();
		sendMessage();
	}
});


chatForm.addEventListener('submit', function(e) {
	e.preventDefault();
	sendMessage();
});