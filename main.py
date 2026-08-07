import os
from kivy.app import App
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

import reader

# Import Plyer's native file chooser facade
from plyer import filechooser

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # A label to show which file was selected
        self.status_label = Label(
            text="No PDF file selected yet.",
            font_size='18sp',
            halign='center',
            valign='middle'
        )
        # Binds text sizing to make sure it wraps neatly on narrow phone screens
        self.status_label.bind(size=self.status_label.setter('text_size'))
        layout.add_widget(self.status_label)

        # The action button
        select_btn = Button(
            text="Open PDF File",
            font_size='20sp',
            size_hint_y=None,
            height=60,
            background_color=(0.1, 0.7, 0.3, 1) # Green accent button
        )
        select_btn.bind(on_press=self.check_permissions_and_open)
        layout.add_widget(select_btn)

        return layout

    def check_permissions_and_open(self, instance):
        """Checks if mobile storage permission is granted before launching the picker."""
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            # Ask the user for permission to read their stored files
            request_permissions(
                [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE], 
                callback=self.permission_callback
            )
        else:
            # If running locally on macOS for testing, jump straight to opening the picker
            self.open_pdf_picker()

    def permission_callback(self, permissions, grant_results):
        """Callback that fires immediately after user clicks Allow or Deny on Android."""
        # Check if permissions were accepted by the mobile user
        if all(grant_results):
            self.open_pdf_picker()
        else:
            self.status_label.text = "Permission denied. Cannot browse files."

    def open_pdf_picker(self):
        """Launches the system file picker looking exclusively for PDF files."""
        try:
            filechooser.open_file(
                title="Select a Sheet Music PDF",
                filters=[("PDF Files", "*.pdf")], # Explicitly isolate PDFs
                on_selection=self.handle_file_selection # Callback function
            )
        except Exception as e:
            self.status_label.text = f"Error opening picker: {str(e)}"

    def handle_file_selection(self, selection):
        """Triggers automatically when the user selects a file or cancels."""
        if not selection:
            self.status_label.text = "Selection cancelled by user."
            return

        # Selection returns a list containing the absolute file path string
        file_path = selection[0]
        file_name = os.path.basename(file_path)
        
        # Display the file details inside the user interface
        self.status_label.text = f"Success!\n\nSelected File: {file_name}\n\nFull Path: {file_path}"

if __name__ == '__main__':
    MainApp().run()
