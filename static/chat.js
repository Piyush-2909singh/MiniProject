
const chatContainer = document.getElementById('chat-container');
const chatForm = document.getElementById('chat-form');
const queryInput = document.getElementById('query');
const sendBtn = document.getElementById('send-btn');
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');


let isLoading = false;
let lastRequestTime = 0;
const MIN_REQUEST_INTERVAL = 1200; // ms

function appendMessage(text, sender, sources = []) {
	const row = document.createElement('div');
	row.className = 'message-row ' + sender;
	const bubble = document.createElement('div');
	bubble.className = 'bubble ' + sender;
	bubble.innerText = text;

	row.appendChild(bubble);

	if (sender === 'ai' && Array.isArray(sources) && sources.length > 0) {
		const sourcesBox = document.createElement('div');
		sourcesBox.className = 'sources-box';

		const title = document.createElement('div');
		title.className = 'sources-title';
		title.innerText = 'Sources:';
		sourcesBox.appendChild(title);

		const list = document.createElement('div');
		list.className = 'sources-list';

		sources.forEach((source) => {
			const item = document.createElement('div');
			item.className = 'source-item';

			const doc = document.createElement('div');
			doc.className = 'source-doc';
			const docName = typeof source === 'string' ? source : (source.document || 'Unknown');
			doc.innerText = docName;

			item.appendChild(doc);

			if (typeof source !== 'string') {
				const snippets = Array.isArray(source.snippets) ? source.snippets : [];
				snippets.slice(0, 2).forEach((text) => {
					const snippet = document.createElement('div');
					snippet.className = 'source-snippet';
					snippet.innerText = `• ${text}`;
					item.appendChild(snippet);
				});
			}

			list.appendChild(item);
		});

		sourcesBox.appendChild(list);
		row.appendChild(sourcesBox);
	}
	chatContainer.appendChild(row);
	// Use requestAnimationFrame for smoother scroll
	requestAnimationFrame(() => {
		chatContainer.scrollTop = chatContainer.scrollHeight;
	});
}

function setLoading(loading) {
	isLoading = loading;
	sendBtn.disabled = loading;
	queryInput.disabled = loading;
	if (loading) {
		// Remove any existing loading bubble first
		const loadingBubbles = chatContainer.querySelectorAll('.bubble.ai-loading');
		loadingBubbles.forEach(b => b.parentElement.remove());
		appendMessage('Thinking...', 'ai-loading');
	} else {
		// Remove loading bubble
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
		// If still loading after 4s, update loading bubble
		const loadingBubbles = chatContainer.querySelectorAll('.bubble.ai-loading');
		loadingBubbles.forEach(b => b.innerText = 'Still thinking...');
	}, 4000);
	try {
		const res = await fetch('/chat', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
			},
			body: JSON.stringify({ message: question })
		});
		clearTimeout(slowTimeout);
		if (!res.ok) {
			let errorMsg = 'Network error';
			try {
				const errData = await res.json();
				errorMsg = errData.error || errorMsg;
			} catch (_e) {
				// Keep default message when response is not JSON.
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

// Submit on Enter
queryInput.addEventListener('keydown', function(e) {
	if (e.key === 'Enter' && !e.shiftKey) {
		e.preventDefault();
		sendMessage();
	}
});

// Submit on button click
chatForm.addEventListener('submit', function(e) {
	e.preventDefault();
	sendMessage();
});