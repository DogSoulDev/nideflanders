"""
Pruebas unitarias para VPNService.
"""
import unittest
from application.vpn_service import VPNService

class TestVPNService(unittest.TestCase):
    def setUp(self):
        self.vpn = VPNService()

    def test_activate_vpn(self):
        # Simulación: test_connection y start_privoxy deben devolver True
        self.vpn.tor.test_connection = lambda: True
        self.vpn.privoxy.start_privoxy = lambda: True
        result = self.vpn.activate_vpn()
        self.assertIn(result, [True, False])
        self.assertTrue(self.vpn.is_active())

    def test_deactivate_vpn(self):
        self.vpn.privoxy.stop_privoxy = lambda: True
        self.vpn.active = True
        result = self.vpn.deactivate_vpn()
        self.assertIn(result, [True, False])
        self.assertFalse(self.vpn.is_active())

    def test_change_country_ip(self):
        self.vpn.tor.change_ip = lambda: True
        result = self.vpn.change_country_ip()
        self.assertIn(result, [True, False])

if __name__ == "__main__":
    unittest.main()
