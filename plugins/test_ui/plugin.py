class Plugin:
    name = "Test UI Plugin"
    version = "1.0.0"
    description = "A dummy plugin to verify the Dynamic Iframe UI System"
    has_ui = True
    icon = "Layout"
    admin_only = False

    def run(self, action_id, params, context):
        return {"status": "ok", "message": "Dummy action completed"}

    def stop(self, context=None):
        pass
