import clr

clr.AddReference("System.Windows.Forms")
clr.AddReference("Ironpython.Wpf")
# from pyrevit import script
import wpf
from System import Windows


class WarningWindow(Windows.Window):
    def __init__(self, xaml_file, label_text, text_content):
        wpf.LoadComponent(self, xaml_file)
        self.label.Content = label_text
        self.txtBlock.Text = text_content

    def window_close(self, sender, args):
        self.Close()
