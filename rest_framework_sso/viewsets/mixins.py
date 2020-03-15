class MetaExtractorMixin:
    """
    Viewset helper for extracting and storing request metadata in model
    """

    def get_ip_address(self):
        remote_addr_header = self.request.headers.get("REMOTE_ADDR", '')
        if remote_addr_header:
            return remote_addr_header.split(',')[0].strip()
        return self.request.headers.get("HTTP_X_FORWARDED_FOR", '').split(",")[0].strip()

    def get_user_agent(self):
        return self.request.headers.get("User-Agent", "")[:1000]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({
            'ip_address': self.get_ip_address(),
            'user_agent': self.get_user_agent()
        })
        return ctx
