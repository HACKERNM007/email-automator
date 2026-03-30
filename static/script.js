document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('emailForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notificationMessage');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Hide previous notifications
        notification.classList.add('hidden');
        notification.classList.remove('success', 'error');
        
        // Set loading state
        submitBtn.disabled = true;
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');
        
        // Gather Data
        const data = {
            host: document.getElementById('host').value,
            port: document.getElementById('port').value,
            address: document.getElementById('address').value,
            password: document.getElementById('password').value,
            subject: document.getElementById('subject').value,
            template: document.getElementById('template').value,
            contacts: document.getElementById('contacts').value
        };

        try {
            const response = await fetch('/api/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            // Show result
            notificationMessage.innerHTML = result.message.replace(/\n/g, '<br>');
            notification.classList.remove('hidden');
            
            if (result.success) {
                notification.classList.add('success');
            } else {
                notification.classList.add('error');
            }
            
        } catch (error) {
            notificationMessage.textContent = "A network error occurred: " + error.message;
            notification.classList.remove('hidden');
            notification.classList.add('error');
        } finally {
            // Reset loading state
            submitBtn.disabled = false;
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });
});
