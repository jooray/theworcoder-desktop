# main.py
import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.clipboard import Clipboard
from kivy.uix.boxlayout import BoxLayout

# Import the worcoder functions
from worcoder.encoding import (
    mnemonic_to_str,
    str_to_mnemonic,
    ChecksumError,
    # words_to_str,  # Not explicitly needed if you only use mnemonic_to_str
)
# We also expect ValueError if an invalid word is encountered in the mnemonic.

class MainWidget(BoxLayout):
    pass


class TheWorcoderApp(App):
    data_text = StringProperty("")
    mnemonic_text = StringProperty("")

    def build(self):
        self.title = "TheWorcoder"
        # Load from KV file
        root = Builder.load_file("theworcoder.kv")
        return root

    def encode_data(self):
        """
        Takes whatever is in the Data textarea,
        encodes it as a mnemonic,
        puts the result into the Mnemonic textarea,
        and copies the mnemonic to clipboard.
        """
        data = self.root.ids.data_text.text.strip()
        if not data:
            return
        # Encode data
        mnemonic = str_to_mnemonic(data)
        self.root.ids.mnemonic_text.text = mnemonic
        # Copy to clipboard
        Clipboard.copy(mnemonic)

    def decode_data(self):
        """
        Takes the mnemonic in the Mnemonic textarea,
        decodes it into data,
        puts the result into the Data textarea,
        and copies the data to clipboard.
        """
        mnemonic = self.root.ids.mnemonic_text.text.strip()
        if not mnemonic:
            return
        try:
            # Decode mnemonic
            data = mnemonic_to_str(mnemonic)
            self.root.ids.data_text.text = data
            # Copy to clipboard
            Clipboard.copy(data)
        except ChecksumError:
            # If invalid checksum, let’s show an error
            error_msg = "** Error: invalid mnemonic or checksum! **"
            self.root.ids.data_text.text = error_msg
            Clipboard.copy(error_msg)
        except ValueError as e:
            # This catches invalid words, e.g., "Invalid mnemonic word: 'maslo'"
            error_msg = str(e)
            self.root.ids.data_text.text = error_msg
            Clipboard.copy(error_msg)


if __name__ == "__main__":
    TheWorcoderApp().run()
