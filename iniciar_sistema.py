#!/usr/bin/env python3
"""
JSP ELÉTRICA - Inicializador do Sistema ERP
Automatiza a inicialização do servidor Flask e abre o navegador
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Exibe banner do sistema"""
    print("\n" + "="*80)
    print("   ██╗███████╗██████╗     ███████╗██╗     ███████╗████████╗██████╗ ██╗ ██████╗ █████╗")
    print("   ██║██╔════╝██╔══██╗    ██╔════╝██║     ██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝██╔══██╗")
    print("   ██║███████╗██████╔╝    █████╗  ██║     █████╗     ██║   ██████╔╝██║██║     ███████║")
    print("   ██║╚════██║██╔═══╝     ██╔══╝  ██║     ██╔══╝     ██║   ██╔══██╗██║██║     ██╔══██║")
    print("   ██║███████║██║         ███████╗███████╗███████╗   ██║   ██║  ██║██║╚██████╗██║  ██║")
    print("   ╚═╝╚══════╝╚═╝         ╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝")
    print("\n                     Sistema ERP - Gestão de Ordens de Serviço")
    print("="*80)

def check_environment():
    """Verifica se o ambiente está configurado corretamente"""
    print("\n[INFO] Verificando ambiente...")
    
    # Verificar se está no diretório correto
    if not os.path.exists('run.py'):
        print("[ERRO] Arquivo run.py não encontrado!")
        print("       Certifique-se de executar este script no diretório do projeto.")
        return False
    
    # Verificar ambiente virtual
    venv_path = Path('.venv')
    if not venv_path.exists():
        print("[ERRO] Ambiente virtual não encontrado!")
        print("       Execute: python -m venv .venv")
        return False
    
    # Verificar ativador do ambiente virtual
    if os.name == 'nt':  # Windows
        activate_script = venv_path / 'Scripts' / 'activate.bat'
        python_exe = venv_path / 'Scripts' / 'python.exe'
    else:  # Linux/Mac
        activate_script = venv_path / 'bin' / 'activate'
        python_exe = venv_path / 'bin' / 'python'
    
    if not activate_script.exists():
        print(f"[ERRO] Script de ativação não encontrado: {activate_script}")
        return False
    
    if not python_exe.exists():
        print(f"[ERRO] Python do ambiente virtual não encontrado: {python_exe}")
        return False
    
    print("[OK] Ambiente verificado com sucesso!")
    return True

def install_dependencies():
    """Instala dependências se necessário"""
    print("\n[INFO] Verificando dependências...")
    
    # Determinar executável Python do venv
    if os.name == 'nt':
        python_exe = Path('.venv') / 'Scripts' / 'python.exe'
    else:
        python_exe = Path('.venv') / 'bin' / 'python'
    
    try:
        # Testar se Flask está instalado
        result = subprocess.run([str(python_exe), '-c', 'import flask'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("[AVISO] Flask não encontrado. Instalando dependências...")
            subprocess.run([str(python_exe), '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("[OK] Dependências instaladas!")
        else:
            print("[OK] Dependências verificadas!")
            
    except Exception as e:
        print(f"[ERRO] Falha ao verificar dependências: {e}")
        return False
    
    return True

def start_server():
    """Inicia o servidor Flask"""
    print("\n[INFO] Iniciando servidor Flask...")
    print("="*80)
    print("  🚀 SERVIDOR INICIANDO...")
    print("  ")
    print("  🌐 URL do Sistema: http://localhost:5000")
    print("  ")
    print("  ⏳ Aguarde alguns segundos...")
    print("  🌍 O navegador abrirá automaticamente")
    print("  ⛔ Para parar o servidor: Pressione Ctrl+C")
    print("="*80)
    
    # Configurar variáveis de ambiente
    env = os.environ.copy()
    env['FLASK_APP'] = 'run.py'
    env['FLASK_ENV'] = 'development'
    env['FLASK_DEBUG'] = '1'
    
    # Determinar executável Python do venv
    if os.name == 'nt':
        python_exe = Path('.venv') / 'Scripts' / 'python.exe'
    else:
        python_exe = Path('.venv') / 'bin' / 'python'
    
    try:
        # Aguardar um pouco e abrir navegador
        def open_browser():
            time.sleep(3)
            print("\n[INFO] Abrindo navegador...")
            webbrowser.open('http://localhost:5000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Iniciar servidor
        subprocess.run([str(python_exe), 'run.py'], env=env)
        
    except KeyboardInterrupt:
        print("\n\n[INFO] Servidor interrompido pelo usuário.")
    except Exception as e:
        print(f"\n[ERRO] Falha ao iniciar servidor: {e}")
        return False
    
    return True

def main():
    """Função principal"""
    try:
        print_banner()
        
        if not check_environment():
            input("\nPressione Enter para sair...")
            return 1
        
        if not install_dependencies():
            input("\nPressione Enter para sair...")
            return 1
        
        if not start_server():
            input("\nPressione Enter para sair...")
            return 1
        
        print("\n[INFO] Sistema encerrado com sucesso.")
        return 0
        
    except Exception as e:
        print(f"\n[ERRO] Erro inesperado: {e}")
        input("\nPressione Enter para sair...")
        return 1

if __name__ == '__main__':
    sys.exit(main())
