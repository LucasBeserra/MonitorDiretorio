import win32serviceutil
import win32service
import win32event
import servicemanager
import logging
import time
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Template mensagens registradas nos logs
class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f"Arquivo criado: {event.src_path}")

    def on_deleted(self, event):
        logging.info(f"Arquivo deletado: {event.src_path}")

    def on_modified(self, event):
        logging.info(f"Arquivo modificado: {event.src_path}")

    def on_moved(self, event):
        logging.info(f"Arquivo movido de {event.src_path} para {event.dest_path}")


# Classe do Serviço
class MonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MonitorDiretorio"
    _svc_display_name_ = "Monitor de Diretório Python"
    _svc_description_ = "Serviço que monitora alterações em uma pasta definida."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, "")
        )

        # Lendo config.json
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError("Arquivo config.json não encontrado!")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                f.write("Nova mensagem de log adicionada via código.\n")

                print("Nova mensagem de log adicionada via código.")
        except Exception as e:
            print(f"Erro ao adicionar mensagem de log: {e}")

        monitor_path = config.get("monitor_path", "C:\\Users\\lbese\\OneDrive\\Documentos\\test")
        log_file = config.get("log_file", "C:\\Users\\lbese\\OneDrive\\Documentos\\test\\logs.log")

        # Configuração do log
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Observador
        event_handler = MonitorHandler()
        observer = Observer()
        observer.schedule(event_handler, monitor_path, recursive=True)
        observer.start()

        try:
            while self.running:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(MonitorService)
