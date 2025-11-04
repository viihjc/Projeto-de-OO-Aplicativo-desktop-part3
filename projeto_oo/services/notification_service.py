class NotificationService:
    def __init__(self):
        self.notifications_sent = []

    def notify(self, client_name, message):
        """Envia uma notificação simulada"""
        if not client_name or not message:
            raise ValueError("Nome do cliente e mensagem são obrigatórios.")
        
        notification = f"🔔 Notificação para {client_name}: {message}"
        self.notifications_sent.append(notification)
        print(notification)
        return notification
