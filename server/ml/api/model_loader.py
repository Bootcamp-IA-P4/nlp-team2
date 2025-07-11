import os
import json
import pickle
import hashlib
import io
import warnings
import contextlib
from typing import Optional, Dict, Any, List, Union, Tuple, Iterator, Generator
from server.core.print_dev import log_info, log_error, log_warning, log_debug



class ModelLoader:
    """
    Cargador de modelo que une las partes de un modelo fragmentado 
    directamente en memoria para su uso, sin necesidad de archivos intermedios.
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Inicializa el cargador de modelos.
        
        Args:
            base_dir: Directorio base donde se encuentra el modelo. Si es None,
                     se usará el directorio 'model' relativo a este script.
        """
        if base_dir is None:
            # Directorio relativo al archivo actual
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Subir un nivel para llegar a ml/ y luego entrar a model/
            base_dir = os.path.join(os.path.dirname(current_dir), "model")
        
        self.base_dir = base_dir
        self.model_parts_dir = os.path.join(base_dir, "partes_modelo")
        self.metadata_path = os.path.join(self.model_parts_dir, "metadatos.json")
        
        # Verificar que existan los directorios y archivos necesarios
        if not os.path.exists(self.model_parts_dir):
            log_error(f"No se encontró el directorio de partes del modelo: {self.model_parts_dir}")
            raise FileNotFoundError(f"No se encontró el directorio de partes del modelo: {self.model_parts_dir}")
        
        if not os.path.exists(self.metadata_path):
            log_error(f"No se encontró el archivo de metadatos: {self.metadata_path}")
            raise FileNotFoundError(f"No se encontró el archivo de metadatos: {self.metadata_path}")
    
    def _load_metadata(self) -> Dict[str, Any]:
        """
        Carga los metadatos del modelo fragmentado.
        
        Returns:
            Dict con los metadatos del modelo
        """
        try:
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            log_info(f"Metadatos cargados: {len(metadata.get('partes', []))} partes encontradas")
            return metadata
        except Exception as e:
            log_error(f"Error al cargar los metadatos: {e}")
            raise
    
    def _check_part_files(self, metadata: Dict[str, Any]) -> List[str]:
        """
        Verifica que todas las partes del modelo existan.
        
        Args:
            metadata: Metadatos del modelo
            
        Returns:
            Lista de partes faltantes. Si está vacía, todas las partes existen.
        """
        missing_parts = []
        for part in metadata.get("partes", []):
            # Usar la ruta al archivo dentro de model_parts_dir
            part_filename = os.path.basename(part["archivo"])
            part_path = os.path.join(self.model_parts_dir, part_filename)
            if not os.path.exists(part_path):
                missing_parts.append(part_path)
        
        if missing_parts:
            log_error(f"Faltan {len(missing_parts)} partes del modelo: {missing_parts[:3]}...")
        
        return missing_parts
    
    def _merge_parts_in_memory(self, metadata: Dict[str, Any]) -> bytes:
        """
        Une las partes del modelo en memoria de manera eficiente.
        
        Args:
            metadata: Metadatos del modelo
            
        Returns:
            Bytes del modelo unido
        """
        try:
            # Crear un buffer en memoria para unir las partes
            buffer = io.BytesIO()
            total_parts = len(metadata.get("partes", []))
            bytes_leidos = 0
            
            # Ordenar las partes por número para asegurar el orden correcto
            partes_ordenadas = sorted(metadata.get("partes", []), key=lambda x: x["numero"])
            
            # Unir las partes en el buffer
            for i, part in enumerate(partes_ordenadas, 1):
                # Usar la ruta al archivo dentro de model_parts_dir
                part_filename = os.path.basename(part["archivo"])
                part_path = os.path.join(self.model_parts_dir, part_filename)
                
                if not os.path.exists(part_path):
                    log_error(f"No se encuentra la parte {i}/{total_parts}: {part_filename}")
                    raise FileNotFoundError(f"Archivo de parte no encontrado: {part_path}")
                
                # Mostrar progreso
                log_info(f"Procesando parte {i}/{total_parts}: {part_filename}")
                
                with open(part_path, 'rb') as part_file:
                    # Leer y escribir en chunks para manejar archivos grandes eficientemente
                    chunk_size = 4 * 1024 * 1024  # 4MB chunks
                    while True:
                        chunk = part_file.read(chunk_size)
                        if not chunk:
                            break
                        buffer.write(chunk)
                        bytes_leidos += len(chunk)
            
            # Obtener los bytes del buffer
            buffer.seek(0)
            model_bytes = buffer.getvalue()
            
            # Verificar el tamaño esperado si está disponible
            if "tamaño_original" in metadata:
                tamano_esperado = metadata["tamaño_original"]
                if len(model_bytes) != tamano_esperado:
                    log_warning(f"Tamaño del modelo incorrecto: esperado={tamano_esperado}, actual={len(model_bytes)}")
                else:
                    log_info(f"Verificación de tamaño exitosa: {tamano_esperado} bytes")
            
            # Verificar el hash si está disponible
            if "hash_original" in metadata:
                calculated_hash = hashlib.sha256(model_bytes).hexdigest()
                expected_hash = metadata["hash_original"]
                if calculated_hash != expected_hash:
                    log_warning(f"Hash incorrecto: esperado={expected_hash}, calculado={calculated_hash}")
                else:
                    log_info(f"Verificación de hash exitosa")
            
            log_info(f"Modelo unido correctamente en memoria: {len(model_bytes)/1024/1024:.2f} MB")
            return model_bytes
            
        except Exception as e:
            log_error(f"Error al unir las partes del modelo: {str(e)}")
            raise
    
    def _debug_paths(self) -> None:
        """
        Imprime información de depuración sobre las rutas y los archivos existentes.
        Útil para diagnosticar problemas de rutas.
        """
        log_info(f"Directorio base: {self.base_dir}")
        log_info(f"Directorio de partes: {self.model_parts_dir}")
        log_info(f"Archivo de metadatos: {self.metadata_path}")
        
        # Verificar si existen
        log_info(f"¿Existe directorio base? {os.path.exists(self.base_dir)}")
        log_info(f"¿Existe directorio de partes? {os.path.exists(self.model_parts_dir)}")
        log_info(f"¿Existe archivo de metadatos? {os.path.exists(self.metadata_path)}")
        
        # Listar contenido del directorio de partes
        if os.path.exists(self.model_parts_dir):
            files = sorted(os.listdir(self.model_parts_dir))
            log_info(f"Archivos en directorio de partes ({len(files)}): {files}")
        
        # Cargar metadatos si es posible
        if os.path.exists(self.metadata_path):
            try:
                metadata = self._load_metadata()
                num_partes = metadata.get('num_partes', 'N/A')
                log_info(f"Número de partes según metadatos: {num_partes}")
                
                # Verificar rutas de partes
                missing_parts = []
                for part in metadata.get("partes", []):
                    part_path = os.path.join(self.model_parts_dir, os.path.basename(part["archivo"]))
                    exists = os.path.exists(part_path)
                    if not exists:
                        missing_parts.append(part_path)
                
                if missing_parts:
                    log_error(f"Faltan {len(missing_parts)} partes: {missing_parts}")
                else:
                    log_info("Todas las partes existen")
            except Exception as e:
                log_error(f"Error cargando metadatos para depuración: {e}")
    
    def load_model(self, debug: bool = False) -> Any:
        """
        Carga el modelo directamente en memoria, uniendo las partes.
        
        Args:
            debug: Si es True, imprime información de depuración
            
        Returns:
            Modelo cargado en memoria
        """
        # Modo de depuración para diagnosticar problemas de rutas
        if debug:
            self._debug_paths()
        
        try:
            # Cargar metadatos
            log_info("Iniciando carga de modelo en memoria...")
            metadata = self._load_metadata()
            
            # Verificar que todas las partes existan
            missing_parts = self._check_part_files(metadata)
            if missing_parts:
                raise FileNotFoundError(f"Faltan {len(missing_parts)} partes del modelo: {missing_parts[:3]}")
            
            # Unir las partes en memoria
            model_bytes = self._merge_parts_in_memory(metadata)
            
            # Cargar el modelo desde los bytes
            log_info("Deserializando modelo desde bytes en memoria...")
            try:
                model = pickle.loads(model_bytes)
                log_info(f"Modelo cargado exitosamente: {type(model)}")
                
                # Liberar memoria del buffer de bytes
                del model_bytes
                
                return model
            except Exception as e:
                log_error(f"Error deserializando el modelo: {str(e)}")
                raise RuntimeError(f"No se pudo deserializar el modelo: {str(e)}")
                
        except Exception as e:
            log_error(f"Error en la carga del modelo: {str(e)}")
            raise

