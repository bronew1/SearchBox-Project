self.addEventListener('push', function(event) {
    const data = event.data.text();

    const options = {
        body: data,
        icon: '/favicon.ico',
        badge: '/favicon.ico'
    };

    event.waitUntil(
        self.registration.showNotification("Sina Pırlanta", options)
    );
});
