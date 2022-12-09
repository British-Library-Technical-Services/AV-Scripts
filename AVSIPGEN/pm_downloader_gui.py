# This script will download Process Metadata from a source SIP in .json format 
# The json file can be used as a local reference SIP in the Excel Batch Upload spreadsheet
# The script is written with a GUI
# A compiled stand-alone version is available to downloaded from [url]
# The script requires config.py to run

import config
import urllib3
import wx
import requests
import json
import os
import time

# Mutes SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GUI framework
class MainFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER | wx.STAY_ON_TOP, title="Process Metadata Downloader", size=(180, 225))
        panel = wx.Panel(self)

        self.URL = config.URL
        self.dl_loc = ''

        font = wx.Font(10, wx.DECORATIVE, wx.DEFAULT, wx.NORMAL)
        bold_font = wx.Font(12, wx.DECORATIVE, wx.BOLD, wx.NORMAL)

        src_text = wx.StaticText(panel, label='SIP ID')
        src_text.SetFont(font)

        self.src_id = wx.TextCtrl(panel, style=wx.TE_CENTRE, size=(115, 25))
        self.src_id.SetFont(font)

        button_location = wx.Button(panel, label='Set Directory', size=(120, 30))
        button_location.SetFont(font)

        button_download = wx.Button(panel, label='DOWNLOAD', size=(120, 50))
        button_download.SetFont(bold_font)

        v_box = wx.BoxSizer(wx.VERTICAL)
        v_box.Add(src_text, 0, wx.ALL | wx.CENTRE, 2)
        v_box.Add(self.src_id, 0, wx.BOTTOM | wx.CENTRE, 5)
        v_box.Add(button_location, 0, wx.ALL | wx.CENTRE, 5)
        v_box.Add(button_download, 0, wx.ALL | wx.CENTRE, 5)

        button_download.Bind(wx.EVT_BUTTON, self.download_pm)
        button_location.Bind(wx.EVT_BUTTON, self.set_dl_location) 
        
        
        panel.SetSizer(v_box)
        self.report = self.CreateStatusBar(1)
        self.Show()


    def set_dl_location(self, event):
        dlg = wx.DirDialog(self, 'Choose a Directory', style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.dl_loc = dlg.GetPath()       
        dlg.Destroy()
        self.report.PushStatusText(self.dl_loc)


    def download_pm(self, event):
        if os.path.isdir(self.dl_loc) is True:  
            self.sip_id = self.src_id.GetValue()
            src_url = '{}/SIP/{}'.format(self.URL, self.sip_id)
            response = requests.get(src_url, verify=False)
            
            if response.status_code == 200:
                self.report.PushStatusText('{}: SIP ID OKAY'.format(response.status_code))
                response.encoding = response.apparent_encoding
                pm_json = response.json()

                d = json.loads(pm_json['ProcessMetadata'])
                process_metadata = json.dumps(d)
                
                write_out = '{}_pm.json'.format(self.sip_id)
                save_location = os.path.join(self.dl_loc, write_out)
                with open(save_location, 'w') as pm:
                    pm.write(process_metadata)
                time.sleep(1)
                if os.path.exists(save_location) is True:
                    self.report.PushStatusText('SUCCESS. File downloaded')
                    time.sleep(1)
                self.report.PushStatusText(self.dl_loc)
            else:
                self.report.PushStatusText('{}: ERROR'.format(response.status_code))
                time.sleep(2)
                self.report.PushStatusText(self.dl_loc)
        else:
            self.report.PushStatusText('Set a download directory')


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