@contextlib.contextmanager
def suppress_torch_numpy_warnings() -> Iterator[None]:
    """
    Contexto que suprime las advertencias relacionadas con torch y numpy.
    Útil para evitar mensajes como 'Failed to initialize NumPy: _ARRAY_API not found'.
    
    Ejemplo de uso:
        with suppress_torch_numpy_warnings():
            model = get_model()
    """
    # Filtrar advertencias específicas
    warnings_to_ignore = [
        "Failed to initialize NumPy: _ARRAY_API not found",
        "device: torch.device = torch.device",
        "torch._C._get_default_device()",
        "_ARRAY_API",
        "tensor_numpy.cpp"
    ]
    
    # Guardar filtros anteriores y aplicar nuevos
    with warnings.catch_warnings():
        # Primero, ignorar todas las UserWarning de torch
        warnings.filterwarnings("ignore", category=UserWarning, module="torch")
        
        # Luego, patrones específicos que podrían venir en otras categorías
        for warning_text in warnings_to_ignore:
            warnings.filterwarnings("ignore", message=f".*{warning_text}.*")
        
        try:
            yield
        except Exception as e:
            log_error(f"Error durante la ejecución con warnings suprimidos: {str(e)}")
            raise


def get_model(debug: bool = False) -> Any:
    """
    Función de utilidad para obtener el modelo unificado directamente en memoria.
    
    Args:
        debug: Si es True, imprime información de depuración
        
    Returns:
        Modelo cargado en memoria, listo para usar
    """
    loader = ModelLoader()
    return loader.load_model(debug)



