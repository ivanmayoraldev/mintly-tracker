# 💰 Mintly Finance Tracker

**Aplicación de gestión de finanzas personales desarrollada con Python y PySide6**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.5+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Descripción

Mintly es una aplicación de escritorio para el control de finanzas personales que permite:

- ✅ Registrar ingresos y gastos con categorización
- ✅ Crear y gestionar metas de ahorro
- ✅ Configurar ahorro automático desde ingresos
- ✅ Visualizar estadísticas financieras con gráficos interactivos
- ✅ Calcular salud financiera y ratios clave
- ✅ Exportar datos a CSV y PDF

---

## 🏗️ Arquitectura MVC

El proyecto sigue el patrón **Modelo-Vista-Controlador** para una separación clara de responsabilidades:

```
mintly/
├── src/
│   ├── models/              # MODELO - Lógica de datos
│   │   ├── database.py      # Gestión de SQLite
│   │   ├── transaction.py   # Entidad Transacción
│   │   └── savings_goal.py  # Entidad Meta de Ahorro
│   │
│   ├── views/               # VISTA - Interfaz de usuario
│   │   ├── main_window.py   # Ventana principal
│   │   ├── dashboard.py     # Panel principal con columnas
│   │   ├── stats_tab.py     # Pestaña de estadísticas
│   │   └── dialogs.py       # Diálogos de entrada
│   │
│   ├── controllers/         # CONTROLADOR - Lógica de negocio
│   │   └── mintly.py        # Coordinador principal
│   │
│   ├── widgets/             # Componentes personalizados
│   │   ├── chart_widget.py  # Gráficos con Matplotlib
│   │   └── balance_card.py  # Tarjetas de balance
│   │
│   ├── utils/               # Utilidades
│   │   ├── export_manager.py   # Exportación CSV/PDF
│   │
│   └── main.py              # Punto de entrada
│
├── tests/
│   └── test_mintly_controller.py       # Tests unitarios
│
├── docs/
│   └── README.md            # Este archivo
│
└── requirements.txt         # Dependencias
```

### Flujo de Datos MVC

```
┌──────────┐      ┌────────────┐      ┌──────────┐
│  VISTA   │ ───> │ CONTROLADOR│ ───> │  MODELO  │
│ (PySide6)│ <─── │  (Lógica)  │ <─── │(Database)│
└──────────┘      └────────────┘      └──────────┘
    │                    │                   │
 Dashboard         MintlyController      Database
  Dialogs                                 Transaction
StatisticsTab                             SavingsGoal
```

**Responsabilidades:**

- **Modelo**: Gestiona datos (SQLite), define entidades (Transaction, SavingsGoal)
- **Vista**: Renderiza UI (QWidgets), captura eventos del usuario
- **Controlador**: Coordina modelo y vista, implementa lógica de negocio

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/mintly.git
cd mintly
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**
```
PySide6>=6.5.0
matplotlib>=3.7.0
reportlab>=4.0.0
```

### Paso 4: Ejecutar la aplicación

```bash
python src/main.py
```

---

## 📦 Dependencias

Librería 
**PySide6** - ≥6.5.0 - Framework de interfaz gráfica (Qt for Python) |
**matplotlib** - ≥3.7.0 - Generación de gráficos financieros |
**reportlab** - ≥4.0.0 - Exportación de reportes a PDF |
**sqlite3** - Base de datos local 

---

## 🎯 Características Principales

### 1. **Gestión de Transacciones**

```python
# Crear ingreso
controller.create_transaction(
    t_type=TransactionType.INCOME,
    amount=2000.0,
    category="💼 Salario",
    description="Salario mensual",
    date="2024-01-15"
)

# Crear gasto
controller.create_transaction(
    t_type=TransactionType.EXPENSE,
    amount=150.0,
    category="🛒 Alimentación",
    description="Compra supermercado",
    date="2024-01-16"
)
```

### 2. **Ahorro Automático**

Configura un porcentaje de ahorro automático al registrar ingresos:

```python
# Ingreso con 20% de ahorro automático
controller.create_transaction(
    t_type=TransactionType.INCOME,
    amount=1000.0,
    category="💼 Salario",
    description="Salario",
    date="2024-01-20",
    goal_id=1,           # ID de la meta
    save_pct=20          # 20% = €200 a la meta
)
```

**Resultado:**
- Balance neto: +€800
- Meta actualizada: +€200

### 3. **Metas de Ahorro**

```python
# Crear meta
goal_id = controller.create_savings_goal(
    name="Vacaciones",
    target_amount=3000.0,
    current_amount=0.0,
    deadline="2024-12-31",
    description="Viaje a Europa"
)

# Añadir ahorro manual
controller.add_to_savings_goal(goal_id, 250.0)
```

### 4. **Salud Financiera**

El sistema calcula un score de 0-100 basado en:
- Tasa de ahorro
- Tasa de gasto
- Proporción ingreso/gasto

```python
health = controller.get_financial_health_score()
# {'score': 85, 'level': 'Excelente', 'message': 'Finanzas óptimas 🎉'}
```

### 5. **Estadísticas Visuales**

