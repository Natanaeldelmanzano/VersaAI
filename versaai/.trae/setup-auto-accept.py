#!/usr/bin/env python3
# 🚀 VersaAI - Configurador Auto Accept All
# Script para configurar automáticamente el modo Auto Accept All optimizado
# Autor: VersaAI Development Team
# Fecha: 2024-12-07
# Versión: 1.0.0

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class VersaAIAutoAcceptConfigurator:
    """Configurador automático para Auto Accept All en VersaAI."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.trae_config_path = self.project_root / ".trae" / "config.json"
        self.auto_accept_config_path = self.project_root / ".trae" / "auto-accept-config.json"
        self.backup_dir = self.project_root / ".trae" / "backups"
        
    def create_backup(self) -> str:
        """Crea un backup de la configuración actual."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"config_backup_{timestamp}.json"
        
        # Crear directorio de backups si no existe
        self.backup_dir.mkdir(exist_ok=True)
        
        # Copiar configuración actual
        if self.trae_config_path.exists():
            shutil.copy2(self.trae_config_path, backup_path)
            print(f"✅ Backup creado: {backup_path}")
            return str(backup_path)
        else:
            print("⚠️  No se encontró configuración existente para respaldar")
            return ""
    
    def load_current_config(self) -> Dict[str, Any]:
        """Carga la configuración actual de Trae."""
        if not self.trae_config_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de configuración: {self.trae_config_path}")
        
        with open(self.trae_config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_auto_accept_config(self) -> Dict[str, Any]:
        """Carga la configuración de Auto Accept All."""
        if not self.auto_accept_config_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de configuración Auto Accept: {self.auto_accept_config_path}")
        
        with open(self.auto_accept_config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def merge_configurations(self, base_config: Dict[str, Any], auto_accept_config: Dict[str, Any]) -> Dict[str, Any]:
        """Fusiona las configuraciones base y Auto Accept."""
        merged_config = base_config.copy()
        
        # Aplicar configuraciones de Auto Accept All
        auto_accept_settings = auto_accept_config["auto_accept_configuration"]
        
        # Configuraciones globales de AI assistance
        if "ai_assistance" in merged_config:
            merged_config["ai_assistance"].update({
                "auto_accept_all": True,
                "auto_implementation": True,
                "intelligent_file_creation": True,
                "project_state_awareness": True,
                "context_aware_decisions": True,
                "safety_checks_enabled": True
            })
        
        # Configuraciones de productividad
        if "productivity" in merged_config:
            if "smart_code_generation" in merged_config["productivity"]:
                merged_config["productivity"]["smart_code_generation"].update({
                    "service_layer_generation": True,
                    "api_endpoint_scaffolding": True,
                    "vue_component_scaffolding": True,
                    "database_model_generation": True,
                    "test_case_generation": True
                })
            
            if "workflow_automation" in merged_config["productivity"]:
                merged_config["productivity"]["workflow_automation"].update({
                    "auto_file_organization": True,
                    "intelligent_refactoring": True,
                    "service_integration_automation": True,
                    "migration_generation": True,
                    "error_resolution_suggestions": True
                })
        
        # Configuraciones específicas de VersaAI
        if "versaai_specific" in merged_config:
            merged_config["versaai_specific"].update({
                "auto_accept_mode": True,
                "intelligent_service_generation": True,
                "context_aware_implementation": True,
                "conversation_history_integration": True
            })
        
        return merged_config
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Guarda la configuración fusionada."""
        with open(self.trae_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Configuración guardada: {self.trae_config_path}")
    
    def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """Valida que la configuración sea correcta."""
        required_sections = [
            "project",
            "ai_assistance",
            "productivity",
            "backend",
            "frontend"
        ]
        
        for section in required_sections:
            if section not in config:
                print(f"❌ Sección requerida faltante: {section}")
                return False
        
        # Validar configuraciones específicas de Auto Accept
        ai_assistance = config.get("ai_assistance", {})
        if not ai_assistance.get("auto_accept_all", False):
            print("❌ Auto Accept All no está habilitado")
            return False
        
        print("✅ Configuración validada correctamente")
        return True
    
    def setup_auto_accept(self) -> bool:
        """Configura Auto Accept All para VersaAI."""
        try:
            print("🚀 Iniciando configuración de Auto Accept All para VersaAI...")
            
            # Crear backup
            backup_path = self.create_backup()
            
            # Cargar configuraciones
            print("📖 Cargando configuración actual...")
            current_config = self.load_current_config()
            
            print("📖 Cargando configuración Auto Accept...")
            auto_accept_config = self.load_auto_accept_config()
            
            # Fusionar configuraciones
            print("🔄 Fusionando configuraciones...")
            merged_config = self.merge_configurations(current_config, auto_accept_config)
            
            # Validar configuración
            print("✅ Validando configuración...")
            if not self.validate_configuration(merged_config):
                print("❌ Error en la validación de configuración")
                return False
            
            # Guardar configuración
            print("💾 Guardando configuración optimizada...")
            self.save_config(merged_config)
            
            # Mostrar resumen
            self.show_configuration_summary(merged_config)
            
            print("\n🎉 ¡Auto Accept All configurado exitosamente!")
            print(f"📁 Backup disponible en: {backup_path}")
            print("\n🔧 Comandos útiles:")
            print("   - Deshabilitar: trae config set ai_assistance.auto_accept_all false")
            print("   - Restaurar backup: cp <backup_path> .trae/config.json")
            print("   - Ver estado: trae config show")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante la configuración: {e}")
            return False
    
    def show_configuration_summary(self, config: Dict[str, Any]) -> None:
        """Muestra un resumen de la configuración aplicada."""
        print("\n📋 Resumen de configuración aplicada:")
        print("="*50)
        
        ai_assistance = config.get("ai_assistance", {})
        print(f"🤖 Auto Accept All: {ai_assistance.get('auto_accept_all', False)}")
        print(f"🧠 Auto Implementation: {ai_assistance.get('auto_implementation', False)}")
        print(f"📁 Intelligent File Creation: {ai_assistance.get('intelligent_file_creation', False)}")
        print(f"🎯 Project State Awareness: {ai_assistance.get('project_state_awareness', False)}")
        
        productivity = config.get("productivity", {})
        smart_gen = productivity.get("smart_code_generation", {})
        workflow = productivity.get("workflow_automation", {})
        
        print(f"\n🏗️  Generación de código inteligente:")
        print(f"   - Service Layer: {smart_gen.get('service_layer_generation', False)}")
        print(f"   - API Endpoints: {smart_gen.get('api_endpoint_scaffolding', False)}")
        print(f"   - Vue Components: {smart_gen.get('vue_component_scaffolding', False)}")
        
        print(f"\n⚡ Automatización de flujo de trabajo:")
        print(f"   - Auto File Organization: {workflow.get('auto_file_organization', False)}")
        print(f"   - Intelligent Refactoring: {workflow.get('intelligent_refactoring', False)}")
        print(f"   - Service Integration: {workflow.get('service_integration_automation', False)}")
        
        print("="*50)
    
    def rollback_configuration(self, backup_path: str) -> bool:
        """Restaura una configuración desde un backup."""
        try:
            if not os.path.exists(backup_path):
                print(f"❌ Backup no encontrado: {backup_path}")
                return False
            
            shutil.copy2(backup_path, self.trae_config_path)
            print(f"✅ Configuración restaurada desde: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error al restaurar configuración: {e}")
            return False

def main():
    """Función principal del configurador."""
    configurator = VersaAIAutoAcceptConfigurator()
    
    print("🚀 VersaAI Auto Accept All Configurator")
    print("="*50)
    print("Este script configurará Auto Accept All optimizado para VersaAI")
    print("Se creará un backup automático de la configuración actual")
    print("="*50)
    
    # Confirmar ejecución
    response = input("\n¿Continuar con la configuración? (y/N): ").strip().lower()
    if response not in ['y', 'yes', 'sí', 's']:
        print("❌ Configuración cancelada")
        return
    
    # Ejecutar configuración
    success = configurator.setup_auto_accept()
    
    if success:
        print("\n🎉 ¡Configuración completada exitosamente!")
        print("🚀 VersaAI está ahora optimizado para Auto Accept All")
    else:
        print("\n❌ Error en la configuración")
        print("🔧 Revisa los logs y intenta nuevamente")

if __name__ == "__main__":
    main()