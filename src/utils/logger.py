"""
Módulo de logging centralizado usando Loguru

Este módulo configura o logger para toda a aplicação,
incluindo formatação, rotação de arquivos e níveis de log.
"""
import sys
from pathlib import Path
from loguru import logger
from config.monitoring_config import LOG_CONFIG, LOG_FILES, LOGS_DIR

# Remover handler padrão do loguru
logger.remove()

# Adicionar handler para console (sempre ativo)
logger.add(
    sys.stdout,
    format=LOG_CONFIG["format"],
    level=LOG_CONFIG["level"],
    colorize=True,
    backtrace=True,
    diagnose=True,
)


def setup_logger(component: str, serialize: bool = False):
    """
    Configura o logger para um componente específico
    
    Args:
        component: Nome do componente (api, training, prediction, retraining)
        serialize: Se True, grava logs em formato JSON
    
    Returns:
        logger configurado
    """
    if component not in LOG_FILES:
        raise ValueError(f"Componente inválido: {component}. Use: {list(LOG_FILES.keys())}")
    
    # Garantir que o diretório de logs existe
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Configurar arquivo de log para o componente
    log_file = LOG_FILES[component]
    
    logger.add(
        log_file,
        format=LOG_CONFIG["format"],
        level=LOG_CONFIG["level"],
        rotation=LOG_CONFIG["rotation"],
        retention=LOG_CONFIG["retention"],
        compression=LOG_CONFIG["compression"],
        serialize=serialize,  # True para JSON, False para texto
        backtrace=True,
        diagnose=True,
        enqueue=True,  # Thread-safe
    )
    
    logger.info(f"Logger configurado para componente: {component}")
    logger.debug(f"Arquivo de log: {log_file}")
    
    return logger


def get_logger():
    """
    Retorna o logger global
    
    Returns:
        logger instance
    """
    return logger


# Exemplo de uso com contexto adicional
def log_with_context(level: str, message: str, **context):
    """
    Loga mensagem com contexto adicional
    
    Args:
        level: Nível do log (info, debug, warning, error, critical, success)
        message: Mensagem do log
        **context: Contexto adicional (kwargs)
    
    Example:
        log_with_context("info", "Predição realizada", 
                        id_cliente=123, risco=0.75, nivel="alto")
    """
    log_func = getattr(logger, level.lower())
    
    if context:
        # Adicionar contexto extra ao log
        logger_with_context = logger.bind(**context)
        getattr(logger_with_context, level.lower())(message)
    else:
        log_func(message)


# Decorador para logar entrada/saída de funções
def log_function(level: str = "debug"):
    """
    Decorador para logar entrada e saída de funções
    
    Args:
        level: Nível do log (default: debug)
    
    Example:
        @log_function(level="info")
        def minha_funcao(x, y):
            return x + y
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger_func = getattr(logger, level)
            logger_func(f"Entrando em {func.__name__} com args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger_func(f"Saindo de {func.__name__} com resultado={result}")
                return result
            except Exception as e:
                logger.exception(f"Erro em {func.__name__}: {e}")
                raise
        return wrapper
    return decorator


# Exportar logger configurado
__all__ = ["logger", "setup_logger", "get_logger", "log_with_context", "log_function"]
