#!/usr/bin/env python3
"""CLI mínimo para NiDeFlanders: activar/desactivar y cambiar país."""
import argparse
from application.vpn_service import VPNService

def main():
    p = argparse.ArgumentParser(description='CLI para NiDeFlanders')
    p.add_argument('accion', choices=['activar', 'desactivar', 'cambiar-pais', 'estado'], help='Acción a realizar')
    p.add_argument('--pais', '-p', help='Código ISO2 del país')
    args = p.parse_args()

    svc = VPNService()

    if args.accion == 'activar':
        ok = svc.activate()
        print('Activado' if ok else 'Error al activar')
    elif args.accion == 'desactivar':
        ok = svc.deactivate()
        print('Desactivado' if ok else 'Error al desactivar')
    elif args.accion == 'cambiar-pais':
        if not args.pais:
            print('Especifica el país con --pais (código ISO2)')
            raise SystemExit(2)
        ok = svc.change_country(args.pais)
        print('País cambiado' if ok else 'Error al cambiar país')
    elif args.accion == 'estado':
        print('Activo' if svc.is_active() else 'Inactivo')

if __name__ == '__main__':
    main()
