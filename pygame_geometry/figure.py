class Figure:
    def __init__(self,forms,color=WHITE):
        """Create a figure object."""
        self.forms=forms
        self.color=color
    def show(self,window):
        """Show segments."""
        for form in self.forms:
            form.show(window)