- Gráficos circulares, de barras y líneas
- Comparativa de ingresos, gastos y ahorros
- Ratios financieros clave

---

## 🧪 Tests Unitarios

El proyecto incluye tests completos para validar la lógica:

```bash
# Ejecutar todos los tests
python tests/test_mintly.py

# Ejecutar con verbosidad
python tests/test_mintly.py -v
```

**Tests incluidos:**

1. ✅ Creación de transacciones
2. ✅ Cálculo de balance mensual
3. ✅ Progreso de metas de ahorro
4. ✅ Ahorro automático
5. ✅ Operaciones CRUD en base de datos
6. ✅ Salud financiera

**Ejemplo de salida:**
```
test_auto_savings_creation ... ok
test_monthly_balance_calculation ... ok
test_progress_percentage_calculation ... ok

Ran 15 tests in 0.234s
OK
```

---

## 🎨 Componente Personalizado: BalanceCard

Widget personalizado que muestra métricas financieras de forma visual:

```
class BalanceCard(QWidget):
    """
    Tarjeta interactiva que muestra balance con:
    - Título descriptivo
    - Monto formateado con símbolo €
    - Color de acento personalizable
    - Efecto hover
    - Señal clicked() para interacción
    """
    
    clicked = Signal()  # Emite al hacer click
    
    def __init__(self, title, amount, color):
        # Configuración de UI...
        
    def set_amount(self, amount):
        """Actualiza el monto dinámicamente"""
        
    def set_color(self, color):
        """Cambia el color de acento"""
```

**Uso:**
```python
card = BalanceCard("Balance Total", 1500.0, "#3B82F6")
card.clicked.connect(self.on_card_clicked)
card.set_amount(2000.0)  # Actualizar dinámicamente
```

---

## 📊 Exportación de Datos

### CSV

```python
# Exportar todas las transacciones y metas
ExportManager.export_to_csv(
    transactions=controller.get_all_transactions(),
    filename="export.csv",
    goals=controller.get_all_savings_goals()
)
```

**Formato del CSV:**
```csv
FECHA,TIPO,CATEGORIA,MONTO,DESCRIPCION
2024-01-15,Ingreso,💼 Salario,2000.00,Salario mensual
2024-01-16,Gasto,🛒 Alimentación,150.00,Supermercado

--- METAS DE AHORRO ---
NOMBRE,OBJETIVO,AHORRADO,PROGRESO,FECHA LIMITE
Vacaciones,3000.00,500.00,16.7%,2024-12-31
```

### PDF

```python
# Exportar reporte completo
ExportManager.export_to_pdf(
    transactions=controller.get_all_transactions(),
    balance=controller.get_monthly_balance(),
    filename="report.pdf",
    goals=controller.get_all_savings_goals()
)
```

---

## 🔒 Base de Datos

**Motor:** SQLite3  
**Archivo:** `mintly.db`

### Esquema

```sql
-- Tabla de transacciones
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT CHECK(type IN ('ingreso', 'gasto', 'ahorro')),
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
);

-- Tabla de metas de ahorro
CREATE TABLE savings_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    target_amount REAL NOT NULL,
    current_amount REAL DEFAULT 0,
    deadline TEXT,
    description TEXT
);
```

---

## 🎓 Buenas Prácticas Implementadas

### 1. **Separación de Responsabilidades (MVC)**
- Modelos independientes de la UI
- Controlador como único punto de comunicación
- Vistas sin lógica de negocio

### 2. **Código Limpio**
- Métodos con `@staticmethod` donde corresponde
- Docstrings en todas las clases y métodos
- Type hints en parámetros y retornos
- Nombres descriptivos

### 3. **Manejo de Errores**
- Try-except en operaciones de archivo
- Validaciones de entrada
- Mensajes de error informativos

### 4. **Testing**
- Coverage de lógica crítica
- Tests aislados e independientes
- Base de datos de prueba separada

### 5. **Documentación**
- README completo
- Comentarios en código complejo
- Docstrings con formato estándar

---

## 🐛 Solución de Problemas

### Error: "No module named 'PySide6'"

```bash
pip install PySide6
```

### Error: "Database locked"

Cierra todas las instancias de la aplicación y elimina el archivo `mintly.db.lock` si existe.

### Error al exportar PDF

```bash
pip install reportlab
```

### Los gráficos no se muestran

```bash
pip install matplotlib
```

---

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT.

---

## 👤 Autor

**Iván Mayoral Capel**

**Alumno de 2 DAM Online** 

📧 Email: ivanmayoral.dev@gmail.com

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📅 Proximas features

- [ ] Login de perfiles
- [ ] Multicuenta para compartir gastos con familiares
- [ ] Organización mensual y anual
- [ ] Notificaciones de metas
- [ ] Importación de datos por csv/xlsx
- [ ] Gráficos mejorados
- [ ] API

---

## ⭐ Agradecimientos

A mi profesor de Desarrollo de Interfaces por enseñarnos librerias dentro de python como PySide6 para la creación de interfaces con Python. He aprendido mucho con esta asignatura y ha hecho las clases bastante entretenidas y prácticas, que es como de verdad uno aprende. Muchas gracias :)