#-*-encoding:utf-8-*-

import win32serviceutil
import win32service
import win32event
import threading

from rsassistant import sign_service


class RSAssistantService(win32serviceutil.ServiceFramework):

    _svc_name_ = "RSsign"
    _svc_display_name_ = "RS Sign Service"
    _svc_description_ = "用来自动到rs签到"

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        t = threading.Thread(target=sign_service)
        t.start()

        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)