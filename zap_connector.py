from zapv2 import ZAPv2

class ZAPConnector:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        if base_url:
            self.zap = ZAPv2(apikey=api_key, proxies={"http": base_url, "https": base_url})
        else:
            self.zap = None

    def start_scan(self, target: str):
        if not self.zap:
            raise RuntimeError("ZAP not configured")
        return self.zap.ascan.scan(target)

    def scan_status(self, scan_id: str):
        if not self.zap:
            raise RuntimeError("ZAP not configured")
        return self.zap.ascan.status(scan_id)

    def get_alerts(self, baseurl=None, start=0, count=50):
        if not self.zap:
            raise RuntimeError("ZAP not configured")
        return self.zap.core.alerts(baseurl, start, count)