def get_model_efficiently(debug: bool = False, max_retries: int = 1) -> Any:
    """
    Función optimizada para obtener el modelo unificado directamente en memoria,
    suprimiendo advertencias comunes de PyTorch y NumPy que pueden aparecer durante
    la carga y deserialización.
    
    Args:
        debug: Si es True, imprime información de depuración y no suprime advertencias
        max_retries: Número máximo de intentos si ocurre un error (por defecto: 1)
        
    Returns:
        Modelo cargado en memoria, listo para usar
        
    Raises:
        RuntimeError: Si no se puede cargar el modelo después de los reintentos
    """
    if debug:
        # En modo debug mostramos todas las advertencias
        log_info("Cargando modelo en modo debug (mostrando advertencias)")
        return get_model(debug=True)
    
    # Suprimir advertencias durante la carga
    log_info("Cargando modelo de forma eficiente (suprimiendo advertencias)")
    attempt = 0
    last_error = None
    
    while attempt < max_retries:
        attempt += 1
        try:
            with suppress_torch_numpy_warnings():
                loader = ModelLoader()
                return loader.load_model(debug=False)
        except Exception as e:
            last_error = e
            log_warning(f"Intento {attempt}/{max_retries} falló: {str(e)}")
    
    # Si llegamos aquí, todos los intentos fallaron
    log_error(f"No se pudo cargar el modelo después de {max_retries} intentos")
    raise RuntimeError(f"Error cargando modelo: {str(last_error)}")


def get_unified_model(in_memory: bool = True, debug: bool = False) -> Any:
    """
    Función de compatibilidad para código existente.
    Redirecciona a get_model o get_model_efficiently según los parámetros.
    
    Args:
        in_memory: Si es True, carga el modelo en memoria (siempre True en esta versión)
        debug: Si es True, imprime información de depuración
        
    Returns:
        Modelo cargado en memoria
    """
    log_warning("get_unified_model está obsoleto, use get_model o get_model_efficiently en su lugar")
    return get_model_efficiently(debug=debug)


