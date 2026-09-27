document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('text-input');
    const charCount = document.getElementById('char-count');
    const wordCount = document.getElementById('word-count');
    const summarizeBtn = document.getElementById('summarize-btn');
    const clearBtn = document.getElementById('clear-btn');
    const loadingSection = document.getElementById('loading');
    const errorSection = document.getElementById('error-message');
    const resultSection = document.getElementById('result-section');
    const summaryOutput = document.getElementById('summary-output');

    // Update counts
    textInput.addEventListener('input', () => {
        const text = textInput.value;
        const chars = text.length;
        const words = text.trim() === '' ? 0 : text.trim().split(/\s+/).length;
        
        charCount.textContent = `${chars} characters`;
        wordCount.textContent = `${words} words`;
        
        errorSection.classList.add('hidden');
    });

    // Clear input
    clearBtn.addEventListener('click', () => {
        textInput.value = '';
        textInput.dispatchEvent(new Event('input'));
        resultSection.classList.add('hidden');
        errorSection.classList.add('hidden');
    });

    // Handle summarization
    summarizeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        
        if (!text) {
            showError("Please enter some text to summarize.");
            return;
        }

        // UI State: Loading
        summarizeBtn.disabled = true;
        loadingSection.classList.remove('hidden');
        resultSection.classList.add('hidden');
        errorSection.classList.add('hidden');

        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'An error occurred during summarization.');
            }

            // Success
            displaySummary(data.summary);

        } catch (error) {
            showError(error.message);
        } finally {
            // UI State: Done Loading
            summarizeBtn.disabled = false;
            loadingSection.classList.add('hidden');
        }
    });

    function showError(message) {
        errorSection.textContent = message;
        errorSection.classList.remove('hidden');
        resultSection.classList.add('hidden');
    }

    function displaySummary(summaryText) {
        // Basic Markdown-like parsing for bullet points and paragraphs
        let html = summaryText;
        
        // Convert markdown bullet points to HTML
        if (html.includes('- ') || html.includes('* ')) {
            const lines = html.split('\n');
            let inList = false;
            let formattedHtml = '';
            
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i].trim();
                const isBullet = line.startsWith('- ') || line.startsWith('* ');
                
                if (isBullet && !inList) {
                    formattedHtml += '<ul>';
                    inList = true;
                } else if (!isBullet && inList && line !== '') {
                    formattedHtml += '</ul>';
                    inList = false;
                }
                
                if (isBullet) {
                    formattedHtml += `<li>${line.substring(2)}</li>`;
                } else if (line !== '') {
                    formattedHtml += `<p>${line}</p>`;
                }
            }
            
            if (inList) {
                formattedHtml += '</ul>';
            }
            
            summaryOutput.innerHTML = formattedHtml;
        } else {
            // Just wrap in paragraph if no bullet points
            summaryOutput.innerHTML = `<p>${html.replace(/\n/g, '<br>')}</p>`;
        }
        
        resultSection.classList.remove('hidden');
    }
});
