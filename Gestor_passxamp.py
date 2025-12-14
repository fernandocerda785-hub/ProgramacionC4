import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import hashlib  # Para seguridad adicional

class GestorContraseñasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contraseñas Seguras")
        self.root.geometry("700x600")
        
        # Configuración de la base de datos
        self.db_config = {
            'host': 'localhost',
            'user': 'root',  # Usuario por defecto de XAMPP
            'password': '',  # Contraseña por defecto (vacía en XAMPP)
            'database': 'gestor_contrasenas'
        }
        
        # Crear base de datos y tabla si no existen
        self.inicializar_base_datos()
        
        # Variables
        self.usuarios = []
        self.contrasenas = []
        
        # Configurar interfaz
        self.configurar_interfaz()
        
    def inicializar_base_datos(self):
        """Crea la base de datos y tabla si no existen"""
        try:
            # Primero conectar sin especificar base de datos
            conn = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            cursor = conn.cursor()
            
            # Crear base de datos si no existe
            cursor.execute("CREATE DATABASE IF NOT EXISTS gestor_contrasenas")
            cursor.execute("USE gestor_contrasenas")
            
            # Crear tabla de usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario VARCHAR(100) NOT NULL UNIQUE,
                    contrasena VARCHAR(255) NOT NULL,
                    es_segura BOOLEAN DEFAULT FALSE,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ultima_verificacion TIMESTAMP
                )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo conectar a MySQL: {e}")
    
    def conectar_db(self):
        """Establece conexión con la base de datos"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar: {e}")
            return None
    
    def configurar_interfaz(self):
        """Configura los elementos de la interfaz gráfica"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(main_frame, text="🔐 Gestor de Contraseñas Seguras", 
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Frame para registro
        frame_registro = ttk.LabelFrame(main_frame, text="Registro de Usuario", padding="15")
        frame_registro.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Entrada de usuario
        ttk.Label(frame_registro, text="Nombre de usuario:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_usuario = ttk.Entry(frame_registro, width=40)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=5)
        
        # Entrada de contraseña
        ttk.Label(frame_registro, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_contrasena = ttk.Entry(frame_registro, width=40, show="•")
        self.entry_contrasena.grid(row=1, column=1, padx=10, pady=5)
        
        # Botón para mostrar/ocultar contraseña
        self.mostrar_contrasena_var = tk.BooleanVar()
        self.check_mostrar = ttk.Checkbutton(frame_registro, text="Mostrar contraseña", 
                                            variable=self.mostrar_contrasena_var,
                                            command=self.toggle_mostrar_contrasena)
        self.check_mostrar.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Botones de acción
        frame_botones = ttk.Frame(frame_registro)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(frame_botones, text="Registrar Usuario", 
                  command=self.registrar_usuario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Verificar Todos", 
                  command=self.verificar_todos).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Generar Contraseña", 
                  command=self.generar_contrasena).pack(side=tk.LEFT, padx=5)
        
        # Frame para resultados
        frame_resultados = ttk.LabelFrame(main_frame, text="Resultados", padding="15")
        frame_resultados.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Texto para resultados
        self.texto_resultados = tk.Text(frame_resultados, height=15, width=70)
        self.texto_resultados.grid(row=0, column=0)
        
        # Scrollbar para resultados
        scrollbar = ttk.Scrollbar(frame_resultados, command=self.texto_resultados.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.texto_resultados.config(yscrollcommand=scrollbar.set)
        
        # Frame para base de datos
        frame_db = ttk.LabelFrame(main_frame, text="Base de Datos", padding="15")
        frame_db.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(frame_db, text="Ver Usuarios Registrados", 
                  command=self.mostrar_usuarios_db).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_db, text="Limpiar Base de Datos", 
                  command=self.limpiar_base_datos).pack(side=tk.LEFT, padx=5)
        
        # Información de criterios
        info_text = """
Criterios para contraseña segura:
• Mínimo 8 caracteres
• Al menos una letra mayúscula
• Al menos una letra minúscula
• Al menos un número
• Al menos un símbolo especial (!@#$%^&*(),.?":{}|<>)
        """
        ttk.Label(main_frame, text=info_text, foreground="gray").grid(row=4, column=0, columnspan=2, pady=10)
    
    def toggle_mostrar_contrasena(self):
        """Muestra u oculta la contraseña en el campo de entrada"""
        if self.mostrar_contrasena_var.get():
            self.entry_contrasena.config(show="")
        else:
            self.entry_contrasena.config(show="•")
    
    def verificar_contrasena(self, contra):
        """Verifica la fortaleza de la contraseña"""
        largo = len(contra)
        mayus = 0
        minus = 0
        num = 0
        simb = 0
        
        # Contar las características de la contraseña
        for c in contra:
            if c.isupper():
                mayus += 1
            elif c.islower():
                minus += 1
            elif c.isdigit():
                num += 1
            elif not c.isalnum():
                simb += 1
        
        # Verificar si cumple con los criterios de seguridad
        if largo >= 8 and mayus > 0 and minus > 0 and num > 0 and simb > 0:
            return True, {
                'largo': largo,
                'mayus': mayus,
                'minus': minus,
                'num': num,
                'simb': simb
            }
        else:
            return False, {
                'largo': largo,
                'mayus': mayus,
                'minus': minus,
                'num': num,
                'simb': simb
            }
    
    def generar_alerta(self, usuario, detalles):
        """Genera una alerta para contraseña débil"""
        mensaje = f"⚠️ ALERTA: La contraseña del usuario '{usuario}' es débil.\n"
        mensaje += f"Longitud: {detalles['largo']} caracteres (mínimo 8)\n"
        mensaje += f"Mayúsculas: {detalles['mayus']} (mínimo 1)\n"
        mensaje += f"Minúsculas: {detalles['minus']} (mínimo 1)\n"
        mensaje += f"Números: {detalles['num']} (mínimo 1)\n"
        mensaje += f"Símbolos: {detalles['simb']} (mínimo 1)\n"
        mensaje += "Debe contener al menos 8 caracteres, mayúsculas, minúsculas, números y símbolos."
        
        return mensaje
    
    def registrar_usuario(self):
        """Registra un usuario en la base de datos"""
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        
        if not usuario or not contrasena:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos")
            return
        
        # Verificar fortaleza de la contraseña
        es_segura, detalles = self.verificar_contrasena(contrasena)
        
        # Guardar en base de datos
        conn = self.conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Encriptar contraseña (hash)
                contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()
                
                # Insertar usuario
                cursor.execute("""
                    INSERT INTO usuarios (usuario, contrasena, es_segura)
                    VALUES (%s, %s, %s)
                """, (usuario, contrasena_hash, es_segura))
                
                conn.commit()
                
                # Mostrar resultado
                self.texto_resultados.delete(1.0, tk.END)
                if es_segura:
                    self.texto_resultados.insert(tk.END, f"✅ Usuario '{usuario}' registrado exitosamente\n")
                    self.texto_resultados.insert(tk.END, "La contraseña es SEGURA\n")
                    messagebox.showinfo("Registro Exitoso", f"Usuario '{usuario}' registrado con contraseña segura")
                else:
                    self.texto_resultados.insert(tk.END, f"⚠️ Usuario '{usuario}' registrado con contraseña débil\n")
                    self.texto_resultados.insert(tk.END, self.generar_alerta(usuario, detalles))
                    messagebox.showwarning("Contraseña Débil", 
                                         f"La contraseña de '{usuario}' es débil. Considere cambiarla.")
                
                # Limpiar campos
                self.entry_usuario.delete(0, tk.END)
                self.entry_contrasena.delete(0, tk.END)
                
                cursor.close()
                
            except Error as e:
                if "Duplicate entry" in str(e):
                    messagebox.showerror("Error", f"El usuario '{usuario}' ya existe")
                else:
                    messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")
            finally:
                conn.close()
    
    def verificar_todos(self):
        """Verifica todas las contraseñas en la base de datos"""
        conn = self.conectar_db()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT usuario, contrasena, es_segura FROM usuarios")
                usuarios = cursor.fetchall()
                
                self.texto_resultados.delete(1.0, tk.END)
                self.texto_resultados.insert(tk.END, "=== VERIFICANDO CONTRASEÑAS ===\n\n")
                
                for usuario in usuarios:
                    # Aquí podríamos verificar la contraseña original, pero como está hasheada,
                    # solo podemos mostrar el estado guardado
                    if usuario['es_segura']:
                        self.texto_resultados.insert(tk.END, 
                            f"✅ La contraseña del usuario {usuario['usuario']} es SEGURA\n")
                    else:
                        self.texto_resultados.insert(tk.END, 
                            f"⚠️ La contraseña del usuario {usuario['usuario']} es DÉBIL\n")
                
                self.texto_resultados.insert(tk.END, "\nVerificación completada.")
                
                cursor.close()
                
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron verificar las contraseñas: {e}")
            finally:
                conn.close()
    
    def generar_contrasena(self):
        """Genera una contraseña segura automáticamente"""
        import random
        import string
        
        # Definir conjuntos de caracteres
        mayusculas = string.ascii_uppercase
        minusculas = string.ascii_lowercase
        numeros = string.digits
        simbolos = "!@#$%^&*(),.?\":{}|<>"
        
        # Asegurar al menos un carácter de cada tipo
        contrasena = [
            random.choice(mayusculas),
            random.choice(minusculas),
            random.choice(numeros),
            random.choice(simbolos)
        ]
        
        # Completar hasta 12 caracteres
        todos_caracteres = mayusculas + minusculas + numeros + simbolos
        contrasena.extend(random.choice(todos_caracteres) for _ in range(8))
        
        # Mezclar la contraseña
        random.shuffle(contrasena)
        contrasena_generada = ''.join(contrasena)
        
        # Mostrar en el campo de contraseña
        self.entry_contrasena.delete(0, tk.END)
        self.entry_contrasena.insert(0, contrasena_generada)
        
        # Mostrar en resultados
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, f"🔑 Contraseña generada: {contrasena_generada}\n")
        self.texto_resultados.insert(tk.END, "Esta contraseña cumple con todos los criterios de seguridad.\n")
        self.texto_resultados.insert(tk.END, "Cópiala y pégala en el campo de contraseña.")
    
    def mostrar_usuarios_db(self):
        """Muestra todos los usuarios registrados en la base de datos"""
        conn = self.conectar_db()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT usuario, es_segura, fecha_registro 
                    FROM usuarios 
                    ORDER BY fecha_registro DESC
                """)
                usuarios = cursor.fetchall()
                
                self.texto_resultados.delete(1.0, tk.END)
                self.texto_resultados.insert(tk.END, "=== USUARIOS REGISTRADOS ===\n\n")
                
                if not usuarios:
                    self.texto_resultados.insert(tk.END, "No hay usuarios registrados.")
                else:
                    for usuario in usuarios:
                        estado = "✅ SEGURA" if usuario['es_segura'] else "⚠️ DÉBIL"
                        fecha = usuario['fecha_registro'].strftime("%Y-%m-%d %H:%M:%S")
                        self.texto_resultados.insert(tk.END, 
                            f"Usuario: {usuario['usuario']}\n")
                        self.texto_resultados.insert(tk.END, 
                            f"Estado: {estado}\n")
                        self.texto_resultados.insert(tk.END, 
                            f"Fecha de registro: {fecha}\n")
                        self.texto_resultados.insert(tk.END, "-" * 40 + "\n")
                
                cursor.close()
                
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron obtener los usuarios: {e}")
            finally:
                conn.close()
    
    def limpiar_base_datos(self):
        """Elimina todos los usuarios de la base de datos"""
        respuesta = messagebox.askyesno(
            "Confirmar", 
            "¿Está seguro de que desea eliminar TODOS los usuarios?\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            conn = self.conectar_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM usuarios")
                    conn.commit()
                    
                    self.texto_resultados.delete(1.0, tk.END)
                    self.texto_resultados.insert(tk.END, "✅ Base de datos limpiada exitosamente.")
                    
                    messagebox.showinfo("Base de Datos", "Todos los usuarios han sido eliminados.")
                    
                    cursor.close()
                    
                except Error as e:
                    messagebox.showerror("Error", f"No se pudo limpiar la base de datos: {e}")
                finally:
                    conn.close()

# Configuración para XAMPP
def configurar_xampp():
    """Muestra instrucciones para configurar XAMPP"""
    instrucciones = """
INSTRUCCIONES PARA XAMPP:

1. Abre el Panel de Control de XAMPP
2. Inicia los servicios:
   - Apache (para servicios web)
   - MySQL (para base de datos)

3. Configuración de MySQL:
   - Usuario: root
   - Contraseña: (vacía por defecto)
   - Host: localhost
   - Puerto: 3306

4. La aplicación creará automáticamente:
   - Base de datos: gestor_contrasenas
   - Tabla: usuarios

5. Para ver los datos en phpMyAdmin:
   - Abre tu navegador
   - Ve a: http://localhost/phpmyadmin
   - Selecciona la base de datos 'gestor_contrasenas'
    """
    
    print(instrucciones)
    messagebox.showinfo("Configuración XAMPP", instrucciones)

# Función principal
def main():
    root = tk.Tk()
    app = GestorContraseñasApp(root)
    
    # Mostrar instrucciones al inicio
    configurar_xampp()
    
    root.mainloop()

if __name__ == "__main__":
    main()