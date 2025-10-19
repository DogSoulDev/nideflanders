#!/usr/bin/env python3
"""CLI mínimo para NiDeFlanders: activar/desactivar y cambiar país."""
import argparse
from application.vpn_service import VPNService


def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['activate', 'deactivate', 'change-country', 'status'])
    p.add_argument('--country', '-c')
    args = p.parse_args()

    svc = VPNService()

    if args.action == 'activate':
        ok = svc.activate()
        print('Activated' if ok else 'Failed to activate')
    elif args.action == 'deactivate':
        ok = svc.deactivate()
        print('Deactivated' if ok else 'Failed to deactivate')
    elif args.action == 'change-country':
        if not args.country:
            print('Specify --country ISO2 code')
            raise SystemExit(2)
        ok = svc.change_country(args.country)
        print('Changed' if ok else 'Failed')
    elif args.action == 'status':
        print('Active' if svc.is_active() else 'Inactive')


if __name__ == '__main__':
    main()
